from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import (CustomUser, Profile, Transaction,
                     Products, Sale, Expense, ExpenseCategory, Subscription)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')} # noqa
        ), # noqa
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(Transaction)
admin.site.register(Products)
admin.site.register(Sale)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(Subscription)
