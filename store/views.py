from django.shortcuts import render
from django.http import JsonResponse 
import json

from .models import * 


# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}        #its used to pass data that its going to be shown in template
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False) #tries to query the customer to attach the order, if does not exist it created it and attaches order
        items = order.orderitem_set.all()      #asigna los items de la orden a items
    else:
        #instructions when user is not logged in
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0} #shows 0 for cart total and cart items when user is not logged in
    
    context = {'items': items, 'order': order }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False) #tries to query the customer to attach the order, if does not exist it created it and attaches order
        items = order.orderitem_set.all()      #asigna los items de la orden a items
    else:
        #instructions when user is not logged in
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0} #shows 0 for cart total and cart items when user is not logged in
    
    context = {'items': items, 'order': order }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body) 
    productId = data['productId']
    action = data['action']
    
    print( 'Action:', action )
    print( 'productId:', productId   )
    
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