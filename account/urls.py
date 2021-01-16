from django.urls import path
from .views import *
from . import views

urlpatterns =[
    path('login/', views.user_login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', user_logout, name='logout'),
    path('dashboard', dashboard, name='dashboard'),
    path('profile', user_profile, name='profile'),
    path('profile/create/', views.create_profile, name='create-profile'),
    path('profile/edit', edit_profile, name='edit-profile'),
    path('change_pass/', views.user_change_pass, name='change_pass'),
    path('change_pass1/', views.user_change_pass1, name='change_pass1'),

]