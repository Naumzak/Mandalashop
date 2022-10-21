from django.urls import reverse
from django.test import TestCase

from mandala_shop.models import *
from .settings import ModelsSettings


class CategoryListViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        response = self.client.get(reverse('category_list'))
        first_category_object = response.context_data['category_list'].get(id=1)
        self.assertEqual(first_category_object, Category.objects.get(id=1))

    def test_template(self):
        response = self.client.get(reverse('category_list'))
        self.assertTemplateUsed(response, 'mandala_shop/category_list.html')


class SubcategoryListViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(reverse('subcategory_list', kwargs={'slug': 'drink'}))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('subcategory_list', kwargs={'slug': 'drink'}))
        self.assertTemplateUsed(response, 'mandala_shop/category_list.html')


class GoodsListViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(reverse('goods_list', kwargs={'slug': 'coffee'}))
        self.assertEqual(response.status_code, 200)

    def test_goods_list(self):
        response = self.client.get(reverse('goods_list', kwargs={'slug': 'coffee'}))
        goods_list = response.context_data['goods_list']
        goods_list_from_model = Goods.objects.filter(category__slug='coffee')
        for i in range(response.context_data['paginator'].per_page):
            """Check all goods on first page"""
            if i < len(goods_list):
                self.assertEqual(goods_list[i], goods_list_from_model[i])

    def test_template(self):
        response = self.client.get(reverse('goods_list', kwargs={'slug': 'coffee'}))
        self.assertTemplateUsed(response, 'mandala_shop/goods_list.html')


class GoodsDetailViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(
            reverse('goods_detail', kwargs={'category_slug': 'coffee', 'goods_slug': 'black-coffee'}))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(
            reverse('goods_detail', kwargs={'category_slug': 'coffee', 'goods_slug': 'black-coffee'}))
        self.assertTemplateUsed(response, 'mandala_shop/goods_detail.html')


class RegisterViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('register', ))
        self.assertTemplateUsed(response, 'mandala_shop/register.html')


class LoginViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'mandala_shop/login.html')


class LogoutViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class CartViewTest(ModelsSettings):
    def test_status_code(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('cart'))
        self.assertTemplateUsed(response, 'mandala_shop/cart.html')