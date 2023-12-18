from django.contrib import admin
from .models import Warehouse, Office, Employee, Category, Product, Order, Components, ArrivalOfComponents, WarehouseMovement, Complimentary, MotionFromProduct

admin.site.register (Warehouse)
admin.site.register (Office)
admin.site.register (Employee)
admin.site.register (Category)
admin.site.register (Product)
admin.site.register (Order)
admin.site.register (Components)
admin.site.register (ArrivalOfComponents)
admin.site.register (WarehouseMovement)
admin.site.register (Complimentary)
admin.site.register (MotionFromProduct)
# Register your models here.
