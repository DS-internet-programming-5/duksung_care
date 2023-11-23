from django.urls import path
from . import views

urlpatterns=[
    path('', views.HospitalList.as_view()),
    path('<int:pk>/', views.HospitalDetail.as_view()),
    path('get_hospital_list/', views.get_hospital_list, name='get_hospital_list'),
]
