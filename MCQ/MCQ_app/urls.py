from django.urls import path

from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('create_mcq/<int:subject_id>/', views.create_mcq, name='create_mcq'),
    path('display_mcqs/<int:subject_id>/', views.display_mcqs, name='display_mcqs'),


]
