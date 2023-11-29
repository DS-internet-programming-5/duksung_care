from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.user_detail, name='accounts-user'),
    path('modify/', views.modify, name='modify'),
    path('delete/', views.user_delete, name='user_delete'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]