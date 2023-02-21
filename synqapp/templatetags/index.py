from django import template

register = template.Library()


# image_list内でcountリストのi番目の値を取得するためにindex関数を使用

@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def index_minus1(indexable, i):
    return indexable[i-1]


@register.filter
def is_in_list(list_data, i):
    # iがlist_dataに含まれていれば、trueを返す
    return i in list_data
