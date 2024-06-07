from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from orders.OrdersDao import OrdersDao  # Импорт DAO
from django.utils import timezone

orders_dao = OrdersDao()  # Создание экземпляра DAO

@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order_id = orders_dao.create_order(
                            user_id=user.id,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'] == '1',  # Преобразуем строку в bool
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'] == '1',  # Преобразуем строку в bool
                        )

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе. В наличии - {product.quantity}')
                            created_timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                            orders_dao.create_order_item(
                                created_timestamp=created_timestamp,
                                order_id=order_id,
                                product_id=product.id,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()

                        # Очистка корзины пользователя после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        # return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                # return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_order.html', context=context)