from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItem, ShippingAddress

# Serializers convert objects into data types understandable by frontend frameworks (byte stream)

# This serializes all objects of User model
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True) # name of the user
    _id = serializers.SerializerMethodField(read_only=True) # unique id of the user
    isAdmin = serializers.SerializerMethodField(read_only=True) # admin status of the user

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin'] # fields to be serialized

    def get__id(self, obj): # function to get above mentioned "_id"
        return obj.id # obj is the instance of the User 

    def get_isAdmin(self, obj): # function to get above mentioned "admin status"
        return obj.is_staff

    def get_name(self, obj): # function to get above mentioned "name"
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


# This serializes all objects of User model with JSON Web Token
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True) # token for the user
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']
    
    def get_token(self, obj): # function that generates token for user
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


# This serializes all objects of Product model with all fields
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# This serializes all objects of Shipping Address model with all fields
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


# This serializes all objects of Order Item model with all fields
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


# This serializes all objects of Order model with nested objects of Order items and Shipping address
class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True) # all order items of the order
    shippingAddress = serializers.SerializerMethodField(read_only=True) # shipping address of the order
    user = serializers.SerializerMethodField(read_only=True) # user who created the order

    class Meta:
        model = Order
        fields = '__all__' # all fields of the order model

    def get_orderItems(self, obj): # function that returns all order items object associated to this instance of Order
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True) # Order Item serializer initialized above
        return serializer.data

    def get_shippingAddress(self, obj): # function that returns single shipping address associated to this instance of Order
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data # Shipping Address serializer initialized above
        except:
            address = False
        return address

    def get_user(self, obj): # function that returns details of the User who created the order
        user = obj.user
        serializer = UserSerializer(user, many=False) # User serializer initialized above
        return serializer.data