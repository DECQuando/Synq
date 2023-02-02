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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ImageList, self).get_context_data(**kwargs)
        # 画像のグループ番号を格納するリスト
        image_group_list = []   # [12, 11, 10, 10, 9, ..., 1, 1]
        # 画像のグループ内での番号を格納するリスト
        pk_in_group = []        # [1,  1,  1,  2,  1, ..., 1, 2]
        # それぞれのグループに属する画像の枚数を格納（group=1~max(group)）
        group_count_list = []   # [2(image_group1), ..., 1(image_group9), 2(image_group10), 1(group11), 1(group12)]

        for i, image in enumerate(self.object_list):
            group = image.group
            image_group_list.append(group)      # 下でgroup_count_listを作成するときに使用
            if i == 0:
                # １つ目の画像はpk=1
                pk = 1
            else:
                # 2つ目以降の画像は、下の条件分岐
                # 前の画像とグループが等しければpk+=1
                if previous_picture_group == group:
                    pk += 1
                else:
                    pk = 1
            pk_in_group.append(pk)
            previous_picture_group = group
        print(max(image_group_list))

        for group_id in range(max(image_group_list)):
            # group_list.count(10)で、group_listの中で10の出現回数を算出
            # e.g., a = [1, 1, 1, 2];    a.count(1) -> 3
            # groupは1始まりなので、group_id+1
            group_count_list.append(image_group_list.count(group_id+1))

        context["pk_in_group"] = pk_in_group        # primary key in the group/そのグループ内での番号
        context["count"] = group_count_list         # number of images in the group/そのグループに属する写真の枚数
        print(context)
        return context

    # def start_end(filtered_object):
    #     prev_data = Timestamp.objects.filter(created_at__lt=filtered_object.created_at).order_by('created_at').last()
    #     if prev_data is None:
    #         start = None
    #     else:
    #         start = prev_data.created_at
    #     end = filtered_object.created_at
    #     return start, end

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(TimestampList, self).get_context_data(**kwargs)
    #     context['count'] = []
    #     for timestamp in self.object_list:
    #         start, end = start_end(timestamp)
    #         count_value = data_filter(start, end, 1)
    #         # 昇順時
    #         # context['count'].append(count_value)
    #         # 降順時
    #         context['count'].insert(0, count_value)
    #     if ExperimentData.objects.exists():
    #         if self.object_list.exists():
    #             # 実験データもタイムスタンプ（self.object_list）も存在している時
    #             last_data = Timestamp.objects.all().order_by('created_at').last().created_at
    #             remain_data = ExperimentData.objects.filter(created_at__gt=last_data).count()
    #             context['non_timestamp_data_count'] = remain_data
    #         else:
    #             # 実験データがあってタイムスタンプが存在しない時
    #             remain_data = ExperimentData.objects.all().count()
    #             context['non_timestamp_data_count'] = remain_data
    #     return context


class ImageDetail(generic.DetailView):
    model = Image
    template_name = "synqapp/image_detail.html"
    context_object_name = "image_context"
