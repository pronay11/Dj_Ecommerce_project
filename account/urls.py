from django.urls import path
from .views import *
from . import views

urlpatterns =[
    path('login/', user_login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', user_logout, name='logout'),
    path('dashboard', dashboard, name='dashboard'),
    path('profile', user_profile, name='profile'),
    path('profile/create', create_profile, name='create-profile'),
    path('profile/edit', edit_profile, name='edit-profile'),
    path('changepass/', views.user_change_pass, name='changepass'),
    path('changepass1/', views.user_change_pass1, name='changepass1'),

]