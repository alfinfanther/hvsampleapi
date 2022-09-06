from django.urls import path
from api import views

urlpatterns = [
    path('v1/user/login', views.LoginView.as_view(), name='api_user_login')
]