from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .forms import UserLoginForm, ProfileForm


def user_profile(request):
    Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def create_profile(request):
    profile=request.user.profile
    # profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    context={'form':form}
    if request.method == 'POST':
        form=ProfileForm(request.POST.request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render (request,'accounts/create_profile.html',context)


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save;
        return redirect('login')
    else:
        return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print("valid")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                print("login done")
                return redirect('home')
            context = {
                'form': form,
                'error': "Invalid username or password !!"
            }
            return render(request, 'accounts/login.html', context)

    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


# change Password with old password
def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Changed Successfully ')
                return HttpResponseRedirect('profile')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/change_pass.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Change Password Without Old Password
def user_change_pass1(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Changed Successfully ')
                return HttpResponseRedirect('profile')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request, 'accounts/change_pass1.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')
