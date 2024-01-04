# Generated by Django 4.2.7 on 2024-01-04 18:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_remove_subscription_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]