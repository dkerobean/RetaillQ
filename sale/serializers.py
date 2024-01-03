from rest_framework import serializers
from user.models import Sale, Expense, ExpenseCategory, Transaction


class SaleSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='user.profile.currency_symbol', read_only=True)
    user_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'user', 'user_name', 'user_profile_image',
                  'product', 'product_name', 'quantity_sold', 'sale_date',
                  'total', 'status', 'currency']

    def get_user_name(self, obj):
        print(obj)
        print(obj.user)
        return obj.user.profiles.name if obj.user.profiles else ''

    def get_user_profile_image(self, obj):
        return obj.user.profiles.avatar.url if obj.user.profiles and obj.user.profiles.avatar else '' # noqa

    def get_product_name(self, obj):
        return obj.product.name if obj.product else ''


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='user.profiles.currency_symbol', read_only=True)
    user_name = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description',
                  'created_at', 'user', 'user_profile_image',
                  'user_name', 'category_name', 'category', 'expense_date', 'currency']

    def get_user_name(self, obj):
        return obj.user.profiles.name if obj.user.profiles else ''

    def get_user_profile_image(self, obj):
        return obj.user.profiles.avatar.url if obj.user.profiles and obj.user.profiles.avatar else '' # noqa

    def get_category_name(self, obj):
        return obj.category.name if obj.category else ''


class TransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()
    currency = serializers.CharField(source='user.profiles.currency_symbol', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.user.profiles.name if obj.user.profiles else ''

    def get_user_profile_image(self, obj):
        return obj.user.profiles.avatar.url if obj.user.profiles and obj.user.profiles.avatar else '' # noqa
