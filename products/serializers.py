from rest_framework import serializers
from user.models import Products, Profile


class ProductsSerializer(serializers.ModelSerializer):

    currency = serializers.CharField(source='user.profiles.currency_symbol',
                                     read_only=True)
    
    class Meta:
        model = Products
        fields = '__all__'
        extra_kwargs = {'product_id': {'write_only': True}}
