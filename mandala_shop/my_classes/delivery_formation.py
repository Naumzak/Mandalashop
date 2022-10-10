import json

from mandala_shop.models import Order, DeliveryAddress, Cart
from django.contrib.auth.models import AnonymousUser


class DeliveryForm:
    def __init__(self, data, user):
        if isinstance(user, AnonymousUser):
            self.user = None
        else:
            self.user = user
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.city = data.get('city')
        self.department_number = data.get('department_number')
        self.phone = data.get('phone')

    def create_delivery(self):
        if DeliveryAddress.objects.filter(user=self.user) and self.user:
            existing_delivery_address = DeliveryAddress.objects.get(user=self.user)
            existing_delivery_address.first_name = self.first_name
            existing_delivery_address.last_name = self.last_name
            existing_delivery_address.email = self.email
            existing_delivery_address.city = self.city
            existing_delivery_address.department_number = self.department_number
            existing_delivery_address.phone = self.phone
            existing_delivery_address.save()
            return existing_delivery_address
        else:
            delivery = DeliveryAddress(
                user=self.user,
                first_name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                city=self.city,
                department_number=self.department_number,
                phone=self.phone
            )
            delivery.save()
            return delivery


class OrderFormation:
    def __init__(self, delivery_address: DeliveryForm, cart: dict):
        self.delivery_address = delivery_address
        self.cart = cart

    def create_order(self):
        order = Order(delivery_address=self.delivery_address, cart=self.cart)
        order.save()