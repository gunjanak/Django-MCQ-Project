from django.urls import path

from . import views
from .views import SubjectList
app_name = 'MCQ_app'

urlpatterns = [
    path('subject/', views.subject_list, name='subject_list'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('create_mcq/<int:subject_id>/', views.create_mcq, name='create_mcq'),
    path('display_mcqs/<int:subject_id>/', views.display_mcqs, name='display_mcqs'),
    path('mcq-list/<int:subject_id>/', views.mcq_list, name='mcq_list'),
    path("score-view/",views.score_view,name='score_view'),
    path("",SubjectList.as_view(),name="subject_list"),

  
]
