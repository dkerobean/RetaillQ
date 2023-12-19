from rest_framework import serializers


class IncomeExpenseSerializer(serializers.Serializer):
   income = serializers.DecimalField(max_digits=10, decimal_places=2)
   expense = serializers.DecimalField(max_digits=10, decimal_places=2)
   sales = serializers.DecimalField(max_digits=10, decimal_places=2)
   profit = serializers.DecimalField(max_digits=10, decimal_places=2)
   products_sold = serializers.DecimalField(max_digits=10, decimal_places=2)
   cash_flow = serializers.DecimalField(max_digits=10, decimal_places=2)


class ProductsSerializer(serializers.Serializer):
   top_selling_products = serializers.DecimalField(max_digits=10, decimal_places=2)




