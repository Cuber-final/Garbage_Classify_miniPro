from django.contrib import admin
from django.urls import path, include
from wx.views import showIndex
urlpatterns = [
    path('',showIndex.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('wx.urls', namespace='api')),
]
