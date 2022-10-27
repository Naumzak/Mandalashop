from django.test import TestCase
from decimal import Decimal
from mandala_shop.models import *
from .settings import ModelsSettings


class CategoryModelTest(ModelsSettings):
    def setUp(self):
        self.category = Category.objects.get(name='Coffee')

    def test_name_max_length(self):
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_slug_max_length(self):
        max_length = self.category._meta.get_field('slug').max_length
        self.assertEqual(max_length, 50)

    def test_check_children_1(self):
        children = self.category.get_children()
        self.assertEqual(bool(children), False)

    def test_check_children_2(self):
        category_2 = Category.objects.get(name='Drink')
        children_2 = category_2.get_children()
        self.assertEqual(bool(children_2), True)

    def test_get_absolute_url_category(self):
        self.assertEqual(self.category.get_absolute_url_category(), '/coffee/')

    def test_get_absolute_url_goods(self):
        self.assertEqual(self.category.get_absolute_url_goods(), '/coffee/g/')

    def test_get_image(self):
        self.assertEqual(self.category.get_image(), None)


class WeightModelTest(ModelsSettings):
    def test_type_weight_max_length(self):
        weight = Weight.objects.get(id=1)
        max_length = weight._meta.get_field('type_weight').max_length
        self.assertEqual(max_length, 50)


class GoodsModelTest(ModelsSettings):
    def setUp(self):
        self.category = Category.objects.get(name='Coffee')
        self.goods = Goods.objects.get(name='Black Coffee')

    def test_category(self):
        category = self.goods.category
        self.assertEqual(category, self.category)

    def test_category_set_null(self):
        self.category.delete()
        category = Goods.objects.get(id=1).category
        self.assertEqual(category, None)

    def test_name_max_length(self):
        max_length = self.goods._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_slug_max_length(self):
        max_length = self.goods._meta.get_field('slug').max_length
        self.assertEqual(max_length, 50)

    def test_description_max_length(self):
        max_length = self.goods._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_price(self):
        max_digits = self.goods._meta.get_field('price').max_digits
        decimal_places = self.goods._meta.get_field('price').decimal_places
        self.assertEqual(max_digits, 10)
        self.assertEqual(decimal_places, 2)

    def test_get_price_per_weight(self):
        weight_1 = Weight.objects.get(id=1)
        weight_2 = Weight.objects.get(id=2)
        right_result = {weight_1: Decimal(250.00), weight_2: Decimal(500.00)}
        self.assertEqual(self.goods.get_price_per_weight(), right_result)

    def test_get_min_price(self):
        self.assertEqual(self.goods.get_min_price(), Decimal(250.00))

    def test_get_absolute_url(self):
        goods = Goods.objects.get(id=1)
        self.assertEqual(goods.get_absolute_url(), '/coffee/black-coffee/')

    def test_get_image(self):
        goods = Goods.objects.get(id=1)
        self.assertEqual(goods.get_image(), None)


class DeliveryAddressModelTest(ModelsSettings):
    def test_first_name_max_length(self):
        delivery_address = DeliveryAddress.objects.get(id=1)
        max_length = delivery_address._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 30)

    def test_last_name_max_length(self):
        delivery_address = DeliveryAddress.objects.get(id=1)
        max_length = delivery_address._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 30)


class CartModelTest(ModelsSettings):
    def test_detail(self):
        cart = Cart.objects.get(user__first_name='TestUser')
        right_json = {'total_cart_price': 0, 'items': {}}
        self.assertEqual(cart.detail, right_json)
