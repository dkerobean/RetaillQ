from rest_framework import serializers
from user.models import Sale, Expense


class SaleSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'user', 'user_name', 'user_profile_image', 'product', 'product_name', 'quantity_sold', 'sale_date', 'total', 'status']

    def get_user_name(self, obj):
        print(obj)
        print(obj.user)
        return obj.user.profiles.name if obj.user.profiles else ''

    def get_user_profile_image(self, obj):
        return obj.user.profiles.avatar.url if obj.user.profiles and obj.user.profiles.avatar else ''

    def get_product_name(self, obj):
        return obj.product.name if obj.product else ''


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
