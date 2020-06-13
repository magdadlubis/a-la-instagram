from django.contrib import admin

# Register your models here.
from photoalbum.models import Photo, Comment


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("path", "creation_date", "user")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "user")