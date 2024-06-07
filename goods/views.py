from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
from goods.GoodsDao import *
from goods.models import Products
from goods.utils import q_search
from goods.GoodsDao import get_goods_by_category


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    discount = request.GET.get('discount', None) 
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    if category_slug == "all" and category_slug != "" and category_slug !=None:
        goods = (get_goods_by_category())
    else:
        goods = (get_goods_by_category(category_slug=category_slug))

    if order_by and order_by != "default":
        goods = (get_goods_by_category(
            category_slug = category_slug, 
            order_by = order_by,
            discount = (discount=='on')
        ))
    else:
        goods = (get_goods_by_category(
            category_slug = category_slug,
            discount = (discount=='on')
        ))

    if query:
        goods = q_search(query)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    
    context = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    
    product = get_product_by_slug(product_slug)
    context = {"product": product}

    return render(request, "goods/product.html", context=context)
