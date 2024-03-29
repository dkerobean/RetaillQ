from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
import uuid
from .utils import generate_organization_id, generate_product_id
from django.utils import timezone


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
    currency_symbol = models.CharField(max_length=5, default='$', null=True,
                                       blank=True)
    subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='user_subscriptions')

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
                                               decimal_places=0,
                                               default=100.00)
    total_quantity_sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set initial_quantity when creating a new product
        if not self.pk:
            self.initial_quantity = self.quantity

        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


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

        # Update total_quantity_sold
        self.product.total_quantity_sold += self.quantity_sold

        # Calculate the remaining  percentage
        remaining_percentage = 100 - (self.product.total_quantity_sold / self.product.initial_quantity) * 100 # noqa
        self.product.remaining_percentage = remaining_percentage

        self.product.save()

        # Call the original save method to save the Sale instance
        super(Sale, self).save(*args, **kwargs)


class Delivery(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=20, default='Pending')
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2,
                                null=True, blank=True)
    delivery_fee = models.IntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name}'s Delivery ({self.status})"


class Pickup(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('standard_monthly', 'Standard Monthly'),
        ('standard_yearly', 'Standard Yearly'),
        ('premium_monthly', 'Premium Monthly'),
        ('premium_yearly', 'Premium Yearly'),
    ]

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES,
                            default='free', unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if 'monthly' in self.plan:
            self.end_date = self.start_date + timezone.timedelta(days=30)
        elif 'yearly' in self.plan:
            self.end_date = self.start_date + timezone.timedelta(days=365)
        else:
            self.end_date = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.plan} Plan'
