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
    path('', views.login, name='login'),
    path('index', views.index, name='index'),  # Empty path for the index page
    
        
    path('warehouse/', views.warehouse, name='warehouse'),
    path('warehouse/add/', views.add_warehouse, name='add_warehouse'),
    path('update_hidden_status/', views.update_hidden_status, name='update_hidden_status'),
    path('edit_warehouse/<int:warehouse_id>/', views.edit_warehouse, name='edit_warehouse'),
    path('calculate-total-quantity/', views.calculate_total_quantity, name='calculate_total_quantity'),
    
    path('products/', views.product, name='products'),
    path('products/add/', views.add_products, name='add_products'),

    path('offices/', views.offices, name='offices'),
    path('add_offices/', views.add_offices, name='add_offices'),
    path('edit_office/<int:office_id>/', views.edit_office, name='edit_office'),
    path('update_hidden_status_offices/', views.update_hidden_status_offices, name='update_hidden_status_offices'),
    
    path('employees/', views.employees, name='employees'),
    path('employees/add/', views.add_employees, name='add_employees'),
    path('edit_employees/<int:employee_id>/', views.edit_employees, name='edit_employees'),
    path('update_hidden_status_employees/', views.update_hidden_status_employees, name='update_hidden_status_employees'),

    path('orders/', views.orders, name='orders'),
    path('add_orders/add', views.add_orders, name='add_orders'),
    
    path('components/', views.components, name='components'),
    path('components/add/', views.add_components, name='add_components'),
    
    path('warehouse_movements/', views.warehouse_movements, name='warehouse_movements'),
    path('warehouse_movements/add', views.add_warehouse_movement, name='add_warehouse_movement'),
    
    path('products_movements/', views.products_movements, name='products_movements'),
    path('products_movements/add', views.add_products_movements, name='add_products_movements'),
]