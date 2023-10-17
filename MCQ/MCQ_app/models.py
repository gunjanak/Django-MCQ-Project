from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from account.models import Profile




# Create your models here.
creators_group,created = Group.objects.get_or_create(name='creators')
readers_group,created = Group.objects.get_or_create(name='readers')


class Subject(models.Model):
    name = models.CharField(max_length=100,unique=True)
   

    def __str__(self):
        return self.name
    
class MCQQuestion(models.Model):
    question_text = models.CharField(max_length=100)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=1,
                                      choices=[('1','Option 1'),
                                                            
                                                            ('2','Option 2'),('3','Option 3'),('4','Option 4')])
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
    

class UserScore(models.Model):
    """
    Table to store user's score on each subject
    """
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    score = models.IntegerField()

   
    
