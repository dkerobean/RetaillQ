# Generated by Django 4.2.7 on 2024-01-03 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_expense_expense_date_transaction_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='currency_symbol',
            field=models.CharField(blank=True, default='$', max_length=5, null=True),
        ),
    ]
