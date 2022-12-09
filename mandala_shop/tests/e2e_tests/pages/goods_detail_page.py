from .base_page import BasePage
from .locators import MainPageLocators, BaseLocators, GoodsDetailLocators

class GoodsDetailPage(BasePage):
    def should_be_product_image(self):
        """
        Check, that guest can see product image
        """
        assert self.is_element_present(*GoodsDetailLocators.IMAGE_PRODUCT_LINK), "Product image is not presented"

    def should_be_availability_status(self):
        """
        Check, that guest can see product image
        """
        assert self.is_element_present(*GoodsDetailLocators.AVAIBILITY_LINK), "availability status is not presented"

    def should_be_tare_selection(self):
        """
        Check, that guest can see tare selection
        """
        assert self.elements_more_than(*GoodsDetailLocators.TARE_LINK, 0), "Tare selection is not presented"

    def should_be_quantity(self):
        """
        Check, that guest can see quantity field
        """
        assert self.is_element_present(*GoodsDetailLocators.QUANTITY_FIELD_LINK), "quantity field is not presented"

    def should_be_button_add_to_cart(self):
        """
        Check, that guest can see button for add goods to cart
        """
        assert self.is_element_present(*GoodsDetailLocators.ADD_TO_CART_LINK), "Button for add goods to cart is not presented"

