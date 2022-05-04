from django.urls import path
from wx.views import *
from utils.useCamera import CameraRec
from utils.portDict import InputCates

app_name = 'api'

urlpatterns = [
    path('user/login', UserLogin.as_view(), name='login'),
    path('user/register', Register.as_view(), name='register'),
    path('search/camera', CameraRec.as_view(), name='camera'),
    path('search/getCates', GetCates.as_view(), name='getCates'),
    path('search/text', TextSearch.as_view(), name='text'),
    path('search/addCate', AddCate.as_view(), name='addCate'),
    path('user/history', GetHistory.as_view(), name='getHistory'),
    path('', theIndex.as_view(), name='index'),
    path('test', UtilApi.as_view(), name='show'),
    # path('update',InputCates())
]
