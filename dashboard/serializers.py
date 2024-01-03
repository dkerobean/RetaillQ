from rest_framework import serializers
from user.models import Transaction, Expense, ExpenseCategory


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'created_at', 'transaction_type']


class IncomeExpenseSerializer(serializers.Serializer):
    income = serializers.DecimalField(max_digits=10, decimal_places=2)
    expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    profit = serializers.DecimalField(max_digits=10, decimal_places=2)
    products_sold = serializers.DecimalField(max_digits=10, decimal_places=2)
    cash_flow = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()


class ProductsSerializer(serializers.Serializer):
    top_selling_products = serializers.DecimalField(max_digits=10,
                                                    decimal_places=2)
    start_of_month_five_months_ago = serializers.DecimalField(max_digits=10,
                                                              decimal_places=2)


# Expense
class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'description', 'created_at']


class ExpenseSerializer(serializers.ModelSerializer):
    category = ExpenseCategorySerializer()

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount',
                  'category', 'description', 'created_at']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, created = ExpenseCategory.objects.get_or_create(**category_data)  # noqa
        expense = Expense.objects.create(category=category, **validated_data)
        return expense

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        category, created = ExpenseCategory.objects.get_or_create(**category_data) # noqa

        instance.amount = validated_data.get('amount', instance.amount)
        instance.category = category
        instance.description = validated_data.get('description', instance.description) # noqa

        instance.save()
        return instance


class IncomeExpenseSerializerDashboard(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=10, decimal_places=2)
    expense = serializers.DecimalField(max_digits=10, decimal_places=2)
