from django.urls import path
from shop.views import (
    HomePage, ProductsPage, ArticleDetail
)


app_name = 'shop'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('categories/<category>/', ProductsPage.as_view(), name='products'),
    path('categories/<category>/<sub_cat_1>/', ProductsPage.as_view(), name='products'),
    path('categories/<category>/<sub_cat_1>/<sub_cat_2>/', ProductsPage.as_view(), name='products'),
    path('article/<slug:slug>/', ArticleDetail.as_view(), name='about_article'),
]
