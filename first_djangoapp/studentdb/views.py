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

# Функция для вычисления общего количества для выбранного компонента и складов
def calculate_total_quantity(selected_component_id, selected_warehouse_minus_id, selected_warehouse_plus_id):
    # Получаем сумму количества перемещений из склада минус для выбранного компонента
    warehouse_movement_quantity_minus = WarehouseMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehouseMinus_id=selected_warehouse_minus_id
    ).aggregate(
        warehouse_movement_quantity_minus=Sum('quantity')
    )['warehouse_movement_quantity_minus'] or 0

    # Получаем сумму количества перемещений из склада плюс для выбранного компонента
    warehouse_movement_quantity_plus = WarehouseMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehousePlus_id=selected_warehouse_plus_id
    ).aggregate(
        warehouse_movement_quantity_plus=Sum('quantity')
    )['warehouse_movement_quantity_plus'] or 0

    # Получаем сумму количества обновленных перемещений продукции для выбранного компонента
    products_movement_quantity = ProductsMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehouse__id=selected_warehouse_minus_id,
        status='updated'
    ).aggregate(
        products_movement_quantity=Sum('quantity')
    )['products_movement_quantity'] or 0

    # Получаем сумму количества перемещений продукции с заменой для выбранного компонента
    substitution_quantity = ProductsMovement.objects.filter(
        IdComponents_id=selected_component_id,
        IdWarehouse__id=selected_warehouse_minus_id,
        status='substitution'
    ).aggregate(
        substitution_quantity=Sum('quantity')
    )['substitution_quantity'] or 0

    # Общее количество вычисляется как сумма плюс, минус и обновленных перемещений, с учетом замен
    total_quantity = warehouse_movement_quantity_plus + products_movement_quantity - warehouse_movement_quantity_minus - substitution_quantity

    return total_quantity



# Функция обработки запроса на добавление перемещения на склад
def add_warehouse_movement(request):
    # Инициализация переменной для хранения общего количества
    total_quantity = 0

    # Проверка, был ли запрос методом POST
    if request.method == 'POST':
        try:
            # Получение данных из запроса для добавления нового перемещения
            selected_component_id = request.POST.get('component_name')
            quantity_raw = request.POST.get('quantity')
            quantity = int(quantity_raw) if quantity_raw is not None else 0
            id_warehouse_plus = request.POST.get('id_warehouse_plus')
            id_warehouse_minus = request.POST.get('id_warehouse_minus')
            date = request.POST.get('date')
            comment = request.POST.get('comment')

            # Проверка наличия необходимых данных
            if not selected_component_id or not id_warehouse_plus or not id_warehouse_minus or not date or not comment:
                messages.error(request, 'Пожалуйста, заполните все обязательные поля действительными значениями.')
            else:
                # Получение объекта компонента по его ID
                selected_component = Components.objects.get(id=selected_component_id)

                # Вычисление общего количества после добавления нового перемещения
                total_quantity = calculate_total_quantity(selected_component_id, id_warehouse_minus, id_warehouse_plus)

                # Если опция 'enable_edit' включена, создаем новое перемещение на склад
                if request.POST.get('enable_edit') == 'on':
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

    # Отображение шаблона с результатами
    return render(request, 'add_warehouse_movements.html', {'warehouses': Warehouse.objects.all(), 'components': Components.objects.all(), 'total_quantity': total_quantity})

# Функция для преобразования результата запроса курсора в список словарей
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_total_quantity(request):
    # Получите значения component_id и warehouse_minus_id из GET-параметров
    component_id = request.GET.get('component_id')
    warehouse_minus_id = request.GET.get('warehouse_minus_id')

    # Вычислите total_quantity используя вашу функцию calculate_total_quantity
    total_quantity = calculate_total_quantity(component_id, warehouse_minus_id, None)

    # Отправьте JSON-ответ с total_quantity
    return JsonResponse({'total_quantity': total_quantity})
    
#-------------------------------------------------------------------------------------

def products_movements(request):
    products_movements = ProductsMovement.objects.all()
    return render(request, 'products_movements.html', {
        'products_movements': products_movements
    })
#-------------------------------------------------------------------------------------