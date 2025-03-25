from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.models import User
    

class GeneratedText(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # Titre généré
    subtitle = models.TextField()  # Sous-titre généré
    question = models.TextField()  # Question générée
    com1 = models.TextField()  # Mots-clés générés
    com2 = models.TextField()
    com3 = models.TextField()
    theme1 = models.TextField()  # Thèmes générés
    theme2 = models.TextField()
    theme3 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="custom_users_groups",  # Ajout d'un related_name pour éviter le conflit
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_users_permissions",  # Ajout d'un related_name pour éviter le conflit
        blank=True
    )

