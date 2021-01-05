from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User,auth
from .models import Profile
from django.contrib import messages

from .forms import UserLoginForm, ProfileForm, TestForm


@login_required
def user_profile(request):
    Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html')


@login_required
def create_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'accounts/create_profile.html', context)


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
        return render(request,'accounts/register.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
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

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
# def user_signup(request):
#     form = UserCreationForm()
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         else:
#             form = UserCreationForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'accounts/register.html', context)


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
      fm = PasswordChangeForm(user=request.user,data=request.POST)
      if fm.is_valid():
        fm.save()
        update_session_auth_hash(request,fm.user)
        messages.success(request,'Password Changed Successfully ')
        return HttpResponseRedirect('profile')
    else:
      fm = PasswordChangeForm(user=request.user)
    return render(request,'accounts/changepass.html',{'form':fm})
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
        return render(request, 'accounts/changepass1.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')

