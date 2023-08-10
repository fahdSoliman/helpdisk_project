from rest_framework import serializers
from product.models import Product, Type
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'product_type',
            'product_img',
            'pub_date',
            'updated',
            'product_description',
            'product_specification',
            'product_file',
            'year_fees',

        ]
    # def create(self, validate_data):
    #     return Product.objects.create(validate_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]