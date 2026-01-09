from django.urls import path
from . import views

urlpatterns = [
    path("", views.materials_home, name="materials-home"),
    path("list/", views.materials_list, name="materials-list"),
    path("create/", views.material_create, name="materials-create"),
    path("download/<int:pk>/", views.material_download, name="materials-download"),
]