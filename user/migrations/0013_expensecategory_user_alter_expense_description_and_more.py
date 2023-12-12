# Generated by Django 4.2.7 on 2023-12-12 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_expensecategory_alter_sale_status_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensecategory',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expensecategory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
