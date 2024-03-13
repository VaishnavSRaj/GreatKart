from django.contrib import admin
from .models import OrderedProduct, Payment, Order

class OrderAdmin(admin.ModelAdmin):
  list_display=['order_number','full_name','phone','email','city','state','is_ordered','order_total','created_at']
  # list_filter=['status','is_ordered']
  search_fields=['email','first_name','last_name','order_number']
  list_per_page=20
  
class OrderProductInline(admin.TabularInline):
  model = OrderedProduct 
  extra=0 
admin.site.register(Payment)
admin.site.register(OrderedProduct)
admin.site.register(Order,OrderAdmin)


