from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
class TestBasePage(StaticLiveServerTestCase):
    fixtures = ['test_db_fixture.json']

    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.url = ''