from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages


import json

from .models import Subject, MCQQuestion
from .forms import SubjectForm, MCQForm
from .decorators import custom_permission_required

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})


@login_required
@custom_permission_required('MCQ_app.can_create_subject')
def create_subject(request):
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MCQ_app:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'create_subject.html', {'form': form})



@login_required
@custom_permission_required('MCQ_app.can_create_subject')
def create_mcq(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    if request.method == 'POST':
        form = MCQForm(request.POST)
        if form.is_valid():
            mcq = form.save(commit=False)
            mcq.subject = subject
            mcq.save()
            if 'save_and_add_another' in request.POST:
                return redirect('MCQ_app:create_mcq',subject_id)
            else:
                return redirect('MCQ_app:subject_list')
    else:
        form = MCQForm(initial={'subject': subject})
    return render(request, 'create_mcq.html', {'form': form})


def display_mcqs(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    mcqs = MCQQuestion.objects.filter(subject=subject)    
    score = None

    if request.method == 'POST':
        form_data = request.POST
        print(form_data.values)

        correct_ans = [mcq.correct_option for mcq in mcqs]
        all_values = [values for key,values in form_data.items() if key != 'csrfmiddlewaretoken']
        score = sum(1 for i, j in zip(all_values,correct_ans) if i == j)

        print("Number of places with the same items:", score)
        return render(request,'display_score.html',{'score':score})

    return render(request, 'display_mcqs.html', {'subject': subject, 'mcqs': mcqs,'score': score})

# def mcq_question_view(request,subject_id):
#     subject = get_object_or_404(Subject,pk=subject_id)
#     mcqs = MCQQuestion.objects.filter(subject=subject)
#     total_questions = len(mcqs)
#     print(total_questions)

#     current_question_index = int(request.session.get('current_question_index',0))
#     print(current_question_index)

#     if current_question_index >= total_questions:
#         current_question_index = 0
#         return render(request, 'no_more_questions.html')  # Create this template for handling no more questions

#     # Get the current question based on the index
#     current_question = mcqs[current_question_index]


#     # current_question = mcqs[current_question_index] if mcqs else None
    
#     context = {
#         'question': current_question,
#         'total_questions': total_questions,
#         'current_question_index': current_question_index,
#         'subject_id':subject_id,
#     }

#     return render(request, 'mcq_question_template.html', context)
    
# def next_question(request,subject_id,):
#     # Retrieve the current question index from the session
#     current_question_index = int(request.session.get('current_question_index', 0))
#     print(subject_id)
#     # Increment the question index
#     current_question_index += 1
    
#     # Update the session with the new question index
#     request.session['current_question_index'] = current_question_index
    
#     # Redirect to the view to display the next question
#     return redirect('MCQ_app:mcq_question_view', subject_id=subject_id)  # Replace 'your_subject' with the actual subject
