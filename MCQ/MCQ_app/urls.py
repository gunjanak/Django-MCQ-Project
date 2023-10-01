from django.urls import path
from .views import SubmitAnswersView
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('create_mcq/<int:subject_id>/', views.create_mcq, name='create_mcq'),
#     path('display_mcqs/<int:subject_id>/', views.display_mcq, 
#          name='display_mcqs'),
#     path('display_mcq/<int:subject_id>/<int:mcq_index>/<int:score>/', 
#          views.display_mcq, name='display_mcq'),
#     path('display_subject_mcqs/<int:subject_id>/', 
#          views.display_subject_mcqs, name='display_subject_mcqs'),
     path('submit_answers/', SubmitAnswersView.as_view(), name='submit_answers'),
     path('submit_answers/<int:subject_id>/',
          SubmitAnswersView.as_view(),name='sub_ans'),

]
