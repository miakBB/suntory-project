from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_record, name="create_record"),  # 飲料記録の登録
    path("list/", views.list_records, name="list_records"),  # 飲料記録の閲覧
]