from django.db import models
from django.contrib.auth.models import User


class VideoSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions')
    video_url = models.URLField(max_length=200)
    video_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'video_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.video_id}"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        VideoSession, on_delete=models.CASCADE, related_name='messages')
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.session.user.username}: {self.user_message[:50]}"
