from django.urls import path
from wx.views import *

app_name = 'api'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/',Register.as_view(),name='register'),
    path('',theIndex.as_view(),name='index'),
    path('test/',showIndex.as_view(),name='show')
]
