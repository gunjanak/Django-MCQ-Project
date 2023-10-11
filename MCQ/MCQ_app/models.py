from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType





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
    
# Create permissions
# content_type = ContentType.objects.get_for_model(MCQQuestion)
# create_permission = Permission.objects.create(
#     codename='can_create_subject',
#     name='Can Create Subject',
#     content_type=content_type,
# )

# edit_permission = Permission.objects.create(
#     codename='can_edit_subject',
#     name='Can Edit Subject',
#     content_type=content_type,
# )

# delete_permission = Permission.objects.create(
#     codename='can_delete_subject',
#     name='Can Delete Subject',
#     content_type=content_type,
# )

# # Assign permissions to the "creators" group
# creators_group.permissions.add(create_permission, edit_permission, delete_permission)

