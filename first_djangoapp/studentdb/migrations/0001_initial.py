# Generated by Django 3.2.12 on 2024-01-11 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Components',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=100)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=255)),
                ('area', models.IntegerField()),
                ('phone', models.CharField(max_length=20, null=True)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('hidden', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.category')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseMovement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('Comment', models.CharField(default='', max_length=100, null=True)),
                ('IdComponents', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='studentdb.components')),
                ('IdWarehouseMinus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_minus', to='studentdb.warehouse')),
                ('IdWarehousePlus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_plus', to='studentdb.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='ProductsMovement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('updated', 'обновлен'), ('substitution', 'замена')], default='updated', max_length=100)),
                ('IdComponents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.components')),
                ('IdProduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.product')),
                ('IdWarehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('PENDING', 'В ожидании'), ('PROCESSING', 'В обработке'), ('COMPLETED', 'Завершен'), ('CANCELLED', 'Отменен')], max_length=10)),
                ('comment', models.CharField(max_length=1000)),
                ('hidden', models.BooleanField(default=False)),
                ('IdOffice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.office')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.employee')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.product')),
            ],
        ),
    ]