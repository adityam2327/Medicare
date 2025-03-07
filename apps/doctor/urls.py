from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.dash, name='dash'),
  







        path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
 

  
    
    path('community-updates/', views.community_updates, name='community_updates'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('logout/', views.logout, name='logout'),
]
