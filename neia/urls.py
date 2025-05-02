from django.urls import path
from . import views

app_name = 'neia'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
]
