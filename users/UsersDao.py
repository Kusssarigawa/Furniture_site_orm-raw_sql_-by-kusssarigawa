from django.db import connection
from orders.models import OrderItem, Order
from goods.models import Products

class UsersDao:
    
    @staticmethod
    def update_cart_user(session_key, user_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE cart
                SET user_id = %s
                WHERE session_key = %s
            """, [user_id, session_key])

    @staticmethod
    def get_user_orders(user_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT o.id, o.created_timestamp, oi.id AS order_item_id, p.id AS product_id, p.name AS product_name, oi.price, p.quantity, status
                FROM mebli.order o
                LEFT JOIN order_item oi ON o.id = oi.order_id
                LEFT JOIN product p ON oi.product_id = p.id
                WHERE o.user_id = %s
                ORDER BY o.id DESC
            """, [user_id])
            item_columns = cursor.description[4:]
            item_columns = [i[0] for i in item_columns]
            rows = cursor.fetchall()
        
        orders = {}
        order_items = {}
        for row in rows:
            order_id, order_status = row[0], row[7]
            product_name, item_price, item_quantity = row[4:6+1]

            product = Products(name = product_name)
            order_item = OrderItem(
                order_id = order_id,
                price = item_price,
                quantity = item_quantity,
                product = product
            )
            order = Order(
                    id=order_id,
                    status=order_status
                )

            if order_id not in orders.keys():
                orders[order_id] = Order(
                    id=order_id,
                    status=order_status
                )

        return list(orders.values())
