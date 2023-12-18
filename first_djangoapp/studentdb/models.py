from django.db import models

# Create your models here.

# Модель Склад
class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор склада
    address = models.CharField(max_length=255)  # адрес склада
    phone = models.CharField(max_length=20, null=True)  # телефонный номер склада
    def __str__(self):
        return 'addres - {0}'.format(self.address)

# Модель Офис
class Office(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор офиса
    address = models.CharField(max_length=255)  # адрес офиса
    area = models.IntegerField()  # площадь офиса в квадратных метрах
    phone = models.CharField(max_length=20, null=True)  # телефонный номер офиса
    def __str__(self):
        return 'addres - {0}'.format(self.address)

# Модель Сотрудник
class Employee(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор сотрудника
    name = models.CharField(max_length=50)  # имя сотрудника
    lastName = models.CharField(max_length=50)  # фамилия сотрудника

# Модель Категория
class Category(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор категории
    name = models.CharField(max_length=100)  # название категории
    def __str__(self):
        return 'name - {0}'.format(self.name)


# Модель Продукт - это рабочее место сотрудника или оборудование в офисе
class Product(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор продукта
    name = models.CharField(max_length=100)  # название продукта
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь с таблицей Категория
    def __str__(self):
        return 'name - {0}'.format(self.name)
    
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
    quantity = models.IntegerField()  # количество заказанных продуктов

# Модель Комплектующие
class Components(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор комплектующего
    name = models.CharField(max_length=100)  # название комплектующего
    def __str__(self):
        return 'name - {0}'.format(self.name)

# Модель Прибытие компонентов
class ArrivalOfComponents(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор
    IdComponents = models.ForeignKey(Components, on_delete=models.CASCADE)  # связь с таблицей Комплектующие
    date = models.DateField()  # дата
    quantity = models.IntegerField()  # количество
    IdWarehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # связь с таблицей Склад
    def __str__(self):
        return 'id - {0}'.format(self.id)

# Модель Складское перемещение
class WarehouseMovement(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор
    name = models.CharField(max_length=100)  # имя
    quantity = models.IntegerField()  # количество
    IdWarehousePlus = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_plus')  # Складское перемещение плюс
    IdWarehouseMinus = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_minus')  # Складское перемещение минус
    date = models.DateField()  # дата
    def __str__(self):
        return 'id - {0}'.format(self.id)

# Модель Из комплектующего
class Complimentary(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор
    IdWarehousePlus = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='complimentary_plus')  # Складское перемещение плюс
    IdWarehouseMinus = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='complimentary_minus')  # Складское перемещение минус
    date = models.DateField()  # дата
    quantity = models.IntegerField()  # количество
    IdComponents = models.ForeignKey(Components, on_delete=models.CASCADE)  # связь с таблицей Комплектующие
    def __str__(self):
        return 'id - {0}'.format(self.id)

# Модель Движение из продукта
class MotionFromProduct(models.Model):
    id = models.AutoField(primary_key=True)  # уникальный идентификатор
    IdProduct = models.ForeignKey(Product, on_delete=models.CASCADE)  # связь с таблицей Продукт
    IdEmployee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # связь с таблицей Сотрудник
    IdOffice = models.ForeignKey(Office, on_delete=models.CASCADE)  # связь с таблицей Офис
    date = models.DateField()  # дата
    quantity = models.IntegerField()  # количество
    IdComponents = models.ForeignKey(Components, on_delete=models.CASCADE, default=1)  # связь с таблицей Комплектующие
    IdWarehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, default=1)  # связь с таблицей Склад
    def __str__(self):
        return 'id - {0}'.format(self.id)