from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import Products
from .serializers import ProductsSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Products.objects.filter(user=request.user)
        serializer = ProductsSerializer(products, many=True)
        # handdle case where  products is empty
        return Response(serializer.data if products else [], status=status.HTTP_200_OK) # noqa

    def post(self, request):

        permission_classes = [IsAuthenticated]  # noqa

        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        product = get_object_or_404(Products, id=pk, user=request.user)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        product = get_object_or_404(Products, id=pk, user=request.user)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductView(APIView):

    permission_classes = [IsAuthenticated]  # noqa

    def get(self, request, pk):
        try:
            product = Products.objects.get(id=pk, user=request.user)
            serializer = ProductsSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            return Response(
                {"error": f"Product with id {pk} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
