from django.urls import path
from .views import EventDetailView

app_name = 'countdown'

urlpatterns = [
    # path('', EventListView.as_view(), name = 'event-list'),
    path('', EventDetailView.as_view(), name = 'event-detail'),

]
