from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import Products
from .serializers import ProductsSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):

        permission_classes = [IsAuthenticated]  # noqa

        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        permission_classes = [IsAuthenticated] # noqa

        product = Products.objects.get(id=pk)

        if request.user != product.user:
            return Response({'error': 'You are not authorized to take this action'}, status=status.HTTP_403_FORBIDDEN) # noqa

        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        permission_classes = [IsAuthenticated] # noqa

        product = Products.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
