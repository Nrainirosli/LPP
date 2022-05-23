from datetime import datetime, timedelta
from django.shortcuts import render,  redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from sensor.models import *
from django.conf import settings
from io import BytesIO
from django.core.files import File
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login1(request):
    print("zzzz")  
    username = request.data.get("username")
    password = request.data.get("password")
    print(username)
    # return Response({'username':username},
    #                 status=HTTP_200_OK)
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    user2 = AuthUser.objects.get(username=username)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    userid = user.id

    role = user2.role.level 
    print(role)
    is_staff = user.is_staff
    is_superuser = user.is_superuser
    username = user.username
    # print(is_superuser)
    email = user.email
    content = {
        'token': token.key, 
        'userid': userid, 
        'is_superuser': is_superuser,
        'username': username,
        'is_staff': is_staff,
        'role': role,
        'email': email,
    }
    return Response(content,
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login2(request):
    parser_classes = [MultiPartParser]
    username = request.data.get("username")
    password = request.data.get("password")
    content = {
        'result': 'success'
    }
    return Response(content,status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def sample_api(request,id):
    data = {'sample_data': id, 'data': 1234}
    return Response(data, status=HTTP_200_OK)
