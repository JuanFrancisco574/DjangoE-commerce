from .models import *
from django.contrib.sessions.models import Session

def getData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,is_completed=False)
        items = OrderItem.objects.filter(order=order)
        cartItems = order.get_cart_items
    else:
        cart = request.session.get('cart', {})
        order = {'get_cart_total':0,'get_cart_items':0}
        items = []

        for c in cart:
            order['get_cart_total'] += cart[c]['price'] * cart[c]['quantity']
            order['get_cart_items'] += cart[c]['quantity']
            items.append( cart[c] )

        cartItems = order['get_cart_items']

    return {'order':order,'items':items, 'cartItems':cartItems}


def addCartElementsToDataBase(request,customer):
    # if the session cart has elements we add those elements in the orde
    cart = request.session.get('cart', {})
    order, created = Order.objects.get_or_create(customer=customer,is_completed=False)
    productFound = None
    for c in cart:
        try:
            productFound = Product.objects.get(id=cart[c]['id'])
        except:
            productFound = None
                
        if productFound is not None:
            orderItem, created = OrderItem.objects.get_or_create(order=order,product=productFound, defaults={'quantity':cart[c]['quantity']})

    request.session['cart'] = {}


