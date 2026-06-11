# Maneja los artículos, categorías, etiquetas, comentarios y la lógica de los "Me gusta".

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

    category = models.ForeignKey(
        'Category', 
        on_delete=models.SET_NULL, # Si borras la categoría, el artículo NO se borra, queda como "Sin categoría"
        null=True, 
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
    tags = models.ManyToManyField('Tag', blank=True, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.article.title}"

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')