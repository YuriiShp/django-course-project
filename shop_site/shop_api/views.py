from django.shortcuts import render, reverse
from rest_framework import generics

from rest_framework import views, viewsets, mixins, status
from rest_framework.response import Response


from shop_api.serializers import (
    BrandSerializer,
    CategoryIDSerializer, CategoryGetSerializer, CategoryAddSerializer,
    GeneralArticleInfoSerializer, FullArticleInfoSerializer, ArticleAddSerializer,
    GeneralItemInfoSerializer, ItemIDSerializer, ItemGetSerializer, ItemPostSerializer,
    ManageStockSerializer, ApplySaleSerializer, UnApplySaleSerializer,
    ReviewSerializer,

)
from shop_api.permissions import HasGroupPermission
from shop.models import (
    Brand, Article, Item, Category
)

# Create your views here.
class BrandsViewSet(viewsets.ModelViewSet):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['__all__'],
        'PUT': ['__all__'],
        'DELETE': ['__all__'],
    }
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryAPIView(views.APIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['__all__'],
        'PUT': ['__all__'],
        'DELETE': ['__all__'],
    }

    def get(self, request):
        serializer = CategoryGetSerializer(Category.objects.filter(level=0), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoryAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CategoryGetSerializer(Category.objects.filter(level=0), many=True).data)

    def put(self, request):
        id_serializer = CategoryIDSerializer(data=request.GET)
        id_serializer.is_valid(raise_exception=True)
        instance = Category.objects.get(pk=request.GET.get('pk'))
        serializer = CategoryAddSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CategoryGetSerializer(Category.objects.filter(level=0), many=True).data)

    def delete(self, request):
        id_serializer = CategoryIDSerializer(data=request.GET)
        id_serializer.is_valid(raise_exception=True)
        instance = Category.objects.get(pk=request.GET.get('pk'))
        instance.delete()
        return Response(CategoryGetSerializer(Category.objects.filter(level=0), many=True).data)


class ItemFilterMixin(object):

    def apply_filters(self, queryset):

        if self.request.GET:
            filters_dict = self.request.GET

            for key in filters_dict.keys():
                if key == "article":
                    queryset = queryset.filter(article_id=filters_dict[key])
                if key == "sale":
                    queryset = queryset.filter(sale=filters_dict[key])
                if key == "in_stock":
                    queryset = queryset.filter(in_stock=filters_dict[key])
                if key == "mass":
                    queryset = queryset.filter(mass=filters_dict[key])
                if key == "volume":
                    queryset = queryset.filter(volume=filters_dict[key])
                if key == "size":
                    queryset = queryset.filter(size=filters_dict[key])
        return queryset


class ItemGetAllPost(ItemFilterMixin, generics.ListCreateAPIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['__all__'],
    }
    serializer_class = ItemGetSerializer

    def get_queryset(self):
        return self.apply_filters(Item.objects.all())

    def create(self, request, *args, **kwargs):

        item_serializer = ItemPostSerializer(data=request.data)
        item_serializer.is_valid(raise_exception=True)
        item_serializer.save()

        return Response(self.serializer_class(self.queryset, many=True).data, status=status.HTTP_202_ACCEPTED)




class ArticleFilterMixin(object):

    def apply_filters(self, queryset):

        if self.request.GET:
            filters_dict = self.request.GET

            for key in filters_dict.keys():

                # filter articles
                if key == "category":
                    queryset = queryset.filter(category__id=filters_dict[key])
                if key == "brand":
                    queryset = queryset.filter(brand__name=filters_dict[key])
                if key == "rate":
                    queryset = queryset.filter(average_rate__gte=filters_dict[key])

                # filter articles with specific items
                if key == "sale":
                    queryset = queryset.filter(items__sale=filters_dict[key]).distinct()
                if key == "mass":
                    queryset = queryset.filter(items__mass=filters_dict[key]).distinct()
                if key == "volume":
                    queryset = queryset.filter(items__volume=filters_dict[key]).distinct()
                if key == "size":
                    queryset = queryset.filter(items__size=filters_dict[key]).distinct()
        return queryset


class ArticleGetAllPost(ArticleFilterMixin, generics.ListCreateAPIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['__all__'],
    }
    serializer_class = GeneralArticleInfoSerializer

    def get_queryset(self):
        return self.apply_filters(Article.objects.all())

    def create(self, request, *args, **kwargs):

        article_serializer = ArticleAddSerializer(data=request.data)
        article_serializer.is_valid(raise_exception=True)
        article_serializer.save()

        return Response(self.serializer_class(self.queryset, many=True).data, status=status.HTTP_202_ACCEPTED)


class ArticleGetSingleUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'GET': ['__all__'],
        'PUT': ['__all__'],
        'PATCH': ['__all__'],
        'DELETE': ['__all__']
    }
    queryset = Article.objects.all()
    serializer_class = FullArticleInfoSerializer

    def get_object(self):
        return self.queryset.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        article_serializer = ArticleAddSerializer(data=request.data, instance=instance)
        article_serializer.is_valid(raise_exception=True)
        response_inst = article_serializer.save()

        return Response(self.serializer_class(response_inst).data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        article_serializer = ArticleAddSerializer(data=request.data, instance=instance, partial=True)
        article_serializer.is_valid(raise_exception=True)
        response_inst = article_serializer.save()

        return Response(self.serializer_class(response_inst).data, status=status.HTTP_202_ACCEPTED)


# Add items to the stock via id
class AddToStockView(views.APIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'POST': ['__all__'],
    }

    def post(self, request):
        print(request.data)
        for entry in request.data:
            if 'item' in entry.keys() and 'amount' in entry.keys():
                id_serializer = ItemIDSerializer(data={'id':entry['item']})
                id_serializer.is_valid(raise_exception=True)

                entry['mode'] = 'arrived'
                serializer = ManageStockSerializer(data=entry)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# Remove items from the stock via id
class RemFromStockView(views.APIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'POST': ['__all__'],
    }

    def post(self, request):
        print(request.data)
        for entry in request.data:
            if 'item' in entry.keys() and 'amount' in entry.keys():
                id_serializer = ItemIDSerializer(data={'id':entry['item']})
                id_serializer.is_valid(raise_exception=True)

                entry['mode'] = 'removed'
                serializer = ManageStockSerializer(data=entry)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# Apply sale to items via id
class ApplySaleView(views.APIView):
    permission_classes = [HasGroupPermission,]
    required_groups = {
        'POST': ['__all__'],
        'DELETE': ['__all__']
    }

    def post(self, request):
        for entry in request.data:
            if 'item' in entry.keys() and 'sale_rate' in entry.keys():
                id_serializer = ItemIDSerializer(data={'id':entry['item']})
                id_serializer.is_valid(raise_exception=True)

                serializer = ApplySaleSerializer(data=entry)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(sef, request):
        for entry in request.data:
            id_serializer = ItemIDSerializer(data={'id':entry['item']})
            id_serializer.is_valid(raise_exception=True)

            serializer = UnApplySaleSerializer(data = entry)
            serializer.is_valid(raise_exception=True)
            serializer.delete()

        return Response(status=status.HTTP_202_ACCEPTED)
