# Generated by Django 2.2.7 on 2020-06-12 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photoalbum', '0002_photo_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='likes',
        ),
        migrations.AddField(
            model_name='photo',
            name='likes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Autor', to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
    ]
