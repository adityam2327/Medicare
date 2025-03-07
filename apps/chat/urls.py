from django.urls import path
from apps.chat import views


urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/', views.chat, name='chat'),

]