# Generated by Django 3.2.15 on 2023-09-24 10:18

from django.db import migrations


def copy_prices_to_order_item(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    Product = apps.get_model('foodcartapp', 'Product')

    order_items = OrderItem.objects.all()
    for item in order_items.iterator():
        product_obj = Product.objects.get(id=item.product_id)
        item.price = product_obj.price
        # item.get_or_create(price=product_obj.price)
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0011_orderitem_price'),
    ]

    operations = [
        migrations.RunPython(copy_prices_to_order_item)
    ]
