from django.shortcuts import render
from django.views import View

# Create your views here.

class MainPageView(View):
    def get(self, request):
        return render(request, 'photoalbum/main_page.html')


class LoginView(View):
    pass


class LogoutView(View):
    pass