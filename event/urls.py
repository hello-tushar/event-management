from django.urls import path
from event.views import *
urlpatterns = [
    path('home/', home, name = 'home/'),
    path('home/event-detail/<int:id>', eventDetail, name = 'home/event-detail/'),
    path('test/', test),
    path('home/create-event/', create_event, name = 'home/create-event/'),
    path('home/update-event/<int:id>', update_event, name = 'home/update-event/'),
    path('home/delete-event/<int:id>', delete_event, name = 'home/delete-event/'),
    path('home/organizer-dashboard/', organizerDashboard, name = 'home/organizer-dashboard/')
]
