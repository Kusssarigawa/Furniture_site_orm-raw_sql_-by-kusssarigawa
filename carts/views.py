from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from carts.utils import get_user_carts
from .CartsDao import (get_product_by_id, get_cart_by_user_and_product, get_cart_by_session_and_product,
                       create_cart, update_cart_quantity, get_cart_by_id, delete_cart)

def cart_add(request):
    product_id = request.POST.get("product_id")
    product = get_product_by_id(product_id)

    if not product:
        return JsonResponse({"message": "Товар не найден"}, status=404)

    if request.user.is_authenticated:
        cart = get_cart_by_user_and_product(request.user.id, product_id)
        if cart:
            update_cart_quantity(cart['id'], cart['quantity'] + 1)
        else:
            create_cart(request.user.id, None, product_id, 1)
    else:
        cart = get_cart_by_session_and_product(request.session.session_key, product_id)
        if cart:
            update_cart_quantity(cart['id'], cart['quantity'] + 1)
        else:
            create_cart(None, request.session.session_key, product_id, 1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string("carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = get_cart_by_id(cart_id)

    if not cart:
        return JsonResponse({"message": "Корзина не найдена"}, status=404)

    update_cart_quantity(cart['id'], quantity)
    updated_quantity = quantity

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string("carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,
    }

    return JsonResponse(response_data)

def cart_remove(request):
    cart_id = request.POST.get("cart_id")

    cart = get_cart_by_id(cart_id)

    if not cart:
        return JsonResponse({"message": "Корзина не найдена"}, status=404)

    quantity = cart['quantity']
    delete_cart(cart['id'])

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string("carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
