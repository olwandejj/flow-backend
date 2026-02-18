from django.urls import path
from .views import register_api, login_api

urlpatterns = [
    path('api/register/', register_api, name='api_register'),
    path('api/login/', login_api, name='api_login'),
]
