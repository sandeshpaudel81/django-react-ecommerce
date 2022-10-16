from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from base.serializers import UserSerializer, UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer): # class that returns user with token
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView): # function to login the user
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST']) # api call with http request - POST
def registerUser(request): # function to register user
    # getting user details from request
    data = request.data
    try:
        # creating new User
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False) # serializes above created User object with token
        return Response(serializer.data)
    except:
        # if new User object is failed to create
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT']) # api call with http request - PUT
@permission_classes([IsAuthenticated]) # function decorator to check whether the requesting user is authenticated or not
def updateUserProfile(request): # function to update profile of the user (requested by User himself)
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    # updating user details
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])
    # saving user object
    user.save()
    
    return Response(serializer.data)


@api_view(['GET']) # api call with http request - GET
@permission_classes([IsAuthenticated]) # function decorator to check whether the requesting user is authenticated or not
def getUserProfile(request): # funtion to get profile of a user
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAdminUser]) # function decorator to check whether requesting user is authenticated and admin or not
def getUsers(request): # function to get all users in the database
    # getting all users
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['DELETE']) # api call with http request - DELETE
@permission_classes([IsAdminUser])
def deleteUser(request, pk): # function to delete user by id
    # getting user by id
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')
    


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk): # function to get details of a user by id
    # getting user by id
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT']) # api call with http request - PUT
@permission_classes([IsAdminUser])
def updateUser(request, pk): # function to update user by id
    # getting user by id
    user = User.objects.get(id=pk)
    # getting data from request and updating
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    
    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)