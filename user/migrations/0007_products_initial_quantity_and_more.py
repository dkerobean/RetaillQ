# Generated by Django 4.2.7 on 2023-12-08 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='initial_quantity',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='remaining_percentage',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=5),
        ),
    ]
