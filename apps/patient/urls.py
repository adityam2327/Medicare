from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('health-calendar/', views.health_calendar, name='health_calendar'),
     path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule-appointment/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),


    path('care-finder/', views.care_finder, name='care_finder'),  # Combined hospital finder + chatbot page
    path('care-finder/find', views.find_hospitals, name='find_hospitals'),  # API to fetch hospitals
    path('care-finder/chatbot-response/', views.chatbot_response, name='chatbot_response'),  # Handles chatbot messages


    
    path('chatbot/', views.chatbot, name='chatbot'), 
    
    path('community-updates/', views.community_updates, name='community_updates'),
    path('health-connect/', views.health_connect, name='health_connect'),
    path('medinfo/', views.medinfo, name='medinfo'),


    path('profile/', views.patient_profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]


