from django.db import models

class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_input = models.TextField()
    bot_response = models.TextField()
    
    class Meta:
        ordering = ['-created_at']