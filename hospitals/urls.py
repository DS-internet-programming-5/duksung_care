from django.urls import path
from . import views

urlpatterns=[
    path('', views.HospitalList.as_view()),
    # path('<int:pk>/', views.HospitalDetail.as_view()),
    path('<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('get_hospital_list/', views.get_hospital_list, name='get_hospital_list'),
    path('new_review/<int:pk>/', views.new_review, name='new_review'),
    path('update_review/<int:review_pk>/', views.UpdateReview.as_view(), name='update_review'),
    path('delete_review/<int:review_pk>/', views.delete_review, name='delete_review'),
]
