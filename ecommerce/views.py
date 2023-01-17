from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import *
import json
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from .utils import getData,addCartElementsToDataBase

def store(request):
    # we get the order, carItems and Items
    data = getData(request)

    # we get the first 15 products and all the categories
    products = Product.objects.all()[:15]
    categories = Category.objects.all()

    context = {'products':products,'cartItems':data['cartItems'],'categories':categories}
    return render(request,'ecommerce/Store.html',context)

# This view shows all the products realted with a category
def productCategory(request,category):
    # we get the order, carItems and Items
    data = getData(request)

    categoryName = 'Categoria no encontrada'
    try:
        categoryFound = Category.objects.get(name=category)
        products = Product.objects.filter(category=categoryFound.id)
        categoryName = categoryFound.name
    except: #The category name does not exist
        products = []

    context = {'products':products,'cartItems':data['cartItems'], 'categoryName':categoryName}
    return render(request,'ecommerce/CategoryProduct.html',context)

# This view shows all info realted with the shopping cart
def cart(request):
    # we get the order, carItems and Items
    data = getData(request)
    
    context = {'cart':data['items'], 'order':data['order'], 'cartItems':data['cartItems']}
    print(data['items'])
    return render(request,'ecommerce/Cart.html',context)

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data = getData(request)
    if request.method == 'POST':
        try:
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            total = float(request.POST['total'])
        except:
            return render(request,'ecommerce/Checkout.html', {'error_message':'Algún campo esta vacío.','cart':data['items'], 'order':data['order'], 'cartItems':data['cartItems']})

        if address == '' or city == '' or state == '':
            return render(request,'ecommerce/Checkout.html', {'error_message':'Algún campo esta vacío.','cart':data['items'], 'order':data['order'], 'cartItems':data['cartItems']})

        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,is_completed=False)
        items = OrderItem.objects.filter(order=order)

        if total != order.get_cart_total:
            return render(request,'ecommerce/Checkout.html', {'error_message':'Los precios no coinciden. Por favor recarga la página.','cart':data['items'], 'order':data['order'], 'cartItems':data['cartItems']})

        if len(items) > 0:
            try:
                order.transaction_id = "trans_id"
                order.is_completed = True
                shoppingAdress = ShippingAddress.objects.create(customer=customer, order=order,address=address,city=city,state=state)
            except:
                return render(request,'ecommerce/Checkout.html', {'error_message':'Algo salió mal','cart':data['items'], 'order':data['order'], 'cartItems':data['cartItems']})

            order.save()
            shoppingAdress.save()

            # process the payment with paypal or any other payment tool and redirect to idnex
            return redirect('index')
        else:
            return render(request,'ecommerce/Checkout.html',{'error_message':'El carrito de compras no tiene elementos.', 'cart':data['items'], 'order':data['order'], 'cartItems':data['cartItems'] })

    else:
        return render(request,'ecommerce/Checkout.html',{'error_message':'', 'cart':data['items'], 'order':data['order'], 'cartItems':data['cartItems'] })

# this view delates an element of the shopping cart.
def deleteItem(request):
    data = json.loads(request.body)
    try:
        productID = data['productID']
    except: # the productID is not present in the send data
        productID = -1

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productID)
        order, created = Order.objects.get_or_create(customer=customer,is_completed=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
        orderItem.delete()
    else:
        # if the user is a no authenticated user we use a cart that is saved in sessions
        cart = request.session.get('cart', {})        
        if productID in cart:
            del cart[productID]
        request.session['cart'] = cart
        
    return JsonResponse('The element was deleted from the cart', safe=False)

def updateItem(request):
    data = json.loads(request.body)

    try:
        productID = data['productID']
        action = data['action']
    except: # the productID and action is not present in the send data
        return JsonResponse('Some thing went wrong', safe=False)

    valueToAdd = -1

    if action == 'add':
        valueToAdd = 1

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            product = Product.objects.get(id=productID)
            order, created = Order.objects.get_or_create(customer=customer,is_completed=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

            orderItem.quantity += valueToAdd

            if orderItem.quantity <= 0:
                orderItem.delete()
            else:
                orderItem.save()

        except:
            return JsonResponse('Something went wrong', safe=False)
    else:
        try:
            cart = request.session.get('cart', {})
            product = Product.objects.get(id=productID)

            if productID in cart:
                cart[productID]['quantity'] += valueToAdd
                cart[productID]['total'] = cart[productID]['price'] * float(cart[productID]['quantity'])
            else:
                cart[productID] = {
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'quantity':1,
                    'imageURL':product.imageURL,
                    'total': product.price,
                }
            
            if cart[productID]['quantity'] <= 0:
                del cart[productID]
            request.session['cart'] = cart
        except:
            return JsonResponse('Something went wrong', safe=False)
    
    return JsonResponse('Successful operation', safe=False)


def registerView(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
        except:
            username = ''
            email = ''
            password = ''
            password2 = ''

        if username == '' or email == '' or password == '' or password2 == '':
            return render(request,'ecommerce/login_Register.html',{'error_message':'Algun campo está vaciío.','flag':'register'})
        
        if password2 != password:
            return render(request,'ecommerce/login_Register.html',{'error_message':'Las contraseñas no coinciden','flag':'register'})

        if len(password)<8:
            return render(request,'ecommerce/login_Register.html',{'error_message':'La contraseña debe de contener al menos 8 caracteres','flag':'register'})
        
        try:
            user = User.objects.get(email=email)
        except:
            user = None           

        if user is not None:
            return render(request,'ecommerce/login_Register.html',{'error_message':'El correo ingresado ya ha sido tomado','flag':'register'})
        
        try:
            user = User.objects.get(username=username.lower())
        except:
            user = None

        if user is not None:
            return render(request,'ecommerce/login_Register.html',{'error_message':'El nombre de usuario ingresado ya ha sido tomado','flag':'register'})
        

        user = User.objects.create_user(username=username.lower(), email=email, password=password)
        user.save()
        customer = Customer.objects.create(user=user,name=username.lower(),email=email)
        customer.save()
        # if the session cart has elements we add those elements in the orde
        addCartElementsToDataBase(request,customer)
        login(request, user)
        return redirect('index')
    else:
        return render(request,'ecommerce/login_Register.html',{'error_message':'','flag':'register'})

def loginView(request):
    flag = 'login'
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            username = ''
            password = ''

        user = authenticate(request, username=username.lower(), password=password)
        customer = Customer.objects.get(user=user)
        if user is not None:
            # if the session cart has elements we add those elements in the orde
            addCartElementsToDataBase(request,customer)
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'ecommerce/login_Register.html', {'error_message': 'Contraseña o nombre de usuario incorrectos','flag':flag})
    else:
        return render(request,'ecommerce/login_Register.html',{'error_message':'','flag':flag})

def logout_view(request):
    logout(request)
    return redirect('index')