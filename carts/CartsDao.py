from django.db import connection
from django.shortcuts import render, get_object_or_404
from goods.models import Products
from django.utils import timezone

def execute_raw_sql(query, params):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor

def fetchall_raw_sql(query, params):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def fetchone_raw_sql(query, params):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else None

def get_product_by_id(product_id):
    query = "SELECT * FROM product WHERE id = %s"
    return fetchone_raw_sql(query, [product_id])

def get_cart_by_user_and_product(user_id, product_id):
    query = "SELECT * FROM cart WHERE user_id = %s AND product_id = %s"
    return fetchone_raw_sql(query, [user_id, product_id])

def get_cart_by_session_and_product(session_key, product_id):
    query = "SELECT * FROM cart WHERE session_key = %s AND product_id = %s"
    return fetchone_raw_sql(query, [session_key, product_id])

def create_cart(user_id, session_key, product_id, quantity):
    query = "INSERT INTO cart (user_id, session_key, created_timestamp, product_id, quantity) VALUES (%s, %s, %s, %s, %s)"
    created_timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    execute_raw_sql(query, [user_id, session_key, created_timestamp, product_id, quantity])

def update_cart_quantity(cart_id, quantity):
    query = "UPDATE cart SET quantity = %s WHERE id = %s"
    execute_raw_sql(query, [quantity, cart_id])

def get_cart_by_id(cart_id):
    query = "SELECT * FROM cart WHERE id = %s"
    return fetchone_raw_sql(query, [cart_id])

def delete_cart(cart_id):
    query = "DELETE FROM cart WHERE id = %s"
    execute_raw_sql(query, [cart_id])