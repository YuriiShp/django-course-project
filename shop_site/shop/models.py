from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



# Create your models here.
class Item(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='items')
    price = models.FloatField(default=0)
    size = models.CharField(max_length=100, blank=True, null=True)
    mass = models.CharField(max_length=100, blank=True, null=True)
    volume = models.CharField(max_length=100, blank=True, null=True)

    sale = models.BooleanField(default=False)
    sale_price = models.FloatField(blank=True)

    amount_avaliable = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=False, editable=False)

    def apply_sale(self, rate):
        if rate > 1 or rate < 0:
            raise ValueError(
                _('invalid rate value (should be in span from 0 to 1)'),
                params={'rate': rate},
            )
        self.sale = True
        self.sale_price = round(self.price * (1-rate), 2)
        self.save()

    def unapply_sale(self):
        self.sale = False
        self.save()

    def save(self, *args, **kwargs):
        if self.sale == False:
            self.sale_price = self.price

        if self.amount_avaliable == 0:
            self.in_stock = False
        else:
            self.in_stock = True
        print(self.price)

        super().save(*args, **kwargs)

    def __str__(self):
        if self.size:
            return str(self.article) + ', ' + str(self.size)
        if self.mass:
            return str(self.article) + ', ' + str(self.mass)
        if self.volume:
            return str(self.article) + ', ' + str(self.volume)
        return str(self.article)


    class Meta:
        ordering = ['article']



class Article(models.Model):
    image = models.ImageField(upload_to='shop/articles/', blank=True)
    title = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='articles')
    description = models.TextField(blank=True)
    contents = models.TextField(blank=True)
    manual = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='articles')

    reviews = models.ManyToManyField('Review', blank=True)
    average_rate = models.FloatField(default=0)

    slug = models.SlugField(allow_unicode=True, null=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        plain_text_cyrilic = ' '.join([str(self.brand), str(self.title)])
        plain_text_latin = transliterate(plain_text_cyrilic)
        self.slug = slugify(plain_text_latin)
        self.average_rate = self.get_average_rate()
        super().save(*args, **kwargs)

    def get_average_rate(self):
        total_rate = 0
        for rev in self.reviews.all():
            total_rate += rev.rate
        num_of_voters = 1
        if self.reviews.count() != 0:
            num_of_voters = self.reviews.count()

        avreage_rate = total_rate / num_of_voters

        return round(avreage_rate,  1)

    def __str__(self):
        return str(self.brand) + ': ' + str(self.title)

    class Meta:
        ordering = ['brand']
        unique_together = ['title', 'brand']


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, null=True, editable=False)
    level = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.slug = slugify(transliterate(self.name))

        if not self.parent:
            self.level = 0

        super().save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        full_path.reverse()
        return ' -> '.join(full_path)

    class Meta:

        unique_together = ['parent', 'name']


class SaleApply(models.Model):
    items = models.ManyToManyField('Item')
    sale_rate = models.FloatField()

    def save(self, *args, **kwargs):
        super(SaleApply, self).save(*args, **kwargs)
        for itm in self.items.all():
            itm.apply_sale(self.sale_rate)
            itm.save()
        super(SaleApply, self).save(*args, **kwargs)

    def delete(self):
        for itm in self.items.all():
            itm.sale = False
            itm.save()
        super().delete()


class Review(models.Model):
    VALUES = (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.PositiveIntegerField(choices=VALUES, default=0)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ': ' + str(self.text)


class SalesRecord(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='records')
    amount = models.PositiveIntegerField(default=0)
    total_price = models.FloatField(default=0)
    time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = round(self.item.sale_price * self.amount, 2)
        super().save(*args, **kwargs)


    # class Sales(models.Model):
    #     product_name = models.ForeignKey(Product)
    #     category = models.ForeignKey(Category)
    #     sales= models.DecimalField(max_digits=25)

    # Sales.objects.values(
    #         'product_name'
    #     ).annotate(
    #         total_sales=Sum('sales')
    #     ).order_by('product_name')
    #


def transliterate(string):
    letters = {
        'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'є':'ye',
        'ж':'zh', 'з':'z', 'и':'y', 'і':'i', 'ї':'yi', 'й':'y', 'к':'k',
        'л':'l', 'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s',
        'т':'t', 'у':'u', 'ф':'f', 'х':'kh', 'ц':'ts', 'ч':'ch', 'ш':'sh',
        'щ':'shch', 'ь':'', 'ю':'yu', 'я':'ya', '\'':'-'
    }

    string = string.lower()

    for char in string:
        if char in letters.keys():
            string = string.replace(char, letters[char])

    return string
