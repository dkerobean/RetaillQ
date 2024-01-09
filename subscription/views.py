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


class UpgradeSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        new_plan = request.data.get('new_plan')

        # Ensure the new plan is valid
        if new_plan not in ['standard', 'premium']:
            return Response({'error': 'Invalid subscription plan'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user's profile
        profile = user.profiles

        # Fetch the selected subscription plan
        subscription = Subscription.objects.get(plan='premium_monthly')

        # Update the user's subscription
        profile.subscription = subscription
        profile.save()

        return Response({'message': 'Subscription upgraded successfully'},
                        status=status.HTTP_200_OK)
