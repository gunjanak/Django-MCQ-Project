from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core import serializers

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


#following class works
@method_decorator(csrf_exempt, name='dispatch')
class SubmitAnswersView(View):

    #the following function works
    # def get(self,request,subject_id):
    #     subject = get_object_or_404(Subject, pk=subject_id)
    #     subject_data = serializers.serialize('json', [subject])
    #     print(subject)
    #     mcqs = MCQQuestion.objects.filter(subject=subject)
    #     # mcqs = list(mcqs[:3])
    #     # mcqs = list(mcqs)
    #     print(mcqs)

    #     data = [{'mcqs': mcqs}]
    #     return JsonResponse({'objects':data})
    
        # if request.method == 'POST':
        #     print("fuck")
        # return render(request, 'display_mcqs.html', {'subject': subject, 'mcqs': mcqs})

    def get(self,request,subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        mcqs = MCQQuestion.objects.filter(subject=subject)  
        if request.method == 'POST':
            print("fuck")
        return render(request, 'display_mcqs.html', {'subject': subject, 'mcqs': mcqs})


    def post(self, request):
        print("Here i am **************************************")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        selected_options = data.get('selectedOptions', {})
        subject_id =  data.get('subjectId',{})

        subject = get_object_or_404(Subject, pk=subject_id)
        

        mcqs = MCQQuestion.objects.filter(subject=subject)  
       
        score = 0
        for mcq in mcqs:
            if str(selected_options.get(str(mcq.id))) == str(mcq.correct_option):
                score += 1

        response_data = {
            'score': score,
        }
        
        return JsonResponse(response_data)