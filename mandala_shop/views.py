from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

# Import models
from mandala_shop.models import Category, Goods, Basket

# Import forms
from .forms import *


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            parent_object = Category.objects.get(slug=slug)
            return Category.get_children(parent_object)
        else:
            category = Category.objects.filter(parent=None)
            return category


class GoodsListView(ListView):
    model = Goods
    paginate_by = 3

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            goods_in_category = Goods.objects.filter(category__slug=slug).prefetch_related('category')
            return goods_in_category


class GoodsDetailView(DetailView):
    model = Goods
    context_object_name = 'goods'
    slug_url_kwarg = 'goods_slug'


    def get_context_data(self, **kwargs):
        object = kwargs.get('object')
        context = super().get_context_data(**kwargs)
        ingredients = object.ingredients.all().prefetch_related('category')
        context['ingredients'] = ingredients
        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mandala_shop/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'mandala_shop/login.html'


class BasketListView(ListView):
    model = Basket
    def get_queryset(self):
        user = self.request.user
        goods_in_category = Basket.objects.filter(user=user)
        return goods_in_category