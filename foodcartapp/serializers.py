from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Product, Order, OrderItem
from rest_framework import serializers

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'price',
            'image',
            'special_status',
            'description',
            'objects'
        ]


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity'
        ]


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(
        many=True,
        allow_empty=False,
        allow_null=False,
        write_only=True,
    )
    phonenumber = PhoneNumberField(region="RU")

    class Meta:
        model = Order
        fields = [
            'id',
            'firstname',
            'lastname',
            'address',
            'phonenumber',
            'products'
        ]
        extra_kwargs = {
            'lastname': {'required': True},
            'address': {'required': True},
        }





