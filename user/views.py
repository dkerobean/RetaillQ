
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, TrasactionSerializer
from rest_framework import status
from .models import Transaction


class RegistrationView(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Create a new user and set the password using the serializer.
        """

        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class TransactionView(generics.ListAPIView):

    queryset = Transaction.objects.all()
    serializer_class = TrasactionSerializer
