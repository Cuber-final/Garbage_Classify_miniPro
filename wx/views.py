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
        fb_dic = {"name": cate.tc_name, "pc_name": par_name}
        return Response(fb_dic)

    def post(self, request):
        """
        :param request: 包括用户名，垃圾名称/搜索内容,搜索方式为文本搜索
        :return: 返回查询的垃圾所属类别,暂时只保存查询成功的信息
        应当支持模糊搜索？
        """
        # 分为两种情景模式，游客与用户
        use_status = request.data['stat']
        sea_info = request.data["content"]
        if use_status == 'visitor':
            cate = TcCate()
            # 先检测是否存在当前垃圾的数据，没有则直接返回失败
            try:
                cate = TcCate.objects.get(tc_name=sea_info)
            except cate.DoesNotExist:
                return Response({'msg': '未找到任何信息', 'code': 0})
            cateName = cate.tc_name
            parent_cate = TcCate.objects.get(tc_id=cate.tc_parent_id)
            par_name = parent_cate.tc_name
            fb_msg = {'name': cateName, 'pc_name': par_name, 'msg': '查找结果如下', 'code': 1}
            return Response(fb_msg)
        else:
            username = request.data['username']
            user = TcUser.objects.get(username=username)
            userId = user.userId
            cate = TcCate()
            fb_msg = {'msg': '当前信息曾被查询过，可通过历史记录查看', 'code': 0}
            # 先检测是否存在当前垃圾的数据，没有则直接返回失败
            try:
                cate = TcCate.objects.get(tc_name=sea_info)
            except cate.DoesNotExist:
                return Response({'msg': '未找到任何信息', 'code': 0})
            # 若库内没有当前用户下与这个词条相关的记录，则可以添加搜索的记录
            history = TcSearch()
            try:
                history = TcSearch.objects.get(sea_info=sea_info, sea_user_id=userId)
            except history.DoesNotExist:
                cateId = cate.tc_id
                cateName = cate.tc_name
                parent_cate = TcCate.objects.get(tc_id=cate.tc_parent_id)
                par_name = parent_cate.tc_name
                TcSearch.objects.create(sea_info=sea_info, sea_way=0, sea_user_id=userId,
                                        sea_cate_id=cateId)
                fb_msg = {'name': cateName, 'pc_name': par_name, 'msg': '查找成功，结果如下', 'code': 1}
            return Response(fb_msg)


# 获取分类信息
class GetCates(APIView):
    def get(self, request):
        # 获取所有一级分类,将每一个数据打包成字典列表
        cate_set = []
        cates = TcCate.objects.all()
        for cate in cates:
            if cate.tc_parent_id == cate.tc_id:
                cate_dict = {"tcId": cate.tc_id, "tcName": cate.tc_name}
                cate_set.append(cate_dict)
                # json_dict = json.dumps(cate_dict, ensure_ascii=False) 不需要解析为json字符串
        return Response(cate_set)

    # 查询某一父类下的所有垃圾种类
    def post(self, request):
        cate_set = []
        parent_id = request.data["tcId"]
        cates = TcCate.objects.filter(tc_parent_id=parent_id).exclude(tc_id=parent_id)
        for cate in cates:
            cate_dict = {"tcId": cate.tc_id, "tcName": cate.tc_name}
            cate_set.append(cate_dict)
        return Response(cate_set)


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


# 查询当前用户的所有历史搜索记录
class GetHistory(APIView):
    def get(self, request):
        # username=request.data['username']
        username = 'userB'
        userId = TcUser.objects.get(username=username).userId
        sea_list = []
        sea_dict = {}
        infos = TcSearch.objects.filter(sea_user_id=userId)
        for info in infos:
            pid = TcCate.objects.get(tc_id=info.sea_cate_id).tc_parent_id
            pcName = TcCate.objects.get(tc_id=pid).tc_name
            sea_dict['seaInfo'] = info.sea_info
            sea_dict['pcName'] = pcName
            sea_list.append(sea_dict)
        return Response(sea_list)

    def post(self, request):
        username = request.data['username']
        userId = TcUser.objects.get(username=username).userId
        sea_list = []
        sea_dict = {}
        infos = TcSearch.objects.filter(sea_user_id=userId)
        for info in infos:
            pid = TcCate.objects.get(tc_id=info.sea_cate_id).tc_parent_id
            pcName = TcCate.objects.get(tc_id=pid).tc_name
            sea_dict['seaInfo'] = info.sea_info
            sea_dict['pcName'] = pcName
            sea_list.append(sea_dict)
        return Response(sea_list)


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
