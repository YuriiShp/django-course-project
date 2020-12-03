from django.test import TestCase

from shop_api.serializers import BrandSerializer
from .factories import BrandFactory

# 
# class BrandSerializerTestCase(TestCase):
#     def test_model_fields(self):
#         """serializer's data matches the brand object for each field"""
#         brand = BrandFactory()
#         for field in = [
#             'id', 'name', 'description'
#         ]:
#             self.assertEqual(
#                 serializer.data
#             )
