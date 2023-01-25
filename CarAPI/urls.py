"""CarAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from brand.views import BrandViewSet
from model.views import ModelViewSet
from car.views import CarViewSet, CarAllViewSet
from user.views import UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r"brands", BrandViewSet, basename="brand")
router.register(r"models", ModelViewSet, basename="model")
router.register(r"cars/all", CarAllViewSet, basename="car")
router.register(r"cars", CarViewSet, basename="car")
router.register(r"user", UserView, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-user/", include("rest_framework.urls", namespace="rest_framework")),
    path("user/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
