# Generated by Django 4.2.7 on 2024-01-17 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0033_delivery_contact_number_delivery_delivery_fee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pickup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
        ),
    ]