from django.shortcuts import render, Http404
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView
)

from shop import models
from django.db.models import Sum



class BasePageMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = categorize(models.Category.objects.all())
        context['brands'] = models.Brand.objects.all()

        return context


class HomePage(BasePageMixin,ListView):
    model = models.Article
    template_name = 'shop/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = models.Article.objects.exclude(items__sale=False)
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


class ProductsPage(BasePageMixin,ListView):
    model = models.Article
    template_name = 'shop/contents.html'
    context_object_name = 'articles'
    paginate_by = 20
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

        queryset = models.Article.objects.filter(category=category)
        return queryset


class ArticleDetail(BasePageMixin, DetailView):
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
