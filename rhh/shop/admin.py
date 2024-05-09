from django.contrib import admin

from shop.models import UserOtpModel, ProductModel, DjangoUser, Order, OrderItem, MessageUs

from import_export.admin import ExportActionMixin


# Register your models here.

# admin.site.register(UserOtpModel)
# admin.site.register(ProductModel)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['product_name', 'product_price','product_stock']
@admin.register(DjangoUser)
class User(ExportActionMixin, admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_verified']


@admin.register(UserOtpModel)
class UserOtpAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['user', 'code']


@admin.register(ProductModel)
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'product_stock', 'product_description', 'product_picture']


@admin.register(Order)
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['user', 'paid', 'created', 'updated']


@admin.register(OrderItem)
class OrderItemAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']


@admin.register(MessageUs)
class MessageUsAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['username', 'phonenum', 'useremail', 'message', 'created', 'updated']
