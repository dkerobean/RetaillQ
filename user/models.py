from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
import uuid
from .utils import generate_organization_id


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class Profile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE,
                                related_name='profiles')
    profile_id = models.UUIDField(default=uuid.uuid4, unique=True,
                                  editable=False)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    organization_id = models.IntegerField(default=generate_organization_id)
    mobile_number = models.CharField(max_length=20)
    address = models.CharField(max_length=70, null=True, blank=True)
    business_type = models.CharField(max_length=70, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    organization_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,
                                   null=True, blank=True,
                                   related_name='user_profile')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10,
                                        choices=[('income', 'Income'),
                                                 ('expense', 'Expense')])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
