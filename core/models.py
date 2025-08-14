from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    timezone = models.CharField(max_length=100, default='UTC')
    
    # Add these to resolve the reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="core_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions",
        related_query_name="user",
    )

class Event(models.Model):
    EVENT_TYPES = (
        ('meeting', 'Meeting'),
        ('reminder', 'Reminder'),
        ('task', 'Task'),
        ('holiday', 'Holiday'),
        ('other', 'Other'),
    )
    
    COLOR_CHOICES = (
        ('#3b82f6', 'Blue'),
        ('#10b981', 'Green'),
        ('#f59e0b', 'Yellow'),
        ('#ef4444', 'Red'),
        ('#8b5cf6', 'Purple'),
        ('#ec4899', 'Pink')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='meeting')
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='#3b82f6')
    location = models.CharField(max_length=200, blank=True)
    is_all_day = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def get_html_url(self):
        return f'<a href="/events/{self.id}/update/">{self.title}</a>'
    
    @property
    def get_color_class(self):
        return {
            '#3b82f6': 'bg-blue-100 text-blue-800',
            '#10b981': 'bg-green-100 text-green-800',
            '#f59e0b': 'bg-yellow-100 text-yellow-800',
            '#ef4444': 'bg-red-100 text-red-800',
            '#8b5cf6': 'bg-purple-100 text-purple-800',
            '#ec4899': 'bg-pink-100 text-pink-800'
        }.get(self.color, 'bg-blue-100 text-blue-800')
    
    class Meta:
        ordering = ['start_time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['due_date']
