import json
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    # item = json.loads(request.body.decode())
    # item = request.body.decode()
    item = request.data
    try:
        match (item['products']):
            case str():
                return Response(
                    "TypeError: 'products': '%s' - string indices must be list" % item['products'],
                    status=status.HTTP_404_NOT_FOUND
                )
            case None:
                return Response(
                    "TypeError: 'products': '%s' - This field cannot be empty" % item['products'],
                    status=status.HTTP_404_NOT_FOUND
                )
            case []:
                return Response(
                    "TypeError: 'products': '%s' - List cannot be empty" % item['products'],
                    status=status.HTTP_404_NOT_FOUND
                )
    except:
        return Response("KeyError: 'products' - This is a required field",
                        status=status.HTTP_404_NOT_FOUND)
    else:
        order = Order.objects.create(
            firstname=item['firstname'],
            lastname=item['lastname'],
            address=item['address'],
            phonenumber=item['phonenumber'], )

        order_items = [
            OrderItem(
                order=order,
                product=Product.objects.get(id=fields['product']),
                quantity=fields['quantity'])
            for fields in item['products']]

        OrderItem.objects.bulk_create(order_items)

        # {
        #     "products": [{"product": 2, "quantity": 2}, {"product": 1, "quantity": 2}, {"product": 3, "quantity": 1}],
        #     "firstname": "2",
        #     "lastname": "7",
        #     "phonenumber": "7",
        #     "address": "7"
        # }

        # return JsonResponse(item, safe=False)
        return Response(item, status=status.HTTP_201_CREATED)
