from django.db import models

# Create your models here.
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
    
