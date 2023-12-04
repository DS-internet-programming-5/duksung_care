from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include

from . import views
from .views import post_list, post_detail, PostUpdate, new_comment, PostCreate, delete_comment

urlpatterns = [
    path('post/', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    # path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create_post/', PostCreate.as_view(), name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('new_comment/<int:pk>/', new_comment, name='new_comment'),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view(),name='update_comment'),
    path('delete_comment/<int:pk>', delete_comment, name='delete_comment'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update_post'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    ]
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



