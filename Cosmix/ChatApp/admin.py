from django.contrib import admin
from .models import UserProfile, ChatRoom, PrivateChat, Message

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','last_seen')
    search_fields = ('user__username',)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name','created_at')
    search_fields = ('name',)

@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')
    search_fields = ('user1__username', 'user2__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'private_chat', 'chatroom', 'content', 'timestamp')
    search_fields = ('sender__username', 'chat_room__name', 'private_chat__user1__username', 'private_chat__user2__username')
