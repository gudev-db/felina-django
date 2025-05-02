from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ('user', 'Usuário'),
        ('assistant', 'Assistente'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
