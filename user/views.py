
from rest_framework import generics
from rest_framework.response import Response
from .serializers import (UserRegistrationSerializer,
                          TrasactionSerializer, UserProfileSerializer)
from rest_framework import status
from .models import Transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


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


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profiles
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.profiles

        if request.user != profile.user:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionView(generics.ListAPIView):

    queryset = Transaction.objects.all()
    serializer_class = TrasactionSerializer
