# Generated by Django 4.2.7 on 2024-01-25 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_alter_products_total_quantity_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
