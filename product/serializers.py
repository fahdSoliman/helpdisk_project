from rest_framework import serializers
from .models import VPS, HostDomain, Product, ResDomain, SharedHosting
from django.utils.html import strip_tags


class TypeSerializer(serializers.Serializer):
    type_name = serializers.CharField(read_only=True)
    des_file = serializers.FileField(read_only=True)
    products = serializers.SerializerMethodField(read_only=True)

    def get_products(self, obj):
        product = obj
        the_products_qs = product.product_set.all()
        return ProductSerializer(the_products_qs, many=True, context=self.context).data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # read_only_fiields = '__all__'

class HostDomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = HostDomain
        fields = [
            'user',
            'my_product',
            'domain_name',
            'ip_address',
            'note',
            'bill_file',
        ]
        read_only_fields = [
            'id',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
        ]

class ResDomainSerializer(serializers.ModelSerializer):
    clean_note = serializers.SerializerMethodField()
    class Meta:
        model = ResDomain
        fields = [
            'user',
            'my_product',
            'domain_name',
            'activate',
            'primary_name_server',
            'secondary_name_server',
            'hosting_company',
            'bill_file',
            'note',
            'clean_note'
        ]
        read_only_fields = [
            'id',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
        ]
    def get_clean_note(self, opj):
        return strip_tags(opj.note)


class SharedHostingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SharedHosting
        fields = [
            'user',
            'my_product',
            'website_name',
            'operation',
            'transfer_website',
            'backup_website',
            'bill_file',
            'note',
        ]
        read_only_fields = [
            'id',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
        ]

class VPSSerializer(serializers.ModelSerializer):

    class Meta:
        model = VPS
        fields= [
            'user',
            'my_product',
            'website_name',
            'operation_system',
            'ip_address',
            'ip_count',
            'port_numbers',
            'data_transfer',
            'data_backup',
            'bill_file',
            'note',
        ]
        read_only_fields = [
            'id',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
        ]
