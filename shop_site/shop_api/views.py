from django.shortcuts import render
from rest_framework import generics

from rest_framework import views, viewsets, mixins
from rest_framework.response import Response


from shop_api.serializers import (
    BrandSerializer, GeneralItemInfoSerializer, GeneralArticleInfoSerializer,
    CategorySerializer, ItemPostSerializer
)
from shop_api.permissions import HasGroupPermission
from shop.models import (
    Brand, Article, Item, Category
)

# Create your views here.
class ListBrands(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ListCategories(generics.ListAPIView):
    queryset = Category.objects.filter(level=0)
    serializer_class = CategorySerializer


class GeneralArticlesApiView(views.APIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['moderators',],
        'PUT': ['moderators',],
        'PATCH': ['moderators'],
        'DELETE': ['moderators',],
    }


    def get(self, request):
        return Response(data=GeneralArticleInfoSerializer(Article.objects.all(), many=True).data)

    def post(self, request):
        serializer = ItemPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)


class ListArticles(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['moderators',],
    }
    queryset = Article.objects.all()
    serializer_class = GeneralArticleInfoSerializer

    def create(self, request, *args, **kwargs):
        serializer = ItemPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATES, headers=headers)
