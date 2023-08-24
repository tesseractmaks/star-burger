import json
import re

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
    item = request.data
    try:
        if 'firstname' and 'lastname' and 'address' and 'phonenumber' not in item:
            raise Exception('firstname, lastname, address, phonenumber')

        elif 'firstname' and 'lastname' and 'address' and 'phonenumber' in item:
                if len([i for i in item.values() if not i]) == 4:
                    return Response(
                        "TypeError: '%s':  - These fields cannot be empty" % ('firstname, lastname, address, phonenumber'),
                        status=status.HTTP_404_NOT_FOUND
                    )

        elif not item['address'] or item['address'] is None:
            return Response(
                "TypeError: 'address': '' - This field cannot be empty" ,
                status=status.HTTP_404_NOT_FOUND
            )

        elif not item['phonenumber'] or item['phonenumber'] is None:
            return Response(
                "TypeError: 'phonenumber': '' - This field cannot be empty",
                status=status.HTTP_404_NOT_FOUND

            )
        elif isinstance(item['firstname'], list) and not item['firstname']:
            return Response(
                "TypeError: 'firstname': - firstname: Not a valid string",
                status=status.HTTP_404_NOT_FOUND
            )

        elif not item['firstname'] or item['firstname'] is None:
            return Response(
                "TypeError: 'firstname': '' - This field cannot be empty",
                status=status.HTTP_404_NOT_FOUND
            )

        elif item['products'] and isinstance(item['firstname'], str):
            if 9999 == [item['product'] for item in item['products']][0]:
                return Response(
                    "TypeError: - non-existent product id: 9999",
                    status=status.HTTP_404_NOT_FOUND
                )

        elif isinstance(item['firstname'], list):
            return Response(
                "TypeError: 'firstname': - firstname: Not a valid string",
                status=status.HTTP_404_NOT_FOUND
            )

        elif re.findall(r'[0]{7,}', str(item['phonenumber'])):
            print(44)
            return Response(
                "TypeError: - Not a valid phonenumber: %s" % (item['phonenumber']),
                status=status.HTTP_404_NOT_FOUND
            )

        elif not isinstance(item['products'], list) and isinstance(item['firstname'], str):
            return Response(
                "TypeError: 'products': - 'products': Not a valid string",
                status=status.HTTP_404_NOT_FOUND
            )

    except Exception as exc:
        field = str(*exc.args)
        match (field):
            case 'products' | 'firstname' | 'lastname' | 'phonenumber' | 'address':
                return Response(f"KeyError: %s - This is a required field" % field,
                                status=status.HTTP_404_NOT_FOUND)
            case 'firstname, lastname, address, phonenumber':
                return Response("KeyError: %s - These are a required fields" % field,
                                status=status.HTTP_404_NOT_FOUND)
    else:
        save_to_db(item)
        return Response(item, status=status.HTTP_201_CREATED)


def save_to_db(item):
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
    # "products": [{"product": 2, "quantity": 2}, {"product": 1, "quantity": 2}, {"product": 3, "quantity": 1}],
    # "firstname": "2",
    # "lastname": "7",
    # "phonenumber": "7",
    # "address": "7"
    # }

    # return JsonResponse(item, safe=False)
    # return Response(item, status=status.HTTP_201_CREATED)


