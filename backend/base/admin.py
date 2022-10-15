from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Product) # registering Product model in admin dashboard
admin.site.register(Order) # registering Order model in admin dashboard
admin.site.register(OrderItem) # registering OrderItem model in admin dashboard
admin.site.register(Review) # registering Review model in admin dashboard
admin.site.register(ShippingAddress) # registering ShippingAddress model in admin dashboard