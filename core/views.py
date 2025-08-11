# core/views.py



from core.models import Event
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Event, User, Task
from .forms import CustomUserCreationForm, LoginForm, EventForm, TaskForm
from datetime import datetime, timedelta
import json
import pytz


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'core/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    today = datetime.now().date()
    events = Event.objects.filter(user=request.user, start_time__date=today)
    return render(request, 'core/dashboard.html', {
        'events': events,
        'today': today
    })

@login_required
def calendar_view(request):
    return render(request, 'core/calendar.html')

@login_required
def get_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    events = Event.objects.filter(
        user=request.user,
        start_time__gte=start,
        end_time__lte=end
    )
    
    event_data = []
    for event in events:
        event_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'description': event.description,
            'type': event.event_type,
            'allDay': event.is_all_day,
            'color': get_event_color(event.event_type)
        })
    
    return JsonResponse(event_data, safe=False)

def get_event_color(event_type):
    colors = {
        'meeting': '#3b82f6',
        'reminder': '#10b981',
        'task': '#f59e0b',
        'holiday': '#ef4444',
        'other': '#8b5cf6'
    }
    return colors.get(event_type, '#3b82f6')

@login_required
@require_http_methods(["POST"])
def create_event(request):
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.save()
        return JsonResponse({
            'status': 'success',
            'event': {
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
                'color': event.color,
                'type': event.event_type
            }
        })
    return JsonResponse({
        'status': 'error',
        'errors': form.errors.as_json()
    }, status=400)
        # ... error handling ...
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return render(request, 'core/tasks.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'core/confirm_delete.html', {'object': task})

@login_required
def task_toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        return JsonResponse({'status': 'success', 'completed': task.completed})
    return JsonResponse({'status': 'error'})

@login_required
def settings(request):
    if request.method == 'POST':
        timezone = request.POST.get('timezone')
        if timezone:
            request.user.timezone = timezone
            request.user.save()
            return redirect('settings')
    return render(request, 'core/settings.html', {
        'timezones': pytz.all_timezones
    })

# core/views.py
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
        
    return render(request, 'core/confirm_delete.html', {'object': task})


@login_required
@require_http_methods(["POST"])
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
        updated_event = form.save()
        return JsonResponse({
            'status': 'success',
            'event': {
                'id': updated_event.id,
                'title': updated_event.title,
                'start': updated_event.start_time.isoformat(),
                'end': updated_event.end_time.isoformat(),
                'color': updated_event.color,
                'type': updated_event.event_type
            }
        })
    return JsonResponse({
        'status': 'error',
        'errors': form.errors.as_json()
    }, status=400)

@login_required
@require_http_methods(["POST"])
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    event.delete()
    return JsonResponse({'status': 'success'})