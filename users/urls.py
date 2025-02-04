from django.urls import path
from .views import register, update, CustomLoginView


urlpatterns=[
    path('register/',register,name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('update/',update,name='update'),
] 