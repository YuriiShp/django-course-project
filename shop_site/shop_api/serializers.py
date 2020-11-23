from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop.models import (
    Article, Item, Brand, Category, Review
)


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'children'
        ]

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['children'] = CategorySerializer(many=True)
        return fields


"""General articles info (List View display)"""

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


"""Full article info (Detail View display)"""

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
            'content',
            'manual',
            'average_rate',
            'reviews',
            'slug',
            'items'
        ]


"""Adding items"""
#
# class ArticleExistsPostSerializer(serializers.Serializer):
#
#     class Meta:
#         fields = [
#             'title',
#             'brand'
#         ]
#
#     def validate(self, attrs):
#         if Article.objects.get(**attrs):
#             return attrs
#         else:
#             raise ValidationError('article does not exist')
#
#
# class ArticleDoesNotExistsPostSerializer(serializers.ModelSerializer):
#     brand = serializers.StringRelatedField()
#     category = serializers.StringRelatedField()
#
#     class Meta:
#         model = Article
#         fields = [
#             'title',
#             'image',
#             'brand',
#             'description',
#             'content',
#             'manual',
#         ]


class ItemPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = [
            'article_id',
            'mass',
            'volume',
            'size',
            'sale',
            'price',
        ]

    def create(self, validated_data):
        print(validated_data.keys())
        article = Article.objects.get(pk=validated_data['article_id'])
        return Item.objects.create(**validated_data, article=article)
