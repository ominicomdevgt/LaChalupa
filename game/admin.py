from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import Card, Reward, Store, Stock
# Register your models here.

#admin.site.register(Card)
class role_inline(admin.TabularInline):
    model = Stock
    extra = 1

@register(Reward)
class RewardAdmin(ModelAdmin):
    list_display = ('type_reward','size','image')
    inlines = (role_inline,)

@register(Store)
class StoreAdmin(ModelAdmin):
    list_display = ('name','lat','longitude')
    inlines = (role_inline,)

@register(Stock)
class StockAdmin(ModelAdmin):
    list_display = ('unit','store','reward')

