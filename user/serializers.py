from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def validate(self, data):
            """ Validate the password and password confirmation fields match """

            password = data.get('password')
            password_confirmation = data.get('password_confirmation')

            if password and password_confirmation and password != password_confirmation:
                raise serializers.ValidationError("Passwords do not match.")

            return data

        def create(self, validated_data):
            """ Create a new user """

            user = CustomUser.objects.create(
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
