from django.contrib import admin
from .models import Product,Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price","stock","updated_at","is_available",)
    prepopulated_fields = {"slug": ("product_name",)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ("product","variation_category","variation_value","is_active")
    list_editable=("is_active",)
    list_filter= ("product","variation_category","variation_value","is_active","created_at")
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation , VariationAdmin )