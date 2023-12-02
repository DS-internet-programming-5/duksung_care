from django.urls import path
from . import views

urlpatterns=[
    path('', views.HospitalList.as_view()),
    path('<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('<int:pk>/bookmark/', views.hospital_bookmark, name='hospital_bookmark'),
    path('get_hospital_list/', views.get_hospital_list, name='get_hospital_list'),
    path('category/<str:slug>/', views.category_page),
    path('new_review/<int:pk>/', views.new_review, name='new_review'),
    path('update_review/<int:review_pk>/', views.UpdateReview.as_view(), name='update_review'),
    path('delete_review/<int:review_pk>/', views.delete_review, name='delete_review'),
    path('like_review/<int:review_pk>/', views.likes_review, name='likes_review'),
    path('partnership_detail/<int:hospital_id>/', views.partnership_detail, name='partnership_detail'),
]
