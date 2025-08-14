from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.get_events, name='get_events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/update/', views.update_event, name='update_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]