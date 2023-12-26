"""first_djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from studentdb import views

app_name = 'studentdb'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Empty path for the index page
    path('warehouse/', views.warehouse, name='warehouse'),
    path('warehouse/add/', views.add_warehouse, name='add_warehouse'),
    path('warehouse/<int:warehouse_id>/delete/', views.delete_warehouse, name='delete_warehouse'),
    path('calculate-total-quantity/', views.calculate_total_quantity, name='calculate_total_quantity'),
    path('products/', views.product, name='products'),
    path('offices/', views.offices, name='offices'),
    path('add_offices/', views.add_offices, name='add_offices'),
    path('employees/', views.employees, name='employees'),
    path('orders/', views.orders, name='orders'),
    path('components/', views.components, name='components'),
    path('warehouse_movements/', views.warehouse_movements, name='warehouse_movements'),
    path('warehouse_movements/add', views.add_warehouse_movement, name='add_warehouse_movement'),
    path('products_movements/', views.products_movements, name='products_movements')
]