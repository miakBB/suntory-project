from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import get_dashboard_data


urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path("api/data/", get_dashboard_data, name="dashboard_data"),
] 