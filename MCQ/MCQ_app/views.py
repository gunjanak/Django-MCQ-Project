from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core import serializers
from django.core.paginator import Paginator

import json

from .models import Subject, MCQQuestion
from .forms import SubjectForm, MCQForm

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'create_subject.html', {'form': form})

def create_mcq(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    if request.method == 'POST':
        form = MCQForm(request.POST)
        if form.is_valid():
            mcq = form.save(commit=False)
            mcq.subject = subject
            mcq.save()
            return redirect('subject_list')
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
       
        # for mcq in mcqs:
            
        #     print(f"{mcq.id}:{mcq.correct_option} ")
        #     correct_ans.append(mcq.correct_option)

        all_values = [values for key,values in form_data.items() if key != 'csrfmiddlewaretoken']
        # all_values = all_values[1:]
        print(all_values) 
        print(correct_ans)
        # score = correct_answers
        score = sum(1 for i, j in zip(all_values,correct_ans) if i == j)

        print("Number of places with the same items:", score)
        return render(request,'display_score.html',{'score':score})

    return render(request, 'display_mcqs.html', {'subject': subject, 'mcqs': mcqs,'score': score})

