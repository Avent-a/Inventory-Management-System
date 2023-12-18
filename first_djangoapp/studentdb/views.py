from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    warehouses = Warehouse.objects.all()
    offices = Office.objects.all()
    employees = Employee.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    components = Components.objects.all()
    arrival_of_components = ArrivalOfComponents.objects.all()
    warehouse_movements = WarehouseMovement.objects.all()
    complimentarys = Complimentary.objects.all()
    motions_from_products = MotionFromProduct.objects.all()

    context = {
        'warehouses': warehouses,
        'offices': offices,
        'employees': employees,
        'products': products,
        'orders': orders,
        'components': components,
        'arrival_of_components': arrival_of_components,
        'warehouse_movements': warehouse_movements,
        'complimentarys': complimentarys,
        'motions_from_products': motions_from_products,
    }
    return render(request, 'index.html', context)

def warehouse(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse.html', {
        'warehouses': warehouses
    })

def product(request):
    products = Product.objects.all()
    return render(request, 'products.html', {
        'products': products,
    })

def offices(request):
    offices = Office.objects.all()
    return render(request, 'offices.html', {
        'offices': offices
    })

def employees(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {
        'employees': employees
    })

def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {
        'orders': orders
    })

def components(request):
    components = Components.objects.all()
    return render(request, 'components.html', {
        'components': components
    })