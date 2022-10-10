from django.contrib import admin
from . import models


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'available',)
    search_fields = ('name',)
    filter_horizontal = ('weight', 'ingredients')
    list_editable = ('available',)
    list_filter = ('available', 'hot')


admin.site.register(models.Category)
admin.site.register(models.Weight)
admin.site.register(models.Goods, GoodsAdmin)
admin.site.register(models.Test)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.DeliveryAddress)
