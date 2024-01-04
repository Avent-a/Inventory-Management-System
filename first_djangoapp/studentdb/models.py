from django.db import models
from datetime import datetime

# Create your models here.

# Модель Склад
class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор склада
    address = models.CharField(max_length=255)  # адрес склада
    phone = models.CharField(max_length=20, null=True)  # телефонный номер склада
    def __str__(self):
        return '{0}'.format(self.address)

# Модель Офис
class Office(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор офиса
    address = models.CharField(max_length=255)  # адрес офиса
    area = models.IntegerField()  # площадь офиса в квадратных метрах
    phone = models.CharField(max_length=20, null=True)  # телефонный номер офиса
    def __str__(self):
        return '{0}'.format(self.address)

# Модель Сотрудник
class Employee(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор сотрудника
    name = models.CharField(max_length=50)  # имя сотрудника
    lastName = models.CharField(max_length=50)  # фамилия сотрудника
    def __str__(self):
        return '{0}'.format(self.name)

# Модель Категория
class Category(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор категории
    name = models.CharField(max_length=100, default='')  # название категории
    def __str__(self):
        return '{0}'.format(self.name)


# Модель Продукт - это рабочее место сотрудника или оборудование в офисе
class Product(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор продукта
    name = models.CharField(max_length=100)  # название продукта
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь с таблицей Категория
    def __str__(self):
        return '{0}'.format(self.name)
    
# Модель Заказ
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'В ожидании'),
        ('PROCESSING', 'В обработке'),
        ('COMPLETED', 'Завершен'),
        ('CANCELLED', 'Отменен'),
    ]

    id = models.AutoField(primary_key=True)  # уникальный идентификатор заказа
    date = models.DateField()  # дата заказа
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)  # статус заказа
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # связь с таблицей Сотрудник
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # связь с таблицей Продукт
    comment = models.CharField(max_length=1000)  # количество заказанных продуктов
    IdOffice = models.ForeignKey(Office, on_delete=models.CASCADE)


# Модель Комплектующие
class Components(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор комплектующего
    name = models.CharField(max_length=100, default=None)  # название комплектующего
    def __str__(self):
        return '{0}'.format(self.name)
    
# Модель Складское перемещение
class WarehouseMovement(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор
    quantity = models.IntegerField()  # количество
    IdWarehousePlus = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_plus')  # Складское перемещение плюс
    IdWarehouseMinus = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_minus')  # Складское перемещение минус
    IdComponents = models.ForeignKey(Components, on_delete=models.CASCADE, null=True, default=None)  # связь с таблицей Комплектующие
    date = models.DateTimeField()  # дата
    Comment = models.CharField(max_length=100, default ='', null=True)  # название комплектующего
    def __str__(self):
        return '{0}'.format(self.id)

# Модель Продукция Перемещение
class ProductsMovement(models.Model):
    ProductsMovement_STATUS_CHOICES = [
        ('updated', 'обновлен'),
        ('substitution', 'замена'),
    ]

    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)  # Добавляем поле datetime
    quantity = models.IntegerField()
    IdComponents = models.ForeignKey(Components, on_delete=models.CASCADE)
    IdProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    IdWarehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=ProductsMovement_STATUS_CHOICES, default='updated')

    def __str__(self):
        return '{0}'.format(self.id)

