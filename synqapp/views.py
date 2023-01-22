from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello Django!!")


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "synqapp/welcome.html")


class AlbumView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "synqapp/album.html")


class UploadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "synqapp/upload.html")


welcome_page = WelcomeView.as_view()
album_page = AlbumView.as_view()
upload_page = UploadView.as_view()

