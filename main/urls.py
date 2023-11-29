# main/urls.py
from django.urls import path
from .views import main_page1_view, main_page2_view

urlpatterns = [
    path('main_page1/', main_page1_view, name='main_page1'),
    path('main_page2/', main_page2_view, name='main_page2'),
]