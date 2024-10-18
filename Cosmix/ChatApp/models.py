from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from .validators import MaxDurationValidator

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    last_seen = models.DateTimeField(default=timezone.now)

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save()

    def is_online(self):
        now = timezone.now()
        return (now - self.last_seen).seconds < 300
    
    def __str__(self):
        return self.user.username
    

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, related_name='private_chats_1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='private_chats_2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Chat between {self.user1.username} and {self.user2.username}'
    
    class Meta:
        unique_together = ('user1', 'user2')


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.CASCADE)
    private_chat = models.ForeignKey(PrivateChat, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    ])
    video = models.FileField(upload_to='videos/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv']),
        # MaxDurationValidator(30)  # Custom validator for 30 seconds
    ])
    audio = models.FileField(upload_to='audios/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg']),
        # MaxDurationValidator(60)  # Custom validator for 1 minute
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.chatroom:
            return f"Message from {self.sender.username} in ChatRoom '{self.chatroom.name}' at {self.timestamp}"
        elif self.private_chat:
            return f"Message from {self.sender.username} in PrivateChat at {self.timestamp}"
        else:
            return f"Message from {self.sender.username} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']