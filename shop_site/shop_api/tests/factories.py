from factory import DjangoModelFactory, Faker
from shop.models import Brand


class BrandFactory(DjangoModelFactory):
    name = Faker('company')
    description = ('text')

    class Meta:
        model = Brand
