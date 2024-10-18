from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('private/<str:username>/', views.private_chat, name='private_chat'),  # One-on-one chat
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),  # Group chat rooms
    path('users/', views.user_list_view, name='user_list'),
    path('chatrooms/', views.chat_room_list, name='chat_rooms_list'),
    path('private/<str:username>/send/', views.send_private_message, name='send_private_message'),
]
