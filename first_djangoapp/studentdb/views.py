import traceback
from unittest import result
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.db import connection
from django.contrib import messages
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
import logging
from django.http import HttpResponse, JsonResponse
from django.utils import timezone


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

def add_warehouse(request):
    if request.method == 'POST':
        address = request.POST['address']
        phone = request.POST['phone']

        new_warehouse = Warehouse(address=address, phone=phone)
        new_warehouse.save()
        return redirect('warehouse')
    return render(request, 'add_warehouse.html')
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

def add_orders(request):
    employees = Employee.objects.all()
    offices = Office.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        date = request.POST.get('date')
        status = request.POST.get('status')
        employee_id = request.POST.get('employee')
        product_id = request.POST.get('product')
        comment = request.POST.get('comment')
        office_id = request.POST.get('office')

        employee = Employee.objects.get(pk=employee_id)
        product = Product.objects.get(pk=product_id)
        office = Office.objects.get(pk=office_id)

        order = Order(
            date=date,
            status=status,
            employee=employee,
            product=product,
            comment=comment,
            IdOffice=office,
        )

        order.save()

        return redirect('orders')

    return render(request, 'add_orders.html', {'employees': employees, 'offices': offices, 'products': products})
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

def calculate_total_quantity(request):
    try:
        selected_component_id = request.GET.get('component_id')
        selected_warehouse_minus_id = request.GET.get('warehouse_minus_id')

        if not selected_component_id or not selected_warehouse_minus_id:
            return JsonResponse({'error': 'Invalid input. Please provide both component_id and warehouse_minus_id.'}, status=400)

        warehouse_movement_quantity_minus = WarehouseMovement.objects.filter(
            IdComponents_id=selected_component_id,
            IdWarehouseMinus_id=selected_warehouse_minus_id
        ).aggregate(
            warehouse_movement_quantity_minus=Sum('quantity')
        )['warehouse_movement_quantity_minus'] or 0

        warehouse_movement_quantity_plus = WarehouseMovement.objects.filter(
            IdComponents_id=selected_component_id,
            IdWarehousePlus_id=selected_warehouse_minus_id
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

        # Преобразование QuerySet в список словарей
        warehouses_with_component_list = list(warehouses_with_component.values())

        return JsonResponse({'total_quantity': total_quantity or 0, 'warehouses_with_component': warehouses_with_component_list})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

    
def add_warehouse_movement(request):
    total_quantity = 0
    warehouses_with_component = []

    if request.method == 'POST':
        try:
            selected_component_id = request.POST.get('component_name')
            quantity_raw = request.POST.get('quantity')
            quantity = int(quantity_raw) if quantity_raw.strip() else 0
            id_warehouse_plus = request.POST.get('id_warehouse_plus')
            id_warehouse_minus = request.POST.get('id_warehouse_minus')
            date_str = request.POST.get('date')
            comment = request.POST.get('comment')

            if not selected_component_id or not id_warehouse_plus or not id_warehouse_minus or not date_str or not comment:
                return HttpResponse('Please fill in all required fields with valid values.')

            selected_component = get_object_or_404(Components, id=selected_component_id)

            # Check if warehouse_plus_id is the same as warehouse_minus_id
            if id_warehouse_plus == id_warehouse_minus:
                return HttpResponse('Warehouse plus and minus cannot be the same.')

            # Convert the date string to a timezone-aware object
            current_timezone = timezone.get_current_timezone()
            date = current_timezone.localize(timezone.datetime.strptime(date_str, '%Y-%m-%dT%H:%M'))

            # Check if IdWarehouseMinus_id is present before saving
            if id_warehouse_minus is None:
                return HttpResponse('IdWarehouseMinus_id cannot be empty.')

            # Add print statement for debugging purposes
            print('IdWarehouseMinus_id:', id_warehouse_minus)

            # Check if IdWarehouseMinus_id is present before saving (additional check)
            if not id_warehouse_minus:
                return HttpResponse('IdWarehouseMinus_id cannot be empty.')

            # Check if the quantity is non-negative and less than or equal to available quantity
            if quantity <= 0:
                return HttpResponse('Quantity must be a non-negative value.')
            if quantity >= quantity:
                return HttpResponse('Quantity must be.')


            # Create and save the warehouse movement object
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
            # Return a more informative error message
            return HttpResponse(f'Input error. Please check your data. Error: {e}')

    context = {
        'warehouses': Warehouse.objects.all(),
        'components': Components.objects.all(),
        'total_quantity': total_quantity,
        'warehouses_with_component': warehouses_with_component,
        'warehouse_movements': WarehouseMovement.objects.all(),
    }

    return render(request, 'add_warehouse_movements.html', context)
    
#-------------------------------------------------------------------------------------

def products_movements(request):
    products_movements = ProductsMovement.objects.all()
    return render(request, 'products_movements.html', {
        'products_movements': products_movements
    })
#-------------------------------------------------------------------------------------