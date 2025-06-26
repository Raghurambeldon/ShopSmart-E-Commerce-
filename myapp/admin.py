from django.contrib import admin
from .models import Product,Category,Customer,Cart,Order,OrderItem
# Register your models here.

class Cartinfo(admin.ModelAdmin):
    list_display = ["customer","product","quantity"]

class Productinfo(admin.ModelAdmin):
    list_display = ["name","category","price"]

class Customerinfo(admin.ModelAdmin):
    list_display = ["first_name","email","mobile"]

admin.site.register(Product,Productinfo)
admin.site.register(Customer,Customerinfo)
admin.site.register(Cart,Cartinfo)
admin.site.register(Order)
admin.site.register(OrderItem)
