# authentication > api > urls.py
from django.urls import path, include
from .views import RegistrationAPIView


urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
]