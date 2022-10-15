from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from base.models import Product, Order, OrderItem, ShippingAddress #importing all models
from base.serializers import OrderSerializer # importing serializer from serializers.py

from rest_framework import status
from datetime import datetime

@api_view(['POST']) # api call with http method - POST
@permission_classes([IsAuthenticated]) # decorator that checks whether the user (who requests api call) is authenticated or not
def addOrderItems(request): # function to create new order and add order items to that order
    user = request.user # get user who requests
    data = request.data # get data from frontend

    orderItems = data['orderItems'] # access order items from data
    # check if the data has at least one order item or not
    if orderItems and len(orderItems)==0: # if there are no order items
        return Response({'detail':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else: 

        # (1) Create order object
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice'],
        )

        # (2) Create shipping address object
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        # (3) Create orderItem objects and set order to orderItems relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )
            # (4) Update countInStock of product
            product.countInStock -= item.qty
            product.save()
        serializer = OrderSerializer(order, many=False) # serializes Order along with all order items and shipping address
        return Response(serializer.data)


@api_view(['GET']) # api call with http method - GET
@permission_classes([IsAuthenticated])
def getOrderById(request, pk): # function to get order details using passed id
    user = request.user

    try:
        # get order from database - using id
        order = Order.objects.get(_id=pk)
        # check whether the requesting user is authorized to view or not (only admin and user who placed that order can access that order)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False) # serializes Order along with all order items and shipping address
            return Response(serializer.data)
        else:
            # response if the requesting user is not authorized to view
            Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        # response if the order is not found in database
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request): # function to get all his orders by a user
    user = request.user # user who requests this function
    orders = user.order_set.all() # all orders of requesting user
    serializer = OrderSerializer(orders, many=True) # serializes all orders along with all order items and shipping address of each order
    return Response(serializer.data)

    

@api_view(['PUT']) # api call with http method - PUT
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk): # function to update payment status of the order (accessed by id) to PAID after payment is successful
    order = Order.objects.get(_id=pk) # get order by its id
    # update isPaid boolean field to True
    order.isPaid = True 
    # update paidAt field by current date and time
    order.paidAt = datetime.now()
    order.save() # save the object

    return Response('Order was paid')



