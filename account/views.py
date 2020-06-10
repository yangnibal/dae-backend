from django.shortcuts import render
from .models import User
from rest_framework import viewsets
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (action, api_view)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .sendemail import send_id, init_pw
import random

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def token_request(request):
        if user_requested_token() and token_request_is_warranted():
            new_token = Token.objects.create(user=request.user)
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial=True):
        instance = self.get_object()
        serializer = UserSerializer(instance ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user = User.objects.all()
        if request.user.is_superuser:
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)
        return Response("no superuser")

    @action(detail=False, list=True, methods=['GET'])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, list=True, methods=['POST'])
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(detail=False, list=True, methods=['POST'])
    def loginsuperuser(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_superuser:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response("not superuser")

    @action(detail=False, list=True, methods=['GET'])
    def logout(self, request):
        if not request.user.is_authenticated:
            print(request.user)
            return Response("Do not exits user")
        request.user.auth_token.delete()
        return Response("user token delete success")
    
    @action(detail=False, list=True, methods=['POST'])
    def duplicate(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            return Response("username already exist")
        except User.DoesNotExist:
            return Response("useable username")

    @action(detail=False, list=True, methods=['POST'])
    def find_password(self, request):
        user = User.objects.get(username=request.data['username'])
        serializer = UserUpdateSerializer(user)

    @action(detail=False, list=True, methods=['POST'])
    def findid(self, request):
        try:
            user = User.objects.get(name=request.data['name'], phone_number=request.data['phone_number'], email=request.data['email'])
            send_id(user.email, user.username, user.name)
            return Response("email sended")
        except User.DoesNotExist:
            return Response("incorrect info")

    @action(detail=False, list=True, methods=['POST'])
    def findpw(self, request):
        try:
            user = User.objects.get(username=request.data['username'], name=request.data['name'], phone_number=request.data['phone_number'], email=request.data['email'])
            possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            new_pw = ""
            for i in range(10):
                new_pw += random.choice(possible)
            
            init_pw(user.email, user.username, user.name, new_pw)
            request.data['password'] = new_pw
            serializer = UserUpdateSerializer(self.request.user, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response("email sended")
        except User.DoesNotExist:
            return Response("incorrect info")

    @action(detail=False, list=True, methods=['POST'])
    def deleteuser(self, request):
        user = User.objects.get(username=request.data['username'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, list=True, methods=['POST'])
    def getuserinfo(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response("no user exist")

    @action(detail=False, list=True, methods=['POST'])
    def finduser(self, request):
        user = User.objects.all()
        if request.data['name'] is not "":
            user = user.filter(name=request.data['name'])
        if request.data['username'] is not "":
            user = user.filter(username=request.data['username'])
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)