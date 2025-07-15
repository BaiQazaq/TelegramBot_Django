from django.db import models

# Create your models here.

class UserProfile(models.Model):
    telegram_chat_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username or self.first_name} ({self.telegram_chat_id})"
    
class Message(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    telegram_message_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Msg to {self.user} at {self.created_at}"