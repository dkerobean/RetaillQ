# Generated by Django 4.2.7 on 2023-12-12 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.expensecategory'),
        ),
    ]
