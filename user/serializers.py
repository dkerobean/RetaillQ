from rest_framework import serializers
from .models import CustomUser, Transaction, Profile


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
                organization_name=validated_data['organization_name'],
                email=validated_data['email'],
                password=validated_data['password'],
                country=validated_data['country']
            )
            return user


class TrasactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = fields = ['name', 'display_name', 'avatar', 'mobile_number', 'address', 'business_type']
