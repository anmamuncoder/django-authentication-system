from apps.inventory.models import Category,Inventory
from django.contrib import admin
# Register your models here.

# --------------------------
# Category Admin
# --------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','inventory_count']

# --------------------------
# Inventory Admin
# --------------------------
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['user','name','priority','category']

