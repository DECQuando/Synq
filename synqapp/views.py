from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Image
from .forms import ImageForm
from django.urls import reverse_lazy


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "synqapp/welcome.html")


welcome_page = WelcomeView.as_view()


class CSRFExemptMixin(object):
    """
    クラス汎用ビューでも@csrf_exempt使用できるようにこのクラスを追加
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class ImagePost(CSRFExemptMixin, generic.CreateView):
    model = Image
    form_class = ImageForm
    template_name = "synqapp/image_form.html"
    # success_urlはフォームが作成された後のリダイレクト先。
    # reverse_lazyの引数はsynqapp/urls.pyに定義したurlのname属性。
    # そのnameをurlに変換するのがreverse_lazy。
    success_url = reverse_lazy('synqapp:image_post')


class ImageList(generic.ListView):
    model = Image
    ordering = "-created_at"
    template_name = "synqapp/image_list.html"
    context_object_name = "image_context_list"


class ImageDetail(generic.DetailView):
    model = Image
    template_name = "synqapp/image_detail.html"
    context_object_name = "image_context"
