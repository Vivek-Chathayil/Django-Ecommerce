from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import json
import datetime
from .models import *
from .utils import cookieCart,cartData, guestOrder

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    products = Product.objects.all()
    categories = Category.objects.all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(price__lte=float(search_query) if search_query.replace('.', '').isdigit() else 0)
        )

    if category_filter:
        products = products.filter(category__id=category_filter)

    context = {
        'products': products,
        'categories': categories,
        'cartItems': cartItems,
        'search_query': search_query,
        'selected_category': category_filter
    }
    return render(request, 'eshop/store.html', context)


def cart(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'eshop/cart.html', context)


def checkout(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'eshop/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'delete':
        orderItem.quantity = 0
        orderItem.delete()
        return JsonResponse('Item was deleted', safe=False)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was updated', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    order.payment_method = 'Cash on Delivery'

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country'],
        )

    return JsonResponse('Order placed successfully! You will pay cash on delivery.', safe=False)


# Authentication Views
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('store') 
        else:
            messages.error(request, 'Invalid username or password')

    data = cartData(request)
    return render(request, 'eshop/login.html', {'cartItems': data['cartItems']})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        elif Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            Customer.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

    data = cartData(request)
    return render(request, 'eshop/register.html', {'cartItems': data['cartItems']})


def logout_view(request):
    logout(request)
    return redirect('store')


@login_required
def order_history(request):
    customer = request.user
    orders = Order.objects.filter(customer=customer, complete=True).order_by('-date_ordered')

    data = cartData(request)
    return render(request, 'eshop/order_history.html', {'orders': orders, 'cartItems': data['cartItems']})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('store')
    data = cartData(request)
    return render(request, 'eshop/product_detail.html', {'product': product, 'cartItems': data['cartItems']})
