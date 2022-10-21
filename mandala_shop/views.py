from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

# Import Checkout
from cloudipsp import Api, Checkout

# Import models
from mandala_shop.models import Category, Goods, Cart, DeliveryAddress
from django.contrib.auth.models import AnonymousUser

# Import forms
from .forms import *

# My classes
from mandala_shop.my_classes.cart_formation import CartFormation, TransferData, TypeCart
from mandala_shop.my_classes.delivery_formation import DeliveryFormation, OrderFormation


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            """Send subcategory list"""
            parent_object = Category.objects.get(slug=slug)
            return Category.get_children(parent_object)
        else:
            """Send category list"""
            category = Category.objects.filter(parent=None)
            return category


class GoodsListView(ListView):
    model = Goods
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            goods_in_category = Goods.objects.filter(category__slug=slug).prefetch_related('category')
            return goods_in_category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = context['page_obj'].number
        return context


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
    success_url = reverse_lazy('transfer_cart')

    # auto login after register:
    def form_valid(self, form):
        """save the new user first"""
        form.save()
        """authenticate user then login"""
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
        login(self.request, user)
        cart = CartFormation(request=self.request, type_cart=TypeCart.MODEL)
        cart.create_cart()
        return redirect('category_list')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'mandala_shop/login.html'
    success_url = reverse_lazy('transfer_cart')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        user = form.get_user()
        transfer_cart = TransferData(user=user)  # If user has cart in session, transfer it to model
        data = self.request.session.get('cart', {})
        transfer_cart.add_data(data)
        return form_valid


class LogoutUser(LogoutView):
    form_class = AuthenticationForm
    template_name = 'mandala_shop/login.html'


def checkout(request):
    if request.method == "GET":
        """Open checkout template"""
        user = request.user
        context = {}
        if not isinstance(user, AnonymousUser):
            """
            We fill in the data for the order if the user is authorized
            and his data is saved
            """
            cart_data = Cart.objects.get(user=user).detail
            if DeliveryAddress.objects.get(user=user):
                context['data'] = DeliveryAddress.objects.get(user=user)
        else:
            cart_data = request.session.get('cart', {})
        cart_total_price = cart_data.get('total_cart_price', 0.00)
        context['total_cart_price'] = cart_total_price
        context['cart_data'] = cart_data
        return render(request, 'mandala_shop/checkout.html', context)
    if request.method == "POST":
        data = request.POST
        total_cart_price = data.get('total_cart_price')
        user = request.user
        cart_data = request.POST.get('cart_data', {})
        delivery_address = DeliveryFormation(data, user)
        delivery = delivery_address.create_delivery()  # Create delivery address model and save it
        order = OrderFormation(delivery_address=delivery, cart=cart_data)
        order.create_order()  # Create order model and save it
        request.session['total_cart_price'] = total_cart_price
        return redirect('payment')


def cart(request):
    if request.method == "GET":
        user = request.user
        if user.is_authenticated:
            cart = Cart.objects.get(user=user).detail
        else:
            cart = request.session.get('cart')
        context = {'cart': cart}
        return render(request, 'mandala_shop/cart.html', context)


def add_item(request):
    if request.method == "POST":
        if isinstance(request.user, AnonymousUser):
            type_cart = TypeCart.SESSION
        else:
            type_cart = TypeCart.MODEL
        cart = CartFormation(request, type_cart)
        item = request.POST.get('item')
        tare = request.POST.get('tare')
        quantity = request.POST.get('quantity')
        path = request.POST.get('path')
        price = request.POST.get('price')
        cart.update_cart(item, tare, int(quantity), price)
        return redirect(path)


def delete_item(request):
    if request.method == "POST":
        if isinstance(request.user, AnonymousUser):
            type_cart = TypeCart.SESSION
        else:
            type_cart = TypeCart.MODEL
        cart = CartFormation(request, type_cart)
        item = request.POST.get('item')
        tare = request.POST.get('tare')
        cart.update_cart(item, tare, delete=True)
        return redirect('cart')


def remove_item(request):
    if isinstance(request.user, AnonymousUser):
        type_cart = TypeCart.SESSION
    else:
        type_cart = TypeCart.MODEL
    if request.method == "POST":
        cart = CartFormation(request, type_cart)
        item = request.POST.get('item')
        tare = request.POST.get('tare')
        quantity = -1
        cart.update_cart(item, tare, quantity)
        return redirect('cart')


def transfer_cart(request):
    if request.method == "GET":
        user = request.user
        data = request.session.get('cart', {})
        cart = CartFormation(user, TypeCart.MODEL)
        cart.create_cart()
        transfer = TransferData(user)
        transfer.add_data(data)
        return redirect('cart')


def payment(request, *args, **kwargs):
    """Test payment api"""
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    total_cart_price = request.session.get('total_cart_price', 0)
    int_tcp = int(Decimal(total_cart_price)) * 100
    data = {
        "currency": "UAH",
        "amount": int_tcp
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)
