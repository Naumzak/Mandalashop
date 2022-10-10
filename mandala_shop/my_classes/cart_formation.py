import decimal
from django.contrib.auth.models import AnonymousUser
from mandala_shop.models import Cart, Goods
from abc import ABC, abstractmethod
from enum import Enum


class TypeCart(Enum):
    SESSION = 1
    MODEL = 2


class AbstractCartFormation(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_cart(self):
        pass

    @abstractmethod
    def update_cart(self, item, tare, quantity, price):
        pass

    @abstractmethod
    def delete_cart(self):
        pass

    @abstractmethod
    def save_cart(self):
        pass


class CartItemsUpdate:
    """
    This class allows you to update the cart.
    Cart is JSON and has the following format:
    {
    "total_cart_price": price,
    'items': {
        item1: {
            "type": {
                tare1: {
                    "quantity": count1,
                    "price": price1,
                    "total_price": price1*count1
                    },
                tare2: {
                    "quantity": 2,
                    "price": price2,
                    "total_price": price2*count2
                    }
                },
            "img": img_url
            "name": name}
        item2: {
            ...}
            }
        }
    """

    def __init__(self, cart, item, tare, quantity, price):
        self.cart = cart
        self.item = item
        self.tare = tare
        self.quantity = quantity
        self.price = price

    def add_item(self):
        items_dict = self.cart.get('items')
        if items_dict is None:
            items_dict = self.cart['items'] = {}
        item_detail = items_dict.get(self.item)
        dec_price = decimal.Decimal('.'.join(self.price.split(',')))
        if item_detail:
            if item_detail['type'].get(self.tare):
                tare_detail = item_detail['type'][self.tare]
                tare_detail['quantity'] += self.quantity
                tare_detail['total_price'] = str(dec_price * tare_detail['quantity'])
            else:
                item_detail['type'][self.tare] = {
                    'quantity': self.quantity,
                    'price': self.price,
                    'total_price': str(dec_price * self.quantity)
                }
        else:
            items_dict[self.item] = {
                'type':
                    {
                        self.tare: {
                            'quantity': self.quantity,
                            'price': self.price,
                            'total_price': str(dec_price * self.quantity)
                        }
                    },
                'img': str(Goods.objects.get(slug=self.item).get_image()),
                'name': Goods.objects.get(slug=self.item).name
            }

    def remove_item(self):
        info = self.cart['items'][self.item]['type'][self.tare]
        dec_price = decimal.Decimal('.'.join(info['price'].split(',')))
        if info and info['quantity'] > 1:
            info['quantity'] -= 1
            info['total_price'] = str(dec_price * info['quantity'])
        elif info and info['quantity'] == 1:
            self.delete_item()

    def delete_item(self):
        item = self.cart['items'][self.item]
        if item['type'][self.tare]:
            del item['type'][self.tare]
            if not item['type']:
                del item
            # self.cart_model.save()
        pass


class CartTotalPriceUpdate:

    def __init__(self, cart):
        self.cart = cart

    def update_total_cart_price(self):
        total_cart_price = decimal.Decimal('0.00')
        for key, item in self.cart['items'].items():
            if key != 'total_cart_price':
                for info in item['type'].values():
                    total_cart_price += decimal.Decimal('.'.join(info['total_price'].split(',')))
        self.cart['total_cart_price'] = str(total_cart_price)


class CartUpdate(CartItemsUpdate, CartTotalPriceUpdate):
    """
    This class update cart with total price
    """


class CartFormation(AbstractCartFormation, ABC):
    def __init__(self, request, type_cart: TypeCart):
        self.type_cart = type_cart
        self.request = request
        self.user = request.user
        if type_cart == TypeCart.MODEL:
            try:
                self.cart_model = Cart.objects.get(user=self.user)
                self.cart = self.cart_model.detail
            except:
                self.create_cart()
        elif type_cart == TypeCart.SESSION:
            self.session = request.session
            if not self.session.get('cart'):
                request.session['cart'] = {}

            self.cart = self.session['cart']

    def create_cart(self):
        if not isinstance(self.user, AnonymousUser) and not Cart.objects.filter(user=self.user):
            cart = Cart(user=self.user)
            cart.save()

    def update_cart(self, item, tare, quantity=0, price='0.00', delete=False):
        cart = CartUpdate(self.cart, item, tare, quantity, price)
        if delete:
            cart.delete_item()
        else:
            if quantity > 0:
                cart.add_item()
            elif quantity < 0:
                cart.remove_item()
        cart.update_total_cart_price()
        self.save_cart()

    def save_cart(self):
        if self.type_cart == TypeCart.MODEL:
            self.cart_model.save()
        if self.type_cart == TypeCart.SESSION:
            self.request.session.modified = True

    def delete_cart(self):
        user = self.request['user']
        if not isinstance(user, AnonymousUser) and Cart.objects.get(user=user):
            cart = Cart.objects.get(user=user)
            cart.delete()


class TransferData:
    def __init__(self, user):
        self.cart = Cart.objects.get(user=user)
        self.cart_field = self.cart.detail
        pass

    def add_data(self, data):
        TransferData.merge(self.cart_field, data)
        self.cart.save()

    @staticmethod
    def merge(d1, d2):
        for k in d2:
            if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
                TransferData.merge(d1[k], d2[k])
            else:
                d1[k] = d2[k]


class CartObject:
    def __init__(self, data):
        self.data = data

    def get_total_price(self):
        total_cart_price = self.data.get('total_cart_price', 0.00)
        return total_cart_price
