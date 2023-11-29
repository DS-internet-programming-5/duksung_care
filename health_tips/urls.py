from django.urls import path

from . import views
from .views import post_list, post_detail, PostUpdate

urlpatterns = [
    path('post/', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update_post'),

]
