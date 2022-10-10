"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('transfer_cart/', views.transfer_cart, name='transfer_cart'),
    path('add_item/', views.add_item, name='add_item'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('<slug:slug>/', views.CategoryListView.as_view(), name='subcategory_list'),
    path('<slug:slug>/g/', views.GoodsListView.as_view(), name='goods_list'),
    path('<slug:category_slug>/<slug:goods_slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )