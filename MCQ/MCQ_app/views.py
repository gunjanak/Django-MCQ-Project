from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User

from json import dumps 
import json

from .models import Subject, MCQQuestion,UserScore
from .forms import SubjectForm, MCQForm,UserSubjectForm
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



@login_required
def mcq_list(request,subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    mcq_objects = MCQQuestion.objects.filter(subject=subject) 
    mcq_list = []

    for mcq in mcq_objects:
        mcq_item = {
            'question':mcq.question_text,
            'options':[mcq.option1,mcq.option2,mcq.option3,mcq.option4],
            'correct_answer':mcq.correct_option
        }

        mcq_list.append(mcq_item)

    the_subject = [{"subject":subject.name}]
    print(the_subject[0])
    dataJSON = dumps(mcq_list) 
    the_subject = dumps(the_subject)
    print(type(dataJSON))
    return render(request, 'mcq_list_2.html', {'data': dataJSON,'subject':the_subject}) 

@login_required
def score_view(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        print(post_data)
        print(request.user)
        value = post_data['value']
        print(value)
        print(post_data['subject'])
        subject = get_object_or_404(Subject,name=post_data['subject'])
        print(f"The subject is {subject}")
        score_object = UserScore(user=request.user,
                                 subject=subject,
                                 score=post_data['value'])
        score_object.save()
       
        # Process the value as needed
        return JsonResponse({'message': 'Received value from JavaScript: {}'.format(value)})


#list all the subjects
class SubjectList(ListView):
    model = Subject
    template_name = 'subject_list_user.html'  # Specify the template name
    context_object_name = 'subject_list'  # Specify the context variable name for the list of objects

def display_all_Scores(request):
    if request.method=='POST':
        form = UserSubjectForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user = User.objects.get(username=user)
            print("******************")
            print(user.id)
            subject = form.cleaned_data['subject']
            subject = Subject.objects.get(name=subject)
            print(subject.id)

            print("*********************")
            user_scores = UserScore.objects.filter(user=user.id,subject=subject.id)
            return render(request,'scores.html',{'user_scores':user_scores})
        
    else:
        form = UserSubjectForm()

    return render(request,'user_subject_form.html',{'form':form})


        