from django import forms
from django.db.models import Sum, F, Count, Value, Prefetch
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views


from foodcartapp.models import Product, Restaurant, Order, OrderItem, AllOrdersQuerySet


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })

import operator
@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    # all_orderss = Order.objects.prefetch_related("order_items__product", "order_items").all()
    all_orders = Order.objects.prefetch_related("order_items__product", "order_items").all_orders_total_prices()

    # x = all_orders.only("id").all()
    # print(all_orders)
    # print(all_orders.order_items.all())

    # for order in all_orders.filter(id__in=all_orders).prefetch_related("order_items__product", "order_items").all():
        # print(all_orders.get(id=products.id))
        # print(products.id)

    items =[
        {"total": int(str(order_items[0]["total"]).replace('None', '0')),
        "order_id": order_items[1].id,
        "firstname": order_items[1].firstname,
        "lastname": order_items[1].lastname,
        "address": order_items[1].address,
        "phonenumber": order_items[1].phonenumber} for order_items in all_orders]

    items.sort(key=operator.itemgetter("total"), reverse=True)



    # order_ = all_orders.get(id=order.id).order_items.all()
    # order_ = all_orders.filter(id__in=all_orders).prefetch_related("order_items__product", "order_items").all()
    #     order_ = order.order_items()
    # print(order_)



        # for item in order_items[1].order_items.all():
        # print(order_items[1])
        #     print(item.product.price, item.product.name, item.quantity, "|", order_items[1].id)



        # x = order.order_items.aggregate(total=Sum(F('quantity') * F('product__price'))).get("total")
        # x = order.order_items.aggregate(total=Sum(F('quantity') * F('product__price'))).get("total")
    # x = [order.order_items.aggregate(total=Sum(F('quantity') * F('product__price'))).get("total") for order in all_orders]

    # x = order_.annotate(total_cost=F('order_items__quantity') * F('order_items__product__price')).aggregate(total=Sum('total_cost')).get("total")

        # for i in x:
        #     print(i)
        # print(x, order['id'])
#     print(i.total_cost, order.id)
#     f = x.aggregate(total=Sum('total_cost'))
#     f = x.aggregate(total=Sum('total_cost')).get("total")

        # print('------')
        # print(order_items[0], order_items[1].id, '\n')
    # print(f, '\n')
    #     print(x, order.id, '\n')

        #     # print(i["total_cost"], " | ",  products.order_items.quantity, " | ")
        #     print(i)




    # all_orders_qry = OrderItem.objects.select_related("order").prefetch_related("product").all()
    # for i in all_orders_qry:
    #     print(i)

    # all_orders = Order.objects.with_total_prices().prefetch_related("items__product__menu_items__restaurant")
     #.filter(order__id=i.order.id)
    # print(all_orders)

    # collect_ids = [i.order.id for i in all_orders]
    # print(collect_ids)
    # all_orders = []

    # ----------------------
    # for i in all_orders_qry:
    # all_orders = all_orders_qry.all_orders_total_prices()
        # print(all_orders['total'], i.order.firstname)
    # print(all_orders)
    #

    # for t in all_orders:
    #
    #     for i in t:
    #         x = t.aggregate(total=Sum('total_cost'))
    #         print(x, i.order.id)

    #----------------------

    # all_orders.append(all_orders_.all_orders_query_set(i.order.id).annotate(
    #             total_cost=F('quantity') * F('product__price')) #.aggregate(total=Sum('total_cost')))
    # for i in all_orders:
    #     print(i['total'])

        # print(cost_order['total'])
        # print(i.quantity)
        # print(i['total'], '| quantity:',  i.items.quantity, 'firstname: ', i.order.firstname, 'order.id: ', i.order.id)



    # cost_order = Order.objects.items.all()


    # for i in all_orders:
    #     print(i)
    #     print('firstname: ', i.order.firstname, '| total_cost:', i.total_cost, '| quantity:',  i.quantity)


    return render(
        request,
        template_name='order_items.html',
        context={
            "order_items": items
        },
    )
