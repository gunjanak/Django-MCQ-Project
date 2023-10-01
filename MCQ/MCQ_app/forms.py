from django import forms
from .models import Subject, MCQQuestion

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class MCQForm(forms.ModelForm):
    class Meta:
        model = MCQQuestion
        fields = ['subject', 'question_text', 
                  'option1', 'option2', 'option3', 'option4', 'correct_option']
