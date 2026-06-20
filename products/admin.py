from django.contrib import admin

# Register your models here.
from .models import Product,Category,Order,User
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Order)

#AdminModel

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','category']
    # ordering = ['-price']
    list_per_page = 2
   

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name','status']
    list_filter = ['status']
    ordering = ['-id']
    
    list_editable = ['status']
    readonly_fields = ['created_at']
    

# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['name']





# admin.site.register(Product)