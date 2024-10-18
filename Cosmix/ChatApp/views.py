from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import ChatRoom, PrivateChat, Message, UserProfile
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST

# Create your views here.
def home_view(request):
    return render(request, 'index.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('home')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('home')

    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('home')

    return redirect('home')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


def chat_room_list(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


def user_list_view(request):
        # Fetch all users and their profiles
    users = UserProfile.objects.all()

    # Separate users into online and offline lists
    # online_users = []
    # offline_users = []

    # for user in users:
    #     if user.is_online:
    #         online_users.append(user)
    #     else:
    #         offline_users.append(user)

    context = {
        'users': users,
    }

    return render(request, 'user_list.html', context)


def chat_room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    return render(request, 'room.html', {'room_name': room_name})


@require_POST
def create_room(request):
    room_name = request.POST.get('room_name')
    if room_name:
        ChatRoom.objects.create(name=room_name)
    return redirect('chat_room_list')


def private_chat(request, username):
    user2 = get_object_or_404(User, username=username)
    # Ensure user1 is always the lexicographically smaller user
    if request.user.username < user2.username:
        user1 = request.user
        user2 = user2
    else:
        user1 = user2
        user2 = request.user

    # Get or create the private chat with consistent ordering
    private_chat, created = PrivateChat.objects.get_or_create(
        user1=user1, 
        user2=user2
    )

    messages = Message.objects.filter(private_chat=private_chat).order_by('timestamp')

    context = {
        'private_chat': private_chat, 
        'messages': messages, 
        'user1': user1, 
        'user2': user2
        }
    
    return render(request, 'private_chat.html', context)

@login_required
def send_private_message(request, username):
    # Get the receiver user object
    receiver = get_object_or_404(User, username=username)

    # Prevent users from sending messages to themselves
    if request.user == receiver:
        return redirect('private_chat', username=username)  # Redirect or handle this case as needed

    # Find or create the private chat between the two users
    private_chat, created = PrivateChat.objects.get_or_create(
        user1=min(request.user, receiver, key=lambda u: u.username),
        user2=max(request.user, receiver, key=lambda u: u.username)
    )

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            # Create a new message
            Message.objects.create(sender=request.user, private_chat=private_chat, content=content)

    # Redirect back to the private chat page
    return redirect('private_chat', username=username)