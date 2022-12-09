from .base_page import BasePage
from .locators import MainPageLocators, BaseLocators


class MainPage(BasePage):
    def should_be_single_category_link(self):
        """
        Check, that guest can see card with category
        """
        assert self.elements_more_than(*MainPageLocators.SINGLE_CATEGORY_LINK, 3), "Category card link is not presented"
