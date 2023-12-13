from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import Sale, Products, Expense, ExpenseCategory, Transaction
from .serializers import SaleSerializer, ExpenseSerializer, ExpenseCategorySerializer, TransactionSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class SalesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        sales = Sale.objects.filter(user=request.user)
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data if sales else [], status=status.HTTP_200_OK)

    def post(self, request):
        # Ensure the selected product belongs to the current user
        product_id = request.data.get('product')
        product = get_object_or_404(Products, id=product_id, user=request.user)

        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            # Set the product before saving the Sale instance
            serializer.validated_data['product'] = product

            # Ensure that the quantity_sold is less than or equal to the available quantity
            quantity_sold = serializer.validated_data['quantity_sold']
            if quantity_sold > product.quantity:
                return Response({'error': 'Quantity sold exceeds available quantity.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        sale = get_object_or_404(Sale, id=pk, user=request.user)
        serializer = SaleSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            sale = Sale.objects.get(id=pk, user=request.user)
            serializer = SaleSerializer(sale)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Sale.DoesNotExist:
            return Response(
                {"error": f"Product with id {pk} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ExpenseCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expense_category = ExpenseCategory.objects.filter(user=request.user)
        serializer = ExpenseCategorySerializer(expense_category, many=True)
        return Response(serializer.data if expense_category else [], status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpenseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense_category = get_object_or_404(ExpenseCategory, id=pk, user=request.user)

        serializer = ExpenseCategorySerializer(expense_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense_category = get_object_or_404(ExpenseCategory, id=pk, user=request.user)
        expense_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseCategoryView(APIView):
    def get(self, request, pk):
        expense_category = get_object_or_404(ExpenseCategory, id=pk, user=request.user)
        serializer = ExpenseCategorySerializer(expense_category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expense = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expense, many=True)
        return Response(serializer.data if expense else [], status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense = get_object_or_404(Expense, id=pk, user=request.user)
        serializer = ExpenseSerializer(expense, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, id=pk, user=request.user)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        expense = get_object_or_404(Expense, id=pk, user=request.user)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data if transactions else [], status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        transaction = get_object_or_404(Transaction, id=pk, user=request.user)

        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionView(APIView):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, id=pk, user=request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

