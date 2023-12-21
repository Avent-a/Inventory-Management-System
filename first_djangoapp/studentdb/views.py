from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import *
from django.db import connection
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum, F


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

def calculate_total_quantity(selected_component_id, selected_warehouse_minus_id):
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

    total_quantity = products_movement_quantity - substitution_quantity

    return total_quantity

def add_warehouse_movement(request):
    total_quantity = 0

    if request.method == 'POST':
        # Логика отображения данных о складе
        if 'show_items' in request.POST:
            id_warehouse_minus = request.POST.get('id_warehouse_minus')
            selected_component_id = request.POST.get('component_name')

            # Ваш SQL-запрос для отображения данных о складе
            query = '''
                SELECT 
                    wm.id AS movement_id,
                    wm.IdWarehouseMinus_id AS from_warehouse_id,
                    from_warehouse.address AS from_warehouse_address,
                    wm.IdWarehousePlus_id AS to_warehouse_id,
                    to_warehouse.address AS to_warehouse_address,
                    c.name AS component_name,
                    wm.quantity AS movement_quantity,
                    wm.date AS movement_date
                FROM 
                    studentdb_warehousemovement wm
                JOIN 
                    studentdb_components c ON wm.IdComponents_id = c.id
                JOIN 
                    studentdb_warehouse from_warehouse ON wm.IdWarehouseMinus_id = from_warehouse.id
                JOIN 
                    studentdb_warehouse to_warehouse ON wm.IdWarehousePlus_id = to_warehouse.id
                WHERE 
                    (wm.IdWarehouseMinus_id = %s OR wm.IdWarehousePlus_id = %s)
                    AND c.id = %s;
            '''

            with connection.cursor() as cursor:
                cursor.execute(query, [id_warehouse_minus, id_warehouse_minus, selected_component_id])
                components_arrival = dictfetchall(cursor)

            # Добавляем логику для вычисления общего количества
            total_quantity = calculate_total_quantity(selected_component_id, id_warehouse_minus)

            return render(request, 'add_warehouse_movements.html', {'warehouses': Warehouse.objects.all(), 'components_arrival': components_arrival, 'components': Components.objects.all(), 'total_quantity': total_quantity})

        # Если нажата кнопка "Add Movement"
        elif 'add_movement' in request.POST:

            try:
                selected_component_id = request.POST.get('component_name')
                quantity = int(request.POST.get('quantity'))
                id_warehouse_plus = request.POST.get('id_warehouse_plus')
                id_warehouse_minus = request.POST.get('id_warehouse_minus')
                date = request.POST.get('date')
                comment = request.POST.get('comment')

                if not selected_component_id or not id_warehouse_plus or not id_warehouse_minus or not date or not comment:
                    messages.error(request, 'Пожалуйста, заполните все обязательные поля действительными значениями.')
                else:
                    selected_component = Components.objects.get(id=selected_component_id)

                    # Вычисляем общее количество перед сохранением
                    total_quantity = calculate_total_quantity(selected_component_id, id_warehouse_minus)

                    if request.POST.get('enable_edit') == 'on':
                        # Если чекбокс включен, используем введенное пользователем значение
                        warehouse_movement = WarehouseMovement(
                            IdComponents=selected_component,
                            quantity=quantity,
                            IdWarehousePlus_id=id_warehouse_plus,
                            IdWarehouseMinus_id=id_warehouse_minus,
                            date=date,
                            Comment=comment,
                        )

                        warehouse_movement.save()

            except (Components.DoesNotExist, ValueError):
                messages.error(request, 'Недопустимый ввод. Пожалуйста, проверьте ваши данные.')

    warehouses = Warehouse.objects.all()
    return render(request, 'add_warehouse_movements.html', {'warehouses': warehouses, 'components': Components.objects.all(), 'total_quantity': total_quantity})

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


    
#-------------------------------------------------------------------------------------

def products_movements(request):
    products_movements = ProductsMovement.objects.all()
    return render(request, 'products_movements.html', {
        'products_movements': products_movements
    })
#-------------------------------------------------------------------------------------