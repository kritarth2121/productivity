from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profileupdate',name=username)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    '''if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        #j_form= ProfileUpdateForm(request.POST,instance=request.user.profile)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        #j_form= ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    print(u_form.username)'''


    return render(request, 'users/profile.html')
def profileupdate(request,name):
    user=User.objects.get(username=name)
    print(type(user))
    print(type(request.user))
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        #j_form= ProfileUpdateForm(request.POST,instance=request.user.profile)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-posts',username=name)

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
        #j_form= ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'users/profileupdate.html',context)
import datetime

def logout_page(request):
    profile = request.user.profile # it depends 
    if request.user.is_authenticated:
        logout(request)
        profile.last_time_logout = datetime.datetime.now()
        profile.save()
        print(profile.last_time_logout)
        return render(request,'users/logout.html')
     
