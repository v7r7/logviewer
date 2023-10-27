# logapi/urls.py
from django.urls import path
from .views import get_log

urlpatterns = [
    path('log/', get_log, name='get_log'),
]
