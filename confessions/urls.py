
from django.urls import path 
from . import views

# api urls
urlpatterns = [
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('verify-email/', views.verifyEmail, name='verify-email'),
    path('send-msg/<str:recv_username>/', views.sendMessage, name='send-msg')
]