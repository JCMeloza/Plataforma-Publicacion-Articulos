
#Gestiona el flujo de trabajo (workflow) de revisión
from django.db import models
from django.conf import settings
from articles.models import Article

# Create your models here.

class Review(models.Model):
    DECISION_CHOICES = [
        ('approve', 'Aprobar y Publicar'),
        ('reject', 'Rechazar con observaciones')
    ]
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.TextField()
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES)
    feedback = models.TextField(help_text="Sugerencias para mejorar el artículo", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revisión de {self.article.title} por {self.reviewer.username}"
    
