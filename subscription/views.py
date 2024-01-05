from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data if subscriptions else [], status=status.HTTP_200_OK)
