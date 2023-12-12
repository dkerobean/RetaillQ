from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import CustomUser, Sale, Products, Expense
from .serializers import SaleSerializer, ExpenseSerializer
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


class ExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expense = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data if expense else [], status=status.HTTP_200_OK)

    
