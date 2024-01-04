# Generated by Django 4.2.7 on 2024-01-04 11:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_subscriptionplan_subscription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='profile',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='user.profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]