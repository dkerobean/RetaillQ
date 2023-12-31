# Generated by Django 4.2.7 on 2023-11-10 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=150)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('organization_name', models.CharField(max_length=50)),
                ('organization_id', models.IntegerField(default=user.utils.generate_organization_id)),
                ('country', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='user.profile'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
