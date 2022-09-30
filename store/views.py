from sqlite3 import Timestamp
from django.shortcuts import render
from django.http import JsonResponse 
import json
import datetime

from .models import * 


# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False) #tries to query the customer to attach the order, if does not exist it created it and attaches order
        items = order.orderitem_set.all()      #asigna los items de la orden a items
        cartItems = order.get_cart_items
    else:
        #instructions when user is not logged in
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False} #shows 0 for cart total and cart items when user is not logged in
        cartItems = order['get_cart_items']
    
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}        #its used to pass data that its going to be shown in template
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False) #tries to query the customer to attach the order, if does not exist it created it and attaches order
        items = order.orderitem_set.all()      #asigna los items de la orden a items
        cartItems = order.get_cart_items
    else:
        #instructions when user is not logged in
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False} #shows 0 for cart total and cart items when user is not logged in
        cartItems = order['get_cart_items']
    
    context = {'items': items, 'order': order, 'cartItems': cartItems }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False) #tries to query the customer to attach the order, if does not exist it created it and attaches order
        items = order.orderitem_set.all()      #asigna los items de la orden a items
        cartItems = order.get_cart_items
    else:
        #instructions when user is not logged in
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False} #shows 0 for cart total and cart items when user is not logged in
        cartItems = order['get_cart_items']
    
    context = {'items': items, 'order': order, 'cartItems': cartItems }
    return render(request, 'store/checkout.html', context)

#edits quantity of items in checkout, adds and deletes items    
def updateItem(request):
    print("funciton started")
    data = json.loads(request.body) 
    productId = data['productId']
    action = data['action']
    
    #shows in console t
    print( 'Action:', action )
    print( 'productId:', productId   )
    print('checking')
    
    customer = request.user.customer 
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':  
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0 :
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False) 

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        #code to avoid user manipulation on the frontend
        if total == order.get_cart_total:
            order.complete = True 
        order.save()
        
        
        #if there is an order to be shipped, an address is created
        if order.shipping ==True:
            ShippingAddress.objects.create(
               customer = customer,
               order = order,
               address = data['shipping']['address'],
               city = data['shipping']['city'],
               state = data['shipping']['state'],
               zipcode = data['shipping']['zipcode'],
            )
    else:
        print('user is not logged in...')
    
    return JsonResponse('Payment submitted..', safe=False)