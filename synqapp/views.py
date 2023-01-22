from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello Django!!")

class SampleView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "synqapp/upload.html")
upload_page = SampleView.as_view()
