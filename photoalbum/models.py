from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

UserModel = get_user_model()

class Photo(models.Model):
    path = models.CharField(max_length=128, verbose_name='Ścieżka do zdjęcia')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='Użytkownik')