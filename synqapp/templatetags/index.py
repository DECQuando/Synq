from django import template

register = template.Library()


# image_list内でcountリストのi番目の値を取得するためにindex関数を使用

@register.filter
def index(indexable, i):
    return indexable[i]
