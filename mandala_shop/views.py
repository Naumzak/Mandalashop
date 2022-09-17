from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from cloudipsp import Api, Checkout

# Import models
from mandala_shop.models import Category, Goods, Basket

# Import forms
from .forms import *

# My classes
from .basket_formation import BasketForm, TransferData


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
    success_url = reverse_lazy('transfer_basket')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'mandala_shop/login.html'
    success_url = reverse_lazy('transfer_basket')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        user = form.get_user()
        transfer_basket = TransferData(user=user)
        data = self.request.session.get('basket', {})
        transfer_basket.add_data(data)
        return valid_form


class LogoutUser(LogoutView):
    form_class = AuthenticationForm
    template_name = 'mandala_shop/login.html'


def basket(request):
    if request.method == "GET":
        user = request.user
        if user.is_authenticated:
            basket = Basket.objects.get(user=user).detail
        else:
            basket = request.session.get('basket')
        context = {'basket': basket}
        return render(request, 'mandala_shop/cart.html', context)


def add_item(request):
    if request.method == "POST":
        basket = BasketForm(request)
        item = request.POST.get('item')
        tare = request.POST.get('tare')
        count = request.POST.get('count')
        path = request.POST.get('path')
        price = request.POST.get('price')
        basket.add_item(item, tare, int(count), price)
        return redirect(path)


def delete_item(request):
    if request.method == "POST":
        basket = BasketForm(request)
        item = request.POST.get('item')
        tare = request.POST.get('tare')
        basket.delete_item(item, tare)
        return redirect('basket')


def remove_item(request):
    if request.method == "POST":
        basket = BasketForm(request)
        item = request.POST.get('item')
        tare = request.POST.get('tare')
        basket.remove_item(item, tare)
        return redirect('basket')


def transfer_basket(request):
    if request.method == "POST":
        user = request.user
        data = request.session.get('basket', {})
        transfer = TransferData(user)
        transfer.add_data(data)
        return redirect('basket')

def payment(request):

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": 10000
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)