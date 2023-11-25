from django.urls import path
from . import views

urlpatterns=[
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
]