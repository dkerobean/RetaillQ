# Generated by Django 4.2.7 on 2024-01-04 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_subscription_profile_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='subscription',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
