from django import forms
from django.contrib.auth.models import User

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

class UserSubjectForm(forms.Form):
    user = forms.CharField(label='User',required=True)
    subject = forms.CharField(label='Subject',required=False)

    def clean_user(self):
        user_username = self.cleaned_data.get('user')
        try:
            user = User.objects.get(username=user_username)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return user
