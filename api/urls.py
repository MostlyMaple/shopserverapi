from django.urls import path
from . import views

urlpatterns = [
    path('', views.getClothes),
    path('create-item/', views.createItem),
]