"""
URL configuration for calendry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# calendry/urls.py

from django.contrib import admin
from django.urls import path
from core.views import (
    home, register_view, login_view, logout_view,
    dashboard, calendar_view, get_events,
    create_event, EventListView, EventCreateView, 
    EventUpdateView, EventDeleteView,
    task_list, task_create, task_update, 
    task_delete, task_toggle, settings
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('calendar/', calendar_view, name='calendar'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/create/', EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('api/events/', get_events, name='get_events'),
    path('api/events/create/', create_event, name='create_event'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/<int:task_id>/update/', task_update, name='task_update'),
    path('tasks/<int:task_id>/delete/', task_delete, name='task_delete'),
    path('tasks/<int:task_id>/toggle/', task_toggle, name='task_toggle'),
    path('settings/', settings, name='settings'),
]
