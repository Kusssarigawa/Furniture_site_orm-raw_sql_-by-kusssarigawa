from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):


    context = {
        'title': 'Home - Головна',
        'content': "Магазин меблів Kussarigawa",
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Home - О нас',
        'content': "About us ",
        'text_on_page': "Very cool and cute furniture shop/by something from us!"
    }

    return render(request, 'main/about.html', context)