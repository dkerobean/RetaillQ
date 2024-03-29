from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import Transaction, Expense, Sale, Products
from .serializers import (IncomeExpenseSerializer, ProductsSerializer,
                          TransactionSerializer,
                          IncomeExpenseSerializerDashboard)
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.utils import timezone


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
            user=user, transaction_type='expense',
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

        currency_symbol = user.profiles.currency_symbol

        data = {
            'income': total_income,
            'expense': total_expense,
            'sales': sales,
            'profit': profit,
            'products_sold': products_sold,
            'cash_flow': cash_flow,
            'currency': currency_symbol,
        }

        serializer = IncomeExpenseSerializer(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        currency = user.profiles.currency_symbol

        # Get unique products with the highest total sold for the current user
        top_selling_products = Sale.objects.filter(user=user,
                                                   status='completed')\
            .values('product__id', 'product__name')\
            .annotate(total_sold=Sum('quantity_sold'))\
            .order_by('-total_sold')[:4]

        # Fetch additional details for each unique product
        top_selling_products_details = []
        for product_data in top_selling_products:
            product = Products.objects.get(id=product_data['product__id'])
            remaining_percentage = (product.quantity / product.initial_quantity) * 100  # noqa
            product_data['total'] = product_data['total_sold'] * product.price
            product_data['product__remaining_percentage'] = remaining_percentage  # noqa
            product_data['quantity_sold'] = product_data['total_sold']

            top_selling_products_details.append(product_data)

        data = {
            "top_selling_products": top_selling_products_details,
            "currency": currency,
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


class ExpenseCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        # Get the current date
        today = timezone.now()

        # Calculate the start and end dates for this month
        start_of_month = today.replace(day=1, hour=0, minute=0,
                                       second=0, microsecond=0)
        end_of_month = (start_of_month + timezone.timedelta(days=32)
                        ).replace(day=1, microsecond=0)

        # ... (similar calculations for other time periods)

        # Retrieve expenses by categories for this month
        this_month_expenses = Expense.objects.filter(
            user=user,
            expense_date__range=(start_of_month, end_of_month),
        ).values('category__name').annotate(total_amount=Sum('amount'))

        # Retrieve transactions as expenses by categories for this month
        this_month_transactions = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            transaction_date__range=(start_of_month, end_of_month),
        ).values('description').annotate(total_amount=Sum('amount'))

        # Combine expenses and transactions data for this month
        this_month_expenses = this_month_expenses.union(this_month_transactions)  # noqa

        # Retrieve expenses by categories for last month
        start_of_last_month = (start_of_month - timezone.timedelta(days=1)
                               ).replace(day=1)
        end_of_last_month = start_of_month

        last_month_expenses = Expense.objects.filter(
            user=user,
            expense_date__range=(start_of_last_month, end_of_last_month),
        ).values('category__name').annotate(total_amount=Sum('amount'))

        # Retrieve transactions as expenses by categories for last month
        last_month_transactions = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            transaction_date__range=(start_of_last_month, end_of_last_month),
        ).values('description').annotate(total_amount=Sum('amount'))

        # Combine expenses and transactions data for last month
        last_month_expenses = last_month_expenses.union(last_month_transactions)  # noqa

        # Retrieve expenses by categories for this year
        start_of_year = today.replace(month=1, day=1, hour=0,
                                      minute=0, second=0, microsecond=0)
        end_of_year = (start_of_year + timezone.timedelta(days=366)
                       ).replace(day=1, microsecond=0)

        this_year_expenses = Expense.objects.filter(
            user=user,
            expense_date__range=(start_of_year, end_of_year),
        ).values('category__name').annotate(total_amount=Sum('amount'))

        # Retrieve transactions as expenses by categories for this year
        this_year_transactions = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            transaction_date__range=(start_of_year, end_of_year),
        ).values('description').annotate(total_amount=Sum('amount'))

        # Combine expenses and transactions data for this year
        this_year_expenses = this_year_expenses.union(this_year_transactions)

        # Retrieve expenses by categories for this quarter
        current_quarter = (today.month - 1) // 3 + 1
        start_of_quarter = today.replace(month=(current_quarter - 1) * 3 + 1,
                                         day=1, hour=0, minute=0, second=0,
                                         microsecond=0)
        end_of_quarter = (start_of_quarter + timezone.timedelta(days=95)
                          ).replace(day=1, microsecond=0)

        this_quarter_expenses = Expense.objects.filter(
            user=user,
            expense_date__range=(start_of_quarter, end_of_quarter),
        ).values('category__name').annotate(total_amount=Sum('amount'))

        # Retrieve transactions as expenses by categories for this quarter
        this_quarter_transactions = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            transaction_date__range=(start_of_quarter, end_of_quarter),
        ).values('description').annotate(total_amount=Sum('amount'))

        # Combine expenses and transactions data for this quarter
        this_quarter_expenses = this_quarter_expenses.union(this_quarter_transactions)  # noqa

        # Organize data in the desired format
        result = {
            'this_month': this_month_expenses,
            'last_month': last_month_expenses,
            'this_year': this_year_expenses,
            'this_quarter': this_quarter_expenses,
        }

        return Response(result, status=status.HTTP_200_OK)


class IncomeExpenseDashboardView(APIView):
    def get(self, request):
        # Get the requested year from the query parameters
        requested_year = request.query_params.get('year', datetime.now().year)

        # Create a list to store results for each month
        result_list = []

        currency = request.user.profiles.currency_symbol

        # Calculate income vs expense for each month in the requested year
        for month in range(1, 13):  # Loop through all 12 months
            # Filter income transactions for the current user
            income_transactions = Transaction.objects.filter(
                user=request.user,
                transaction_type='income',
                transaction_date__month=month,
                transaction_date__year=requested_year
            ).aggregate(income=Sum('amount'))['income'] or 0

            # Filter completed sales for the current user
            completed_sales = Sale.objects.filter(
                user=request.user,
                status='completed',
                sale_date__month=month,
                sale_date__year=requested_year
            ).aggregate(income=Sum('total'))['income'] or 0

            # Filter expenses for the current user
            expenses = Transaction.objects.filter(
                user=request.user,
                transaction_type='expense',
                transaction_date__month=month,
                transaction_date__year=requested_year
            ).aggregate(expense=Sum('amount'))['expense'] or 0

            expenses += Expense.objects.filter(
                 user=request.user,
                 created_at__month=month,
                 created_at__year=requested_year
                 ).aggregate(sum=Sum('amount'))['sum'] or 0

            # Calculate income vs expense
            income = income_transactions + completed_sales
            expense = expenses

            # Append the result for the current month to the result_list
            result_list.append({
                'month': month,
                'year': requested_year,
                'income': income,
                'expense': expense,
                'currency': currency
            })

        # Serialize the result list
        serializer = IncomeExpenseSerializerDashboard(result_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
