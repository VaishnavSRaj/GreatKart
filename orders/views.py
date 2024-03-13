import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from cart.models import CartItem
from orders.forms import OrderForm
from .models import Payment
from .models import Order, OrderedProduct
import datetime


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )
    payment = Payment()
    payment.user = request.user
    payment.payment_id = body["transID"]
    payment.payment_method = body["payment_method"]
    payment.amount_paid = order.order_total
    payment.status = body["status"]
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    # move the cart items to the ordered product table
    cart_items = CartItem.objects.filter(user=request.user)
    
    for item in cart_items:
        print(item)
        ordered_product = OrderedProduct()
        ordered_product.order_id = order.id
        ordered_product.payment = payment
        ordered_product.user_id = request.user.id
        ordered_product.product_id = item.product_id
        ordered_product.quantity = item.quantity
        ordered_product.product_price = item.product.price
        ordered_product.ordered = True
        ordered_product.save()
    return render(request, "orders/payment.html")


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)
    count = cart_item.count()

    if count <= 0:
        return redirect("store")

    grandtotal = 0
    tax = 0

    for item in cart_item:
        total += item.product.price * item.quantity
        quantity += item.quantity

    tax = (2 * total) / 100
    grandtotal = tax + total

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grandtotal
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, dt, mt)
            current_date = d.strftime("%Y%d%m")
            order_id = current_date + str(data.id)
            data.order_number = order_id
            data.save()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_id
            )
            context = {
                "order": order,
                "cart_items": cart_item,
                "grandtotal": grandtotal,
                "tax": tax,
            }

            return render(request, "orders/payment.html", context)
        else:
            return HttpResponse(form.errors)  # Corrected indentation here
    else:
        return render(request, "store/cart/checkout.html")


# Make sure you have the necessary imports at the beginning of your file.
