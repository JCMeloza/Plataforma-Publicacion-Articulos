# Maneja los artículos, categorías, etiquetas, comentarios y la lógica de los "Me gusta".
from email.policy import default
from enum import unique


from django.db import models
from django.conf import settings

# Create your models here.
class Article(models.Model):
    STATUS_CHOICES=[
        ('draft', 'Borrador'),
        ('pending', 'En Revisión'),
        ('published', 'Publicado'),
        ('rejected', 'Rechazado'),
    ]

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image= models.ImageField(upload_to='articles/', null= True, blank=True)

    status= models.CharField( 
        max_length=10,
        choices = STATUS_CHOICES,
        default='draft'    
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title