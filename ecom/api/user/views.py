from ast import Try
from functools import cache
from warnings import catch_warnings
from xml.parsers import expat
from django.shortcuts import render
import random
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .serializers import serializers
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import re


def generate_session_token(lenght=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(lenght))


@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'Error': 'send a POST request'})

    username = request.POST['email']
    password = request.POST['password']

    if not re.match("\b[\w\.-]+@[\w\.-] +\.\w{2, 4}\b", username):
        return JsonResponse({'Error': 'Enter a valid Email'})

    if len(password) < 3:
        return JsonResponse({'Error': 'password needs to be atleat 3 char'})

    userModel = get_user_model()

    try:
        user = userModel.objects.get(email=username)

        if user.check_password(password):
            user_dic = userModel.objects.filter(
                email=username).values().first()
            user_dic.pop('password')

            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({'Error': 'previus session exists !'})

            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': user_dic})
        else:
            return JsonResponse({'Error': 'invalid password'})

    except userModel.DoesNotExist:
        return JsonResponse({'Error': 'invalide email'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserViewSetzer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except keyError:
            return [permission() for permission in self.permission_classes]
