
from rest_framework import generics
from rest_framework.response import Response
from .serializers import (UserRegistrationSerializer,
                          TrasactionSerializer, UserProfileSerializer)
from rest_framework import status
from .models import Transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
import jwt


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            token = response.data.get('access')
            if token:
                user_id = self.extract_user_id_from_token(token)
                response.data['user_id'] = user_id
        return response

    def extract_user_id_from_token(self, token):
        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256']) # noqa
            return decoded_payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return None, 'Token has expired.'
            pass
        except jwt.InvalidTokenError:
            return None, 'Token has expired.'
            pass
        return None


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
            return Response({"detail": "You do not have permission to perform this action."}, # noqa
                            status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            # handle image upload
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK) # noqa
        except Exception as e: # noqa
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST) # noqa


class TransactionView(generics.ListAPIView):

    queryset = Transaction.objects.all()
    serializer_class = TrasactionSerializer
