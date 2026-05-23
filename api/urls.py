from django.urls import path
from .views import get_events, receive_event

urlpatterns = [
    path('event/', receive_event, name='receive_event'),
     path("event/", receive_event),
    path("event/", receive_event),
    path("events/", get_events),
]