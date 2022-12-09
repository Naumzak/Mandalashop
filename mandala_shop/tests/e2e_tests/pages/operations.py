from selenium.common.exceptions import NoSuchElementException
from django.test import TestCase


class Operations(TestCase):

    def __init__(self, browser, live_server_url, url="", timeout=10):
        super().__init__()
        self.browser = browser
        self.live_server_url = live_server_url
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self, ):  # open page
        self.browser.get('%s%s' % (self.live_server_url, self.url))

    def is_element_present(self, type_selector, selector):  # Check that element exists on page
        try:
            self.browser.find_element(type_selector, selector)
        except NoSuchElementException:
            return False
        return True

    def elements_more_than(self, type_selector, selector, count):  # Check that elements more than count
        try:
            len(self.browser.find_elements(type_selector, selector)) > count
        except NoSuchElementException:
            return False
        return True
