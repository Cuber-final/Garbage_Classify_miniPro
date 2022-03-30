from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth import authenticate
from utils.portDict import *


# 用户登录功能
class UserLogin(APIView):
    def post(self, request):
        data = request.data  # 要求请求方传递JSON格式
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        fb_code = 0
        fb_msg = ['fail', 'success']
        if user:
            fb_code = 1
        # 若账号密码正确，则返回登陆成功的代码
        msg = fb_msg[fb_code]
        return Response({'fb_msg': msg})


# 用户注册
class Register(APIView):
    def post(self, request):
        # 获取传递的参数
        data = request.data
        username = data['username']
        password = data['password']
        fb_code = 0
        fb_msg = ['fail', 'success']
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


# 拍照识别
class CameraRec(APIView):
    def get(self, request):
        dic = {0: "str1", 1: "str2"}
        return Response(dic)


# 文字输入搜索垃圾所属种类
class TextSearch(APIView):
    def get(self, request):
        cate_name = "牙签"
        cate = TcCate()
        try:
            cate = TcCate.objects.get(tc_name=cate_name)
        except cate.DoesNotExist:
            return Response("the cate doesn't exist")
        parent_cate = TcCate.objects.get(tc_id=cate.tc_parent_id)
        par_name = parent_cate.tc_name
        fb_dic = {"name": cate.tc_name, "parent_name": par_name}
        return Response(fb_dic)

    def post(self, request):
        cate_name = request.data["name"]
        cate = TcCate()
        try:
            cate = TcCate.objects.get(tc_name=cate_name)
        except cate.DoesNotExist:
            return Response("the cate doesn't exist")
        parent_cate = TcCate.objects.get(tc_id=cate.tc_parent_id)
        par_name = parent_cate.tc_name
        fb_dic = {"name": cate.tc_name, "parent_name": par_name}
        return Response(fb_dic)


# 获取分类信息
class GetCates(APIView):
    def get(self, request):
        cate_dict = {}
        cates = TcCate.objects.all()
        for cate in cates:
            cate_name = cate.tc_name
            cate_id = cate.tc_id
            cate_dict[cate_id] = cate_name
        # json_dict = json.dumps(cate_dict, ensure_ascii=False) 不需要解析为json字符串
        return Response(cate_dict)

    # 查询某一父类下的所有垃圾种类
    def post(self, request):
        cate_dict = {}
        parent_id = request.data["id"]
        cates = TcCate.objects.filter(tc_parent_id=parent_id).exclude(tc_id=parent_id)
        for cate in cates:
            cate_name = cate.tc_name
            cate_id = cate.tc_id
            cate_dict[cate_id] = cate_name
        return Response(cate_dict)


# 添加分类信息
class AddCate(APIView):
    def post(self, request):
        fb_code = 0
        fb_msg = ['The cate already exists', 'add cate success']
        cate_name = request.data["cate_name"]
        parent_name = request.data["parent_name"]
        parent_id = PcIdentify(parent_name)
        # 先查询是否已有，没有再创建
        cate = TcCate()
        try:
            cate = TcCate.objects.get(tc_name=cate_name)
        except cate.DoesNotExist:
            fb_code = 1
            TcCate.objects.create(tc_name=cate_name, tc_parent_id=parent_id)
        msg = fb_msg[fb_code]
        return Response({'fb_msg': msg})


'''
-------------测试代码--------------
'''


# 用于测试django的命名空间机制
# 首页跳转
class theIndex(APIView):
    def get(self, request):
        return Response("hello world,this is the home page of my system")


class showIndex(APIView):
    def get(self, request):
        print("redirect to index")
        return redirect("api:index")


# 首次导入所有默认垃圾分类的数据
# 解析cate.json 下的所有数据写入数据库
class UtilApi(APIView):
    def get(self, request):
        InputCates()
        return Response("success add cate data")
