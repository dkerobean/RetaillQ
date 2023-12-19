from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import Transaction, Expense, Sale
from .serializers import IncomeExpenseSerializer, ProductsSerializer
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated


class IncomeExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # calculate total income (sum of income in 'transsaction' and 'sales')
        total_income = Transaction.objects.filter(
            user=user, transaction_type='income'
        ).aggregate(sum=Sum('amount'))['sum'] or 0

        total_income += Sale.objects.filter(
            user=user, status='completed'
        ).aggregate(sum=Sum('total'))['sum'] or 0

        # calculate total expense
        total_expense = Transaction.objects.filter(
            user=user, transaction_type='income',
        ).aggregate(sum=Sum('amount'))['sum'] or 0

        total_expense += Expense.objects.filter(
            user=user
        ).aggregate(sum=Sum('amount'))['sum'] or 0

        sales = Sale.objects.filter(
            user=user, status='completed'
        ).aggregate(sum=Sum('total'))['sum'] or 0

        profit = total_income - total_expense

        # total products sold
        products_sold = Sale.objects.filter(
            user=user, status='completed'
        ).aggregate(sum=Sum('total'))['sum'] or 0

        # cashflow
        cash_flow = total_income + total_expense + sales

        data = {
            'income': total_income,
            'expense': total_expense,
            'sales': sales,
            'profit': profit,
            'products_sold': products_sold,
            'cash_flow': cash_flow,
        }

        serializer = IncomeExpenseSerializer(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        top_selling_products = Sale.objects.filter(status='completed')\
            .values('product__id', 'product__name', 'total', 'product__remaining_percentage', 'quantity_sold')\
            .annotate(total_sold=Sum('quantity_sold'))\
            .order_by('-total_sold')[:5]

        data = {
            "top_selling_products": top_selling_products,
        }

        serializer = ProductsSerializer(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


