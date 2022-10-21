import json

from mandala_shop.my_classes.cart_formation import CartItemsUpdate
from mandala_shop.models import Goods
from .settings import ModelsSettings
from . import json_results


class CartItemsUpdateTest(ModelsSettings):
    def setUp(self) -> None:
        self.cart = {}
        self.test_cart_object = CartItemsUpdate(cart=self.cart)
        self.item_1 = Goods.objects.get(id=1)
        self.item_2 = Goods.objects.get(id=2)
        self.tare_1 = str(self.item_1.weight.select_related()[0])
        self.tare_2 = str(self.item_1.weight.select_related()[1])

    def test_add_item(self):
        self.test_cart_object.add_item(self.item_1.slug, self.tare_1, 5, '50.00')
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_add_item_1_json())

        self.test_cart_object.add_item(self.item_1.slug, self.tare_1, 10, '50.00')
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_add_item_2_json())

        self.test_cart_object.add_item(self.item_1.slug, self.tare_2, 5, '50.00')
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_add_item_3_json())

        self.test_cart_object.add_item(self.item_1.slug, self.tare_2, 10, '50.00')
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_add_item_4_json())

        self.test_cart_object.add_item(self.item_2.slug, self.tare_1, 5, '50.00')
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_add_item_5_json())

    def test_delete_item(self):
        """ Filling the cart"""
        self.test_cart_object.add_item(self.item_1.slug, self.tare_1, 5, '50.00')
        self.test_cart_object.add_item(self.item_1.slug, self.tare_2, 5, '50.00')
        self.test_cart_object.add_item(self.item_2.slug, self.tare_1, 5, '50.00')

        """Do tests"""
        self.test_cart_object.delete_item(self.item_1.slug, self.tare_2)
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_delete_item_1_json())

        self.test_cart_object.delete_item(self.item_1.slug, self.tare_1)
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_delete_item_2_json())

        self.test_cart_object.delete_item(self.item_2.slug, self.tare_1)
        self.assertJSONEqual(json.dumps(self.cart), {'items': {}})

    def test_remove_item(self):
        """ Filling the cart"""
        self.test_cart_object.add_item(self.item_1.slug, self.tare_1, 2, '50.00')
        self.test_cart_object.add_item(self.item_2.slug, self.tare_1, 1, '50.00')

        """Do tests"""
        self.test_cart_object.remove_item(self.item_1.slug, self.tare_1)
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_remove_item_1_json())

        self.test_cart_object.remove_item(self.item_2.slug, self.tare_1)
        self.assertJSONEqual(json.dumps(self.cart), json_results.test_remove_item_2_json())

        self.test_cart_object.remove_item(self.item_1.slug, self.tare_1)
        self.assertJSONEqual(json.dumps(self.cart), {'items': {}})
