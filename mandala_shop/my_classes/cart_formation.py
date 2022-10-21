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

    def __init__(self, cart):
        self.cart = cart

    def add_item(self, item, tare, quantity, price):
        items_dict = self.cart.get('items')
        if items_dict is None:
            items_dict = self.cart['items'] = {}
        item_detail = items_dict.get(item)
        dec_price = decimal.Decimal('.'.join(price.split(',')))
        if item_detail:
            if item_detail['type'].get(tare):
                tare_detail = item_detail['type'][tare]
                tare_detail['quantity'] += quantity
                tare_detail['total_price'] = str(dec_price * tare_detail['quantity'])
            else:
                item_detail['type'][tare] = {
                    'quantity': quantity,
                    'price': price,
                    'total_price': str(dec_price * quantity)
                }
        else:
            items_dict[item] = {
                'type':
                    {
                        tare: {
                            'quantity': quantity,
                            'price': price,
                            'total_price': str(dec_price * quantity)
                        }
                    },
                'img': str(Goods.objects.get(slug=item).get_image()),
                'name': Goods.objects.get(slug=item).name
            }

    def remove_item(self, item, tare):
        info = self.cart['items'][item]['type'][tare]
        dec_price = decimal.Decimal('.'.join(info['price'].split(',')))
        if info and info['quantity'] > 1:
            info['quantity'] -= 1
            info['total_price'] = str(dec_price * info['quantity'])
        elif info and info['quantity'] == 1:
            self.delete_item(item, tare)

    def delete_item(self, item_name, tare):
        item = self.cart['items'][item_name]
        if item['type'][tare]:
            del item['type'][tare]
            if not item['type']:
                del self.cart['items'][item_name]
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
        cart = CartUpdate(self.cart)
        if delete:
            cart.delete_item(item, tare)
        else:
            if quantity > 0:
                cart.add_item(item, tare, quantity, price)
            elif quantity < 0:
                cart.remove_item(item, tare)
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
