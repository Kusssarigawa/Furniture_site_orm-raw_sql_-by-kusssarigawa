from django.db import connection
from django.shortcuts import render, get_object_or_404
from goods.models import Products
def get_goods_by_category(category_slug="all", page=1, discount=None, order_by=None, query=None):
    raw_sql = "SELECT product.id, product.name, product.slug, description, image, price, quantity, discount, category_id FROM product"
    params = []
    
    if category_slug and category_slug != "all":
        raw_sql += " JOIN category ON product.category_id = category.id"
        raw_sql += " WHERE category.slug = %s"
        params.append(category_slug)
    elif query:
        raw_sql = "SELECT product.id, product.name, product.slug, description, image, price, discount, quantity, category_id FROM product WHERE name LIKE %s"
        params.append(f'%{query}%')

    if discount:
        if "WHERE" in raw_sql:
            raw_sql += " AND discount > 0"
        else:
            raw_sql += " WHERE discount > 0"

    if order_by and order_by != "default":
        raw_sql += f" ORDER BY {order_by}"

    # Handling pagination
    # limit = 3
    # offset = (int(page) - 1) * limit
    # raw_sql += " LIMIT %s OFFSET %s"
    # params.extend([limit, offset])
    with connection.cursor() as cursor:
        cursor.execute(raw_sql, params)
        goods = dictfetchall(cursor)

    return goods
def get_product_by_slug(product_slug):
    raw_sql = "SELECT * FROM product WHERE slug = %s"
    params = [product_slug]

    with connection.cursor() as cursor:
        cursor.execute(raw_sql, params)
        product = dictfetchone(cursor)
        
    # product._prefetched_objects_cache = {'display_id': f"{product.id:05}"}
    return product

def dictfetchone(cursor):
    "Return one row from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row:
        data= dict(zip(columns, row))
        return Products(**data)
    return None

def product(request, product_slug):
    product = get_product_by_slug(product_slug)

    if not product:
        # Возвращаем 404, если продукт не найден
        return get_object_or_404(Products, slug=product_slug)

    context = {"product": product}

    return render(request, "goods/product.html", context=context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        Products(**dict(zip(columns, row)))
        for row in cursor.fetchall()
    ]
