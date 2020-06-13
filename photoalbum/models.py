from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserModel(AbstractUser):
    username = models.EmailField(unique=True, verbose_name='Nazwa użytkownika', max_length=128)

class Photo(models.Model):
    path = models.CharField(max_length=128, verbose_name='Ścieżka do zdjęcia')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='Użytkownik', related_name='Autor')
    likes = models.ManyToManyField(UserModel)

    def __str__(self):
        return self.path

class Comment(models.Model):
    comment = models.CharField(max_length=60, verbose_name='Komentarz')
    user = models.ForeignKey(UserModel, verbose_name='Użytkownik', on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, verbose_name='Zdjęcie', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data dodania komentarza')

    def __str__(self):
        return self.comment