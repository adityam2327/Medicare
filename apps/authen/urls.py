from django.contrib import admin
from django.urls import path
from apps.authen import views

urlpatterns = [
  
    path("", views.home , name='home'),
    path("index" , views.index), 
    path('signup/', views.signup),
    path('loginn/', views.loginn),
    path('signout/', views.signout, name='signout'),
    



    

]
