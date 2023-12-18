from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import Transaction, Expense, Sale
from .serializers import IncomeExpenseSerializer
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


        data = {
            'income': total_income,
            'expense': total_expense,
            'sales': sales
        }

        serializer = IncomeExpenseSerializer(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
