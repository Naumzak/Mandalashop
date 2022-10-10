from django.test import TestCase


class EasyTest(TestCase):
    def test_1(self):
        x = 2
        y = x * 2
        self.assertEqual(y, 4)


