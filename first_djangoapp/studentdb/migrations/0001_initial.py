# Generated by Django 3.2.12 on 2023-12-07 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('last_фамилия', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('salary', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('addres', models.CharField(max_length=255)),
                ('area', models.IntegerField()),
                ('phone', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=255)),
                ('area', models.IntegerField()),
                ('phone', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255, null=True)),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('wherhouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=20)),
                ('quantity', models.IntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.employee')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.product')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentdb.office'),
        ),
    ]
