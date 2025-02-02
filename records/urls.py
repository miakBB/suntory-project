from django.urls import path
from . import views
from .views import list_records, get_weekly_data

urlpatterns = [
    path("create/", views.create_record, name="create_record"),  # 飲料記録の登録
    path("list/", list_records, name="list_records"), # 飲料記録の閲覧
    path("api/weekly/", get_weekly_data, name="get_weekly_data"),
]