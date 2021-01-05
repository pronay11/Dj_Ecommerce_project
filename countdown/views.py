from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from countdown.models import Event


# class EventListView(ListView):
#     model = Event
#     template_name = 'countdown/main.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'countdown/countdown.html'
