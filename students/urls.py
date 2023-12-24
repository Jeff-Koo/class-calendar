from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_student, name='all_student'),
    path('<int:pk>/', views.get_student, name='get_student'),
]

