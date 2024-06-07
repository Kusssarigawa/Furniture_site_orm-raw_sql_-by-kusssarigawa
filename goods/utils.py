from goods.models import Products

def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    vector = ["name", "description"]

    names = [query,]
    qs = """MATCH({}) AGAINST('+{}*' IN BOOLEAN MODE)""".format(f"{vector[0]}, {vector[1]}", "* +".join(names))
    result = Products.objects.extra(where=[qs])

    return result
