# Generated by Django 4.2.7 on 2023-12-08 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_products_initial_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='initial_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]