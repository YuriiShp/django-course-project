from django.urls import path

from shop_api.views import (
    ListBrands, ListCategories, GeneralArticlesApiView, ListArticles
)


urlpatterns = [
    path('brands/', ListBrands.as_view({
        'get': 'list',
        'post': 'create'
    })
    ),
    path('articles/', GeneralArticlesApiView.as_view()),
    path('categories/', ListCategories.as_view()),
]
