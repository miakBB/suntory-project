from django.urls import path
from .views import register,mypage
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('register/',register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('mypage/',mypage,name='mypage'),
] 