from .operations import Operations
from .locators import BaseLocators
import os


class BasePage(Operations):

    def should_be_links_in_navbar(self):
        """
        Check, that guest can see all icons on navbar
        """
        self.assertTrue(self.is_element_present(*BaseLocators.LOGIN_LINK), "Login link is not presented")
        self.assertTrue(self.is_element_present(*BaseLocators.SEARCH_LINK), "Search link is not presented")
        self.assertTrue(self.is_element_present(*BaseLocators.CART_LINK), "Cart link is not presented")
        self.assertTrue(self.is_element_present(*BaseLocators.CATEGORY_LINK), "Category link is not presented")

    def should_be_logo_link(self):
        """
        Check, that guest can see all icons on navbar
        """
        # assert self.is_element_present(*BaseLocators.LOGO_LINK), "Logo link is not presented"
        self.assertTrue(self.is_element_present(*BaseLocators.LOGO_LINK), "Logo link is not presented")
