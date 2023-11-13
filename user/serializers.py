from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['organization_name', 'country', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def validate(self, data):
            """
            Validate the password and password confirmation fields match
            """

            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if password and confirm_password and password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")

            return data

        def create(self, validated_data):
            """ Create a new user """

            user = CustomUser.objects.create(
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
