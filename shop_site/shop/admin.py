from django.contrib import admin
from shop import models


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):

    list_filter = ['brand', 'category']


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Item)
admin.site.register(models.Brand)
admin.site.register(models.Category)
admin.site.register(models.SaleApply)
admin.site.register(models.Review)
admin.site.register(models.SalesRecord)
