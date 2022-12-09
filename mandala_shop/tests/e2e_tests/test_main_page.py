import os

from .pages.main_page import MainPage
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .pages.locators import MainPageLocators
from .test_base_page import TestBasePage


class TestMainPage(TestBasePage):

    def setUp(self):
        super().setUp()
        self.url = ''
        self.page = MainPage(browser=self.selenium, live_server_url=self.live_server_url)

    def tearDown(self):
        self.selenium.quit()

    def test_navbar(self):
        """
        Check, that guest can see all icons on navbar
        """
        self.page.open()
        self.page.should_be_links_in_navbar()

    def test_logo(self):
        """
        Check, that guest can see logo
        """
        self.page.open()
        self.page.should_be_logo_link()

    def test_category_panel(self):
        """
        Check, that guest can see logo
        """
        self.page.open()
        self.page.should_be_single_category_link()
        pass
