from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop.models import (
    Article, Item, Brand, Category, Review,
    SalesRecord, InOutRecord, SaleApply
)


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


"""Category Serializers"""

class CategoryGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'children'
        ]

    def get_fields(self):
        fields = super(CategoryGetSerializer, self).get_fields()
        fields['children'] = CategoryGetSerializer(many=True)
        return fields


class CategoryAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'parent',
            'name'
        ]


class CategoryIDSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    def validate(self, attrs):
        if Category.objects.filter(pk=attrs['pk']).exists():
            return attrs
        else:
            raise ValidationError(detail='Object not found')


"""Article serializers for request method GET (list)"""

class GeneralItemInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields =[
            'id',
            'mass',
            'volume',
            'size',
            'sale',
            'price',
            'sale_price',
            'in_stock'
        ]


class GeneralArticleInfoSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    items = GeneralItemInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = [
            'pk',
            'title',
            'image',
            'brand',
            'category',
            'average_rate',
            'items'
        ]


"""Article serializers for request method GET (single)"""

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = [
            'user',
            'text',
            'rate',
            'date_updated'
        ]


class FullArticleInfoSerializer(GeneralArticleInfoSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Article
        fields = [
            'pk',
            'title',
            'image',
            'brand',
            'description',
            'contents',
            'manual',
            'average_rate',
            'reviews',
            'slug',
            'items'
        ]


"""Article serializers for request method POST/PUT/PATCH """

class ArticleAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'category',
            'title',
            'image',
            'brand',
            'description',
            'contents',
            'manual'
        ]


"""Item serializers"""

class ItemIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        if Item.objects.filter(pk=attrs['id']).exists():
            return attrs
        else:
            raise ValidationError('item not found')


class ItemGetSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = [
            'id',
            'article',
            'mass',
            'volume',
            'size',
            'price',
            'sale',
            'sale_rate',
            'sale_price',
            'amount_avaliable'
        ]


class ItemPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = [
            'article',
            'mass',
            'volume',
            'size',
            'price',
            'amount_avaliable'
        ]


class ManageStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = InOutRecord
        fields = [
            'item',
            'amount',
            'mode'
        ]


class ApplySaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleApply
        fields = [
            'item',
            'sale_rate'
        ]


class UnApplySaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleApply
        fields = ['item']
