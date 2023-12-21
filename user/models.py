from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
import uuid
from .utils import generate_organization_id, generate_product_id


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


class Products(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_id = models.IntegerField(default=generate_product_id)
    name = models.CharField(max_length=75)
    quantity = models.IntegerField()
    initial_quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_percentage = models.DecimalField(max_digits=5,
                                               decimal_places=2,
                                               default=100.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set initial_quantity when creating a new product
        if not self.pk:
            self.initial_quantity = self.quantity

        super(Products, self).save(*args, **kwargs)


class ExpenseCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory,
                                 on_delete=models.SET_NULL, null=True)
    expense_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10,
                                        choices=[('income', 'Income'),
                                                 ('expense', 'Expense')])
    transaction_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Sale(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sale_date = models.DateField()
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES, default='completed')
    total = models.DecimalField(max_digits=10, decimal_places=2,
                                null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        self.total = self.product.price * self.quantity_sold

        # Deduct quantity_sold from the product quantity
        self.product.quantity -= self.quantity_sold

        # Calculate the remaining  percentage
        remaining_percentage = (self.product.quantity / self.product.initial_quantity) * 100  # noqa
        self.product.remaining_percentage = remaining_percentage

        self.product.save()

        # Call the original save method to save the Sale instance
        super(Sale, self).save(*args, **kwargs)
