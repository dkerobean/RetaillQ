from rest_framework import serializers
from user.models import Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        extra_kwargs = {'product_id': {'write_only': True}}
