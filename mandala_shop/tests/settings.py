from django.test import TestCase
from decimal import Decimal
from mandala_shop.models import *


class ModelsSettings(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create base models for testing
        """
        Category.objects.create(name='Drink',
                                image=None,
                                slug='drink',
                                parent=None)
        Category.objects.create(name='Coffee',
                                image=None,
                                slug='coffee',
                                parent=Category.objects.get(name='Drink'))
        Weight.objects.create(weight=50, type_weight='ml')
        Weight.objects.create(weight=100, type_weight='ml')
        goods_1 = Goods.objects.create(
            category=Category.objects.get(name='Coffee'),
            name='Black Coffee',
            slug='black-coffee',
            image=None,
            description='Some description',
            price=5.00,
            hot=True,
            available=True
        )
        goods_2 = Goods.objects.create(
            category=Category.objects.get(name='Coffee'),
            name='White Coffee',
            slug='white-coffee',
            image=None,
            description='Some description',
            price=5.00,
            hot=False,
            available=True
        )
        weight_1 = Weight.objects.get(id=1)
        weight_2 = Weight.objects.get(id=2)
        goods_1.weight.add(weight_1, weight_2)
        goods_2.weight.add(weight_1, weight_2)
        user_1 = User.objects.create_user('TestUser', 'TestUser@email.com', '12345')
        Cart.objects.create(user=user_1)
        DeliveryAddress.objects.create(
            user=user_1,
            first_name='first_name',
            last_name='last_name',
            email='test@email.com',
            city='city',
            department_number='01',
            phone='0500550050'
        )
