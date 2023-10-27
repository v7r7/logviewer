from django.urls import path
from .views import get_log
from .views import get_log_filenames

urlpatterns = [
    path('log/', get_log, name='get_log'),
    path('logs/', get_log_filenames, name='get_log_filenames'),
]
