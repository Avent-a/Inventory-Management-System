from datetime import datetime, timezone
import traceback
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.db import connection
from django.contrib import messages
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
import logging
from django.http import HttpResponse, JsonResponse

def index(request):
    warehouses = Warehouse.objects.all()
    offices = Office.objects.all()
    employees = Employee.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    components = Components.objects.all()
    warehouse_movements = WarehouseMovement.objects.all()
    products_movements = ProductsMovement.objects.all()

    context = {
        'warehouses': warehouses,
        'offices': offices,
        'employees': employees,
        'products': products,
        'orders': orders,
        'components': components,
        'warehouse_movements': warehouse_movements,
        'products_movements': products_movements,
    }
    return render(request, 'index.html', context)
#-------------------------------------------------------------------------------------

def warehouse(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse.html', {
        'warehouses': warehouses
    })
#-------------------------------------------------------------------------------------
def add_warehouse(request):
    if request.method == 'POST':
        address = request.POST['address']
        phone = request.POST['phone']

        new_warehouse = Warehouse(address=address, phone=phone)
        new_warehouse.save()
        return redirect('warehouse')
    return render(request, 'add_warehouse.html')

def delete_warehouse(request, warehouse_id):
    warehouse = Warehouse.objects.get(id=warehouse_id)
    warehouse.delete()
    return redirect('warehouse')
#-------------------------------------------------------------------------------------

def product(request):
    products = Product.objects.all()
    return render(request, 'products.html', {
        'products': products,
    })
#-------------------------------------------------------------------------------------

def offices(request):
    offices = Office.objects.all()
    return render(request, 'offices.html', {
        'offices': offices
    })

def add_offices(request):
    if request.method == 'POST':
        address = request.POST['address']
        area = request.POST['area']
        phone = request.POST['phone']  

        new_office = Office(address=address, area=area, phone=phone)
        new_office.save()
        return redirect('offices')
    return render(request, 'add_offices.html')
#-------------------------------------------------------------------------------------

def employees(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {
        'employees': employees
    })
#-------------------------------------------------------------------------------------

def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {
        'orders': orders
    })
#-------------------------------------------------------------------------------------

def components(request):
    components = Components.objects.all()
    return render(request, 'components.html', {
        'components': components
    })
#-------------------------------------------------------------------------------------

def warehouse_movements(request):
    warehouse_movements = WarehouseMovement.objects.all()
    return render(request, 'warehouse_movements.html', {
        'warehouse_movements': warehouse_movements
    })

logger = logging.getLogger(__name__)

def calculate_total_quantity(selected_component_id, selected_warehouse_minus_id, selected_warehouse_plus_id):
    warehouse_movement_quantity_minus = WarehouseMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehouseMinus_id=selected_warehouse_minus_id
    ).aggregate(
        warehouse_movement_quantity_minus=Sum('quantity')
    )['warehouse_movement_quantity_minus'] or 0

    warehouse_movement_quantity_plus = WarehouseMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehousePlus_id=selected_warehouse_plus_id
    ).aggregate(
        warehouse_movement_quantity_plus=Sum('quantity')
    )['warehouse_movement_quantity_plus'] or 0

    products_movement_quantity = ProductsMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehouse__id=selected_warehouse_minus_id,
        status='updated'
    ).aggregate(
        products_movement_quantity=Sum('quantity')
    )['products_movement_quantity'] or 0

    substitution_quantity = ProductsMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehouse__id=selected_warehouse_minus_id,
        status='substitution'
    ).aggregate(
        substitution_quantity=Sum('quantity')
    )['substitution_quantity'] or 0

    total_quantity = warehouse_movement_quantity_plus + products_movement_quantity - warehouse_movement_quantity_minus - substitution_quantity

    warehouses_with_component = Warehouse.objects.filter(
            warehouse_plus__IdComponents_id=selected_component_id
        ).annotate(
            total_quantity=Coalesce(Sum('warehouse_plus__quantity'), Value(0)) - Coalesce(Sum('warehouse_minus__quantity'), Value(0))
        )

    return {'total_quantity': total_quantity, 'warehouses_with_component': warehouses_with_component}


def get_warehouses_with_component(request):
    component_id = request.GET.get('component_id')
    try:
        result = calculate_total_quantity(component_id, None, None)
        warehouses_with_component = result['warehouses_with_component']

        # Создаем список с данными по складам и количеству
        data = [
            {'id': warehouse.id, 'address': warehouse.address, 'total_quantity': warehouse.total_quantity}
            for warehouse in warehouses_with_component
        ]

        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def add_warehouse_movement(request):
    total_quantity = 0
    warehouses_with_component = []

    if request.method == 'POST':
        try:
            selected_component_id = request.POST.get('component_name')
            quantity_raw = request.POST.get('quantity')
            quantity = int(quantity_raw) if quantity_raw is not None else 0
            id_warehouse_plus = request.POST.get('id_warehouse_plus')
            id_warehouse_minus = request.POST.get('id_warehouse_minus')
            date_str = request.POST.get('date')
            comment = request.POST.get('comment')

            if not selected_component_id or not id_warehouse_plus or not id_warehouse_minus or not date_str or not comment:
                return HttpResponse('Пожалуйста, заполните все обязательные поля действительными значениями.')

            selected_component = Components.objects.get(id=selected_component_id)

            # Проверка на допустимость значения quantity
            result = calculate_total_quantity(selected_component_id, id_warehouse_minus, id_warehouse_plus)
            total_quantity = result['total_quantity']
            warehouses_with_component = result['warehouses_with_component']
            

            # Проверка на дату
            current_datetime = datetime.now()
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
            if date > current_datetime:
                return HttpResponse('Дата перемещения не может быть в будущем.')

            # Вместо проверки enable_edit, просто всегда добавляем новое перемещение
            warehouse_movement = WarehouseMovement(
                IdComponents=selected_component,
                quantity=quantity,
                IdWarehousePlus_id=id_warehouse_plus,
                IdWarehouseMinus_id=id_warehouse_minus,
                date=date,
                Comment=comment,
            )
            warehouse_movement.save()

        except (Components.DoesNotExist, ValueError) as e:
            return HttpResponse(f'Недопустимый ввод. Пожалуйста, проверьте ваши данные. Ошибка: {e}')

    return render(request, 'add_warehouse_movements.html', {'warehouses': Warehouse.objects.all(), 'components': Components.objects.all(), 'total_quantity': total_quantity, 'warehouses_with_component': warehouses_with_component, 'warehouse_movements': WarehouseMovement.objects.all()})

def get_total_quantity(request):
    component_id = request.GET.get('component_id')
    warehouse_minus_id = request.GET.get('warehouse_minus_id')
    result = calculate_total_quantity(component_id, warehouse_minus_id, None)
    return JsonResponse(result)
    
#-------------------------------------------------------------------------------------

def products_movements(request):
    products_movements = ProductsMovement.objects.all()
    return render(request, 'products_movements.html', {
        'products_movements': products_movements
    })
#-------------------------------------------------------------------------------------