# Generated by Django 5.0.13 on 2025-06-25 05:51

import django.db.models.deletion
import utils.functions
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('tenant_id', models.CharField(default=None, max_length=128, null=True)),
                ('created_by', models.CharField(default=None, max_length=128, null=True)),
                ('updated_by', models.CharField(default=None, max_length=128, null=True)),
                ('updated_dtm', models.DateTimeField(auto_now=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('deleted_dtm', models.DateTimeField(default=None, null=True)),
                ('product_id', models.CharField(default=utils.functions.get_uuid, max_length=36, primary_key=True, serialize=False)),
                ('product_code', models.CharField(max_length=256)),
                ('product_name', models.CharField(max_length=256)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
