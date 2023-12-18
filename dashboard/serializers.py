from rest_framework import serializers


class IncomeExpenseSerializer(serializers.Serializer):
   income = serializers.DecimalField(max_digits=10, decimal_places=2)
   expense = serializers.DecimalField(max_digits=10, decimal_places=2)
   sales = serializers.DecimalField(max_digits=10, decimal_places=2)



