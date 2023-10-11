from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import LoginForm, UserRegistrationForm,UserEditForm,ProfileEditForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)

            #set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])

            #save the Uset object
            new_user.save()
            #create the user profile
            Profile.objects.create(user=new_user)

            return render(request,'registration/register_done.html',
                          {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,'registration/register.html',{'user_form':user_form})

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated successfully')
        else:
            messages.error(request,'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile
        )
    return render(request,'registration/edit.html',{'user_form':user_form,'profile_form':profile_form})
