from django.shortcuts import render

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product
from django.contrib.auth.models import User
from base.serializers import ProductSerializer

from rest_framework import status


@api_view(['GET']) # api call with http method - GET
def getProducts(request): # function to get all the products from database (requires no authentication)
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) # serializes all products
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk): # function to get a product by id (requires no authentication)
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['POST']) # api call with http method - POST
@permission_classes([IsAdminUser]) # decorator that checks whether the user (who requests api call) is authenticated and admin or not
def createProduct(request): # function to create new product (by admin)
    user = request.user # user details of the admin
    # create a product with default initialization
    product = Product.objects.create(
        user = user,
        name = 'Sample Name',
        price = 0,
        brand = 'Sample Brand',
        countInStock = 0,
        category = 'Sample Category',
        description = ''
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT']) # api call with http method - PUT 
@permission_classes([IsAdminUser])
def updateProduct(request, pk): # function to update product by id
    data = request.data
    # get product by id
    product = Product.objects.get(_id=pk)
    # update the instance with data given by admin user
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE']) # api call with http method - DELETE
@permission_classes([IsAdminUser])
def deleteProduct(request, pk): # function to delete product by id
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product deleted')

@api_view(['POST'])
def uploadImage(request):
    data = request.data
    # get product_id from request
    product_id = data['product_id']
    # get product by id
    product = Product.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded')