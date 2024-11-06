from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','stock','available','category')
    list_filter=('category','available')
    search_fields=('name',)
    list_editable=('price','stock','available')