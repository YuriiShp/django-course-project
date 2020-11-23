from django.shortcuts import render, Http404
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView
)

from shop import models
from django.db.models import Sum, Q



class NavBarMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = categorize(models.Category.objects.all())
        context['brands'] = models.Brand.objects.all()

        return context


class SideBarMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['breadcrumb'] = []

        # breadcrumb context
        categories = models.Category.objects.all()
        category = None
        parent = None
        for i in self.kwargs.values():
            category = categories.get(slug=i, parent=parent)
            context['breadcrumb'].append(category)
            parent = category

        # sizes
        context['masses'] = models.Article.objects.filter(
            Q(category=category) |
            Q(category__parent=category)
        ).exclude(items__mass__isnull=True).values_list('items__mass', flat=True)

        context['volumes'] = models.Article.objects.filter(
            Q(category=category) |
            Q(category__parent=category)
        ).exclude(items__volume__isnull=True).values_list('items__volume', flat=True)

        context['sizes'] = models.Article.objects.filter(
            Q(category=category) |
            Q(category__parent=category)
        ).exclude(items__size__isnull=True).values_list('items__size', flat=True)

        # brands
        context['brand'] = models.Brand.objects.filter(
            Q(articles__category=category) |
            Q(articles__category__parent=category)
        ).distinct()

        # ratings
        context['raitings'] = models.Review.objects.values_list('rate', flat=True)

        return context


class FilterMixin(object):

    def apply_filters(self, queryset):

        if self.request.GET:
            filters_dict = self.request.GET

            for key in filters_dict.keys():
                if key == "sale":
                    queryset = queryset.filter(items__sale=filters_dict[key]).distinct()
                if key == "brand":
                    queryset = queryset.filter(brand__name=filters_dict[key])
                if key == "rate":
                    queryset = queryset.filter(average_rate__gte=filters_dict[key])
                if key == "mass":
                    queryset = queryset.filter(items__mass=filters_dict[key]).distinct()
                if key == "volume":
                    queryset = queryset.filter(items__volume=filters_dict[key]).distinct()
                if key == "size":
                    queryset = queryset.filter(items__size=filters_dict[key]).distinct()

        return queryset


class HomePage(NavBarMixin,ListView):
    model = models.Article
    template_name = 'shop/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = models.Article.objects.filter(items__sale=True).distinct()
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        sales_dict = models.SalesRecord.objects.values('item').annotate(total_amount=Sum('amount')).order_by('-total_amount')[:40]
        sales_context_dict = {'articles': set()}
        for i in sales_dict.all():
            id = i['item']
            sales_context_dict['articles'].add(models.Article.objects.get(items__id=id))
        context['bestsellers'] = sales_context_dict

        return context


class ProductsPage(NavBarMixin,SideBarMixin,FilterMixin,ListView):
    model = models.Article
    template_name = 'shop/content.html'
    context_object_name = 'articles'
    paginate_by = 12
    paginate_orphans = 4

    def get_queryset(self):
        kwargs = self.kwargs
        categories = models.Category.objects.all()
        parent=None

        for slug in self.kwargs.values():
            category = categories.get(slug=slug, parent=parent)

            if not category:
                raise Http404
            else:
                parent = category

        if len(self.kwargs.values()) == 1:
            queryset = models.Article.objects.filter(category__parent__parent=category)
        elif len(self.kwargs.values()) == 2:
            queryset = models.Article.objects.filter(category__parent=category)
        elif len(self.kwargs.values()) == 3:
            queryset = models.Article.objects.filter(category=category)

        queryset = self.apply_filters(queryset)

        return queryset


class ArticleDetail(NavBarMixin, DetailView):
    model = models.Article
    context_object_name = 'article'
    template_name = 'shop/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['average_rate'] = self.object.get_average_rate()
        return context





def categorize(category_model):

    res_list = []
    queryset_0 = category_model.filter(parent=None)
    for i in queryset_0:
        dict_0 = {
            'name': i.name,
            'slug': i.slug,
            'subcategories': []
        }
        queryset_1 = category_model.filter(parent=i)
        for j in queryset_1:
            dict_1 = {
                'name': j.name,
                'slug': j.slug,
                'subcategories': []
            }
            queryset_2 = category_model.filter(parent=j)
            for k in queryset_2:
                dict_2 = {
                    'name': k.name,
                    'slug': k.slug
                }
                dict_1['subcategories'].append(dict_2)
            dict_0['subcategories'].append(dict_1)
        res_list.append(dict_0)
    return res_list
