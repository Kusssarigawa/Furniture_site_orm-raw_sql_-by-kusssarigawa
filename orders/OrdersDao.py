from django.db import connection
from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models.functions import Coalesce
from orders.models import Order, OrderItem
from decimal import Decimal
from django.utils import timezone


class OrdersDao:
    def create_order(self, user_id, phone_number, requires_delivery, delivery_address, payment_on_get):
        """Создает новый заказ."""
        
        with connection.cursor() as cursor:
            created_timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                """
                INSERT INTO mebli.order (status,is_paid,user_id, phone_number,created_timestamp, requires_delivery, delivery_address, payment_on_get)
                VALUES ('В обработке',false,%s, %s, %s, %s, %s,%s);
                """,
                [user_id, phone_number,created_timestamp, requires_delivery, delivery_address, payment_on_get],
            )
            cursor.execute( 
                """
                SELECT id FROM mebli.Order ORDER BY id LIMIT 1
                """
            )
            order_id = cursor.fetchone()[0]
        return order_id

    def create_order_item(self, order_id, product_id,created_timestamp, name, price, quantity):
        """Создает новый элемент заказа."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO order_item (order_id, product_id,created_timestamp, name, price, quantity)
                VALUES (%s,%s, %s, %s, %s, %s)
                """,
                [order_id, product_id,created_timestamp, name, price, quantity],
            )

    def get_order_by_id(self, order_id):
        """Возвращает заказ по его ID."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM order WHERE id = %s
                """,
                [order_id],
            )
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'user_id': row[1],
                    'created_timestamp': row[2],
                    'phone_number': row[3],
                    'requires_delivery': row[4],
                    'delivery_address': row[5],
                    'payment_on_get': row[6],
                    'is_paid': row[7],
                    'status': row[8],
                }
        return None

    def get_order_items_by_order_id(self, order_id):
        """Возвращает список элементов заказа по его ID."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM order_item WHERE order_id = %s
                """,
                [order_id],
            )
            rows = cursor.fetchall()
            order_items = []
            for row in rows:
                order_items.append({
                    'id': row[0],
                    'order_id': row[1],
                    'product_id': row[2],
                    'name': row[3],
                    'price': row[4],
                    'quantity': row[5],
                    'created_timestamp': row[6],
                })
            return order_items

    def update_order_status(self, order_id, status):
        """Обновляет статус заказа."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE order SET status = %s WHERE id = %s
                """,
                [status, order_id],
            )

    def get_orders_by_user_id(self, user_id):
        """Возвращает список заказов пользователя по его ID."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM order WHERE user_id = %s
                """,
                [user_id],
            )
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                orders.append({
                    'id': row[0],
                    'user_id': row[1],
                    'created_timestamp': row[2],
                    'phone_number': row[3],
                    'requires_delivery': row[4],
                    'delivery_address': row[5],
                    'payment_on_get': row[6],
                    'is_paid': row[7],
                    'status': row[8],
                })
            return orders

    def get_total_price_for_order(self, order_id):
        """Возвращает общую стоимость заказа по его ID."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT SUM(oi.quantity * oi.price) AS total_price
                FROM order_item oi
                WHERE oi.order_id = %s
                """,
                [order_id],
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return Decimal('0.00')

    def get_total_quantity_for_order(self, order_id):
        """Возвращает общее количество товаров в заказе по его ID."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT SUM(oi.quantity) AS total_quantity
                FROM order_item oi
                WHERE oi.order_id = %s
                """,
                [order_id],
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return 0

    def get_orders_by_status(self, status):
        """Возвращает список заказов по их статусу."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM order WHERE status = %s
                """,
                [status],
            )
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                orders.append({
                    'id': row[0],
                    'user_id': row[1],
                    'created_timestamp': row[2],
                    'phone_number': row[3],
                    'requires_delivery': row[4],
                    'delivery_address': row[5],
                    'payment_on_get': row[6],
                    'is_paid': row[7],
                    'status': row[8],
                })
            return orders

    def get_orders_by_created_date(self, start_date, end_date):
        """Возвращает список заказов по дате создания."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM order WHERE created_timestamp BETWEEN %s AND %s
                """,
                [start_date, end_date],
            )
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                orders.append({
                    'id': row[0],
                    'user_id': row[1],
                    'created_timestamp': row[2],
                    'phone_number': row[3],
                    'requires_delivery': row[4],
                    'delivery_address': row[5],
                    'payment_on_get': row[6],
                    'is_paid': row[7],
                    'status': row[8],
                })
            return orders

    def get_most_popular_products(self):
        """Возвращает список самых популярных товаров (по количеству продаж)."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT oi.product_id, COUNT(*) AS count
                FROM order_item oi
                GROUP BY oi.product_id
                ORDER BY count DESC
                LIMIT 5;
                """,
            )
            rows = cursor.fetchall()
            popular_products = []
            for row in rows:
                popular_products.append({
                    'product_id': row[0],
                    'count': row[1],
                })
            return popular_products

    def get_average_order_value(self):
        """Возвращает среднюю стоимость заказа."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(oi.price * oi.quantity) AS average_order_value
                FROM order_item oi;
                """,
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return Decimal('0.00')

    def get_total_revenue(self):
        """Возвращает общую выручку."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT SUM(oi.price * oi.quantity) AS total_revenue
                FROM order_item oi;
                """,
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return Decimal('0.00')

    def get_orders_with_total_price(self):
        """Возвращает список заказов с их общей стоимостью."""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT o.*, SUM(oi.price * oi.quantity) AS total_price
                FROM order o
                JOIN order_item oi ON o.id = oi.order_id
                GROUP BY o.id
                ORDER BY o.created_timestamp;
                """,
            )
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                orders.append({
                    'id': row[0],
                    'user_id': row[1],
                    'created_timestamp': row[2],
                    'phone_number': row[3],
                    'requires_delivery': row[4],
                    'delivery_address': row[5],
                    'payment_on_get': row[6],
                    'is_paid': row[7],
                    'status': row[8],
                    'total_price': row[9],
                })
            return orders