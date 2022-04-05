from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('', views.apiOverview),
    path('search/', views.search),
    path('create-item/', views.createItem),
    path('get-item/<str:pk>', views.getItem),
    path('update-item/<str:pk>', views.updateItem),
    path('delete-item/<str:pk>', views.deleteItem),
    path('users/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register', views.registerUser, name='register'),
    path('users/', views.getUsers, name='users'),
    path('users/profile', views.getUserProfile, name="user-profile"),
]