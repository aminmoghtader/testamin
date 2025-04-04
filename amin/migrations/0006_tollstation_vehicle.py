# Generated by Django 5.1.7 on 2025-04-03 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amin', '0005_alter_carlocation_car_delete_toll'),
    ]

    operations = [
        migrations.CreateModel(
            name='TollStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('toll_per_cross', models.PositiveIntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.PositiveIntegerField(unique=True)),
                ('owner_national_code', models.CharField(max_length=10, unique=True)),
                ('vehicle_type', models.CharField(choices=[('car', 'Car'), ('truck', 'Truck'), ('bus', 'Bus')], max_length=10)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('distance_to_nearest_toll', models.PositiveIntegerField(blank=True, null=True)),
                ('unpaid_toll', models.PositiveIntegerField(default=0)),
                ('overdue_toll', models.PositiveIntegerField(default=0)),
                ('nearest_toll', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='amin.tollstation')),
            ],
        ),
    ]
