from django.urls import path
from rest_framework import routers


from shop_api.views import (
    BrandsViewSet,
    CategoryAPIView,
    ItemGetAllPost,
    AddToStockView, RemFromStockView, ApplySaleView,
    ArticleGetAllPost,
    ArticleGetSingleUpdate,
)
router = routers.DefaultRouter()
router.register(r'brands', BrandsViewSet)

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('items/', ItemGetAllPost.as_view(), name='items'),
    path('items/add', AddToStockView.as_view()),
    path('items/remove', RemFromStockView.as_view()),
    path('items/sale', ApplySaleView.as_view()),
    path('articles/', ArticleGetAllPost.as_view()),
    path('articles/<pk>', ArticleGetSingleUpdate.as_view()),
]

urlpatterns += router.urls
