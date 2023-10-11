from django.urls import path

from . import views
app_name = 'MCQ_app'

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('create_mcq/<int:subject_id>/', views.create_mcq, name='create_mcq'),
    path('display_mcqs/<int:subject_id>/', views.display_mcqs, name='display_mcqs'),
    # path('mcq_question_view/<int:subject_id>/',views.mcq_question_view,name='mcq_question_view'),
    # path('next_question/<int:subject_id>/',views.next_question,name='next_question'),
]
