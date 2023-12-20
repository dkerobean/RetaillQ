from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import Transaction, Expense, Sale, Products
from .serializers import IncomeExpenseSerializer, ProductsSerializer, TransactionSerializer
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

        # Get unique products with the highest total sold, considering only completed sales
        top_selling_products = Sale.objects.filter(status='completed')\
            .values('product__id', 'product__name')\
            .annotate(total_sold=Sum('quantity_sold'))\
            .order_by('-total_sold')[:4]

        # Fetch additional details for each unique product
        top_selling_products_details = []
        for product_data in top_selling_products:
            product = Products.objects.get(id=product_data['product__id'])
            remaining_percentage = (product.quantity / product.initial_quantity) * 100
            product_data['total'] = product_data['total_sold'] * product.price
            product_data['product__remaining_percentage'] = remaining_percentage
            product_data['quantity_sold'] = product_data['total_sold']

            top_selling_products_details.append(product_data)

        data = {
            "top_selling_products": top_selling_products_details,
        }

        serializer = ProductsSerializer(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        transactions = Transaction.objects.order_by('-created_at')[:5]
        serializer = TransactionSerializer(data=transactions, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)




