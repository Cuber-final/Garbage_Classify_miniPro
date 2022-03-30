from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth import authenticate
from utils.portDict import InputCates


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
        fb_code = 0
        fb_msg = ['The user already exists', 'register success']
        # 先查询是否已有，没有再创建
        try:
            user = TcUser.objects.get(username=username)
        except TcUser.DoesNotExist:
            fb_code = 1
            # 信息不存在报异常，在此处处理添加用户，使用下面注释的方法只会存储明文的密码不会加密，我的理解是
            '''
            
            newUser = TcUser()
            newUser.username = username
            newUser.password = password
            newUser.save()
            '''
            TcUser.objects.create_user(username=username, password=password)
        msg = fb_msg[fb_code]
        return Response({'fb_msg': msg})


class theIndex(APIView):
    def get(self, request):
        return Response("hello world,this is the home page of my system")


class showIndex(APIView):
    def get(self, request):
        print("redirect to index")
        return redirect("api:index")


class utilApi(APIView):
    def get(self, request):
        InputCates()
        return Response("success add cate data")
