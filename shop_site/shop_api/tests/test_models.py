from django.test import TestCase

from shop.models import Brand
from .factories import BrandFactory


class BrandTestCase(TestCase):
    def test_str(self):
        brand = BrandFactory()
        self.assertEqual(str(brand), brand.name)
