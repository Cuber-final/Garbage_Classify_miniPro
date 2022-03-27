from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth import authenticate


class UserLogin(APIView):
    def post(self, request):
        data = request.data  # 要求请求方传递JSON格式
        username = data['user']
        password = data['psw']
        user = authenticate(request, username=username, password=password)
        fb_code = 0
        fb_msg = ['fail', 'success']
        if user:
            fb_code = 1
        # 若账号密码正确，则返回登陆成功的代码
        msg = fb_msg[fb_code]
        return Response({'fb_msg': msg})


class Register(APIView):
    def post(self, request):
        # 获取传递的参数
        data = request.data
        username = data['user']
        password = data['psw']
        fb_code = 1
        fb_msg = ['The user already exists', 'register success']
        # 先查询是否已有，没有再创建
        user = TcUser.objects.get(username=username)
        if user:
            fb_code = 0
        else:
            user = TcUser.objects.creat(
                username=username,
                password=password
            )
        msg = fb_msg[fb_code]
        return Response({'fb_msg': msg})


class theIndex(APIView):
    def get(self, request):
        return Response("hello world")


class showIndex(APIView):
    def get(self, request):
        print("redirect to index")
        return redirect("api:index")
