from django.urls import path
from . import views

# urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('word_score/', views.word_score_view, name='word_score'),  
    path('task-status/<str:task_id>/', views.task_status_view, name='task_status'),  # Trailing slash!
]