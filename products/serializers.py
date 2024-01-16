from rest_framework import serializers
from user.models import Products, Delivery


class ProductsSerializer(serializers.ModelSerializer):

    currency = serializers.CharField(source='user.profiles.currency_symbol',
                                     read_only=True)

    class Meta:
        model = Products
        fields = '__all__'
        extra_kwargs = {'product_id': {'write_only': True}}


class ProductListSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='user.profiles.currency_symbol',
                                     read_only=True)

    class Meta:
        model = Products
        fields = ['name', 'price', 'remaining_percentage', 'currency']


class DeliverySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()
    product = ProductListSerializer()

    class Meta:
        model = Delivery
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.user.profiles.name if obj.user.profiles else ''

    def get_user_profile_image(self, obj):
        return obj.user.profiles.avatar.url if obj.user.profiles and obj.user.profiles.avatar else '' # noqa


class DeliveryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = '__all__'
