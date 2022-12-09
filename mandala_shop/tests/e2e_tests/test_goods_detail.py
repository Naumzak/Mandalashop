from .pages.goods_detail_page import GoodsDetailPage
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .test_base_page import TestBasePage

class TestMainPage(TestBasePage):

    def setUp(self):
        super().setUp()
        self.url = '/kava/q/'
        self.page = GoodsDetailPage(browser=self.selenium, live_server_url=self.live_server_url, url=self.url)

    def tearDown(self):
        self.selenium.quit()

    def test_logo(self):
        """
        Check, that guest can see logo
        """
        self.page.open()
        self.page.should_be_logo_link()

    def test_navbar(self):
        """
        Check, that guest can see all icons on navbar
        """
        self.page.open()
        self.page.should_be_links_in_navbar()

    def test_product_image(self):
        """
        Check, that guest can see product image
        """
        self.page.open()
        self.page.should_be_product_image()
        pass

    def test_availability_status(self):
        """
        Check, that guest can see availability status
        """
        self.page.open()
        self.page.should_be_availability_status()
        pass

    def test_tare_selection(self):
        """
        Check, that guest can see tare selection
        """
        self.page.open()
        self.page.should_be_tare_selection()
        pass
