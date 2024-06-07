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
        'text_on_page': "Це мебельний магазин , основної метою якого є полегшення замовлення товарів через web-застосунок "
    }

    return render(request, 'main/about.html', context)