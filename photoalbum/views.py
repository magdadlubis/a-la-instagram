from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from photoalbum.models import *
from photoalbum.forms import *
from PIL import Image

# Create your views here.

class MainPageView(LoginRequiredMixin, View):
    def get(self, request):
        form = UploadPhotoForm()
        photos = Photo.objects.all().order_by('-creation_date')
        return render(request, 'photoalbum/main_page.html', {'photos': photos, 'form': form})

    def post(self, request):
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['file']
            Photo.objects.create(path=image.name, user=self.request.user)
            fs = FileSystemStorage(location='photoalbum/static/photoalbum/')
            fs.save(image.name, image)
            return redirect('/')
        return HttpResponse('Nie udało się załadować pliku')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'photoalbum/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                msg = 'Niepoprawny login lub hasło!'
                return render(request, 'photoalbum/login.html', {'form': form, 'msg': msg})
        #return render(request, 'photoalbum/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('main-page'))


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'photoalbum/add_user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not UserModel.objects.filter(username=username):
                UserModel.objects.create_user(username=username, email=username, password=password)
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse_lazy('main-page'))
            else:
                msg = 'Nazwa użytkownika (e-mail) jest już w użyciu!'
                return render(request, 'photoalbum/add_user.html', {'form': form, 'msg': msg})
        #return render(request, 'twitter/add_user.html', {'form': form})


class UserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(UserModel, pk=user_id)
        photos = Photo.objects.filter(user=user).order_by('-creation_date')
        return render(request, 'photoalbum/user.html', {'photos': photos, 'user': user})

class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditUserForm(instance=self.request.user)
        return render(request, 'photoalbum/edit_user.html', {'form': form})

    def post(self, request):
        form = EditUserForm(request.POST, instance=self.request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            user = UserModel.objects.get(pk=self.request.user.pk)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('edit-user')
        return render(request, 'photoalbum/edit_user.html', {'form': form})


class PhotoView(LoginRequiredMixin, View):
    def get(self, request, photo_id):
        photo = get_object_or_404(Photo, pk=photo_id)
        comments = Comment.objects.filter(photo=photo).order_by('creation_date')
        form = CommentForm()
        return render(request, 'photoalbum/photo.html', {'photo': photo, 'comments': comments, 'form': form})

    def post(self, request, photo_id):
        photo = get_object_or_404(Photo, pk=photo_id)
        comments = Comment.objects.filter(photo=photo).order_by(('creation_date'))
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            Comment.objects.create(comment=comment, user=self.request.user, photo=photo)
            return redirect('photo', photo_id=photo_id)
        return render(request, 'photoalbum/photo.html', {'photo': photo, 'comments': comments, 'form': form})



class LikeView(LoginRequiredMixin, View):
    def get(self, request, photo_id):
        photo = get_object_or_404(Photo, pk=photo_id)
        user = request.user
        photo.likes.add(user)
        return redirect('/')


class UnlikeView(LoginRequiredMixin, View):
    def get(self, request, photo_id):
        photo = get_object_or_404(Photo, pk=photo_id)
        user = request.user
        photo.likes.remove(user)
        return redirect('/')