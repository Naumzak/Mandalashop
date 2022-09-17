import decimal

from .models import Basket, Goods
from abc import ABC, abstractmethod


class AbstractBasketForm(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_item(self, item, tare, count, price):
        pass

    @abstractmethod
    def delete_item(self, item, tare):
        pass

    @abstractmethod
    def remove_item(self, item, tare):
        pass


class BasketAuthForm(AbstractBasketForm):
    def __init__(self, user):
        self.basket = Basket.objects.get(user=user)
        self.basket_field = self.basket.detail
        pass

    def add_item(self, item, tare, count, price):
        item_dict = self.basket_field.get(item)
        dec_price = decimal.Decimal('.'.join(price.split(',')))
        if item_dict:
            if item_dict['type'].get(tare):
                item_dict['type'][tare]['count'] += count
                item_dict['type'][tare]['total_price'] = str(dec_price * item_dict['type'][tare]['count'])
            else:
                item_dict['type'][tare] = {
                    'count': count,
                    'price': price,
                    'total_price': str(dec_price * count)
                }
        else:
            self.basket_field[item] = {'type': {
                tare: {
                    'count': count,
                    'price': price,
                    'total_price': str(dec_price * count)
                }
            },
                'img': str(Goods.objects.get(slug=item).image),
                'name': Goods.objects.get(slug=item).name
            }

        self.basket.save()

    def delete_item(self, item, tare):
        if self.basket_field[item]['type'][tare]:
            del self.basket_field[item]['type'][tare]
            if not self.basket_field[item]['type']:
                del self.basket_field[item]
            self.basket.save()
        pass

    def remove_item(self, item, tare):
        info = self.basket_field[item]['type'][tare]
        dec_price = decimal.Decimal('.'.join(info['price'].split(',')))
        if info and info['count'] > 1:
            info['count'] -= 1
            info['total_price'] = str(dec_price * info['count'])
        elif info and info['count'] == 1:
            self.delete_item(item, tare)
        self.basket.save()

class BasketAnonForm(AbstractBasketForm):
    def __init__(self, request):
        self.session = request.session
        if not self.session.get('basket'):
            request.session['basket'] = {}

        self.basket = self.session['basket']

    def add_item(self, item, tare, count, price):
        item_dict = self.basket.get(item)
        if item_dict:
            exiting_count = item_dict.get(tare)
            if exiting_count:
                self.session['basket'][item][tare] += count
            else:
                self.session['basket'][item][tare] = count
        else:
            self.session['basket'][item] = {tare: count}

    def delete_item(self, item, tare):
        if self.session['basket'][item][tare]:
            del self.session['basket'][item][tare]
            if not self.session['basket'][item]:
                del self.session['basket'][item]
        pass

    def remove_item(self, item, tare):
        if self.basket[item][tare] and self.basket[item][tare] > 1:
            self.basket[item][tare] -= 1
        elif self.basket[item][tare] and self.basket[item][tare] == 1:
            self.delete_item(item, tare)


class BasketForm(AbstractBasketForm):
    def __init__(self, request):
        self.request = request
        if request.user.is_authenticated:
            self.basket = BasketAuthForm(request.user)
        else:
            self.basket = BasketAnonForm(request)

    def add_item(self, item, tare, count, price):
        self.basket.add_item(item, tare, count, price)
        self.request.session.modified = True

    def delete_item(self, item, tare):
        self.basket.delete_item(item, tare)
        self.request.session.modified = True

    def remove_item(self, item, tare):
        self.basket.remove_item(item, tare)
        self.request.session.modified = True


class TransferData:
    def __init__(self, user):
        self.basket = Basket.objects.get(user=user)
        self.basket_field = self.basket.detail
        pass

    def add_data(self, data):
        TransferData.merge(self.basket_field, data)
        self.basket.save()

    @staticmethod
    def merge(d1, d2):
        for k in d2:
            if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
                TransferData.merge(d1[k], d2[k])
            else:
                d1[k] = d2[k]
