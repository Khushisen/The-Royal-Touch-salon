from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock','description','image','created_at')
    list_editable = ('stock',)
