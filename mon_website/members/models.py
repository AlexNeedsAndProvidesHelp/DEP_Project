from django.shortcuts import render
from django.http import HttpResponse
from django.db import models

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

    def __str__(self):
        return self.title