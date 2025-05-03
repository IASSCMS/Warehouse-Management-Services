from django.urls import path
from .views import check_endpoint

urlpatterns = [
    path('check/', check_endpoint, name='check_endpoint'),
]
