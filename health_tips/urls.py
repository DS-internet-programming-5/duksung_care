from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('like_post/<int:pk>/', views.likes_post, name='likes_post'),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update_post'),
    path('new_comment/<int:pk>/', views.new_comment, name='new_comment'),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view(), name='update_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)