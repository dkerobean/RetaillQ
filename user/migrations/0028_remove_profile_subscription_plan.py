# Generated by Django 4.2.7 on 2024-01-04 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_remove_subscription_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='subscription_plan',
        ),
    ]