from factory import Faker
from factory.django import DjangoModelFactory
from shop.models import Brand


class BrandFactory(DjangoModelFactory):
    name = Faker('company')
    description = ('text')

    class Meta:
        model = Brand
