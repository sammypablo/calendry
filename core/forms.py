# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Event, Task
from django.utils import timezone
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm your password'
        })

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your password'
        })

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            base_classes = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            if field in ['start_time', 'end_time']:
                self.fields[field].widget = forms.DateTimeInput(
                    attrs={
                        'type': 'datetime-local',
                        'class': base_classes
                    },
                    format='%Y-%m-%dT%H:%M'
                )
            else:
                self.fields[field].widget.attrs.update({
                    'class': base_classes
                })
        
        # Set default times if creating new event
        if not self.instance.pk:
            now = timezone.now()
            later = now + timezone.timedelta(hours=1)
            self.initial['start_time'] = now.strftime('%Y-%m-%dT%H:%M')
            self.initial['end_time'] = later.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time")
        
        return cleaned_data

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 
                 'event_type', 'color', 'location', 'is_all_day', 'is_recurring']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        
        self.fields['due_date'].widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            },
            format='%Y-%m-%dT%H:%M'
        )
        
        # Set default due_date to now + 1 day
        if not self.instance.pk:
            self.initial['due_date'] = (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']

