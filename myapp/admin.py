from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdminget(ImportExportActionModelAdmin):
    list_display = ("id", "product", "address", "order_date", "order")
    pass


@admin.register(Category)
class CategoryAdminget(ImportExportActionModelAdmin):
    list_display = ('id', "cat_name")
    pass


@admin.register(Product)
class ProductAdminget(ImportExportActionModelAdmin):
    list_display = ("id", "product_image", "description",
                    "price", "product_name", "subcat_name", "cat_name")
    pass


@admin.register(Cart)
class CartAdminget(ImportExportActionModelAdmin):
    pass


@admin.register(Contact)
class ContactAdminget(ImportExportActionModelAdmin):
    list_display = ("name", "email", "contact", "subject", "comment")
    pass


@admin.register(Register)
class RegisterAdminget(ImportExportActionModelAdmin):
    pass


@admin.register(Chack)
class ChackAdminget(ImportExportActionModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdminget(ImportExportActionModelAdmin):
    pass