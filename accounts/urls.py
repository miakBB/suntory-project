from django.urls import path
from . import views


urlpatterns=[
    path('register/',views.register,name='register'),#認証機能
]