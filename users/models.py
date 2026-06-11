#Gestiona los usuarios, perfiles y, lo más importante, los roles (Autor, Editor, Administrador).
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ("reader", "Lector"),
        ("reviewer", "Revisor"),
        ("editor", "Editor"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="reader"
    )

    bio= models.TextField(
        max_length=500,
        blank = True
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null= True,
        blank= True
    )