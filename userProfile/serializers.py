from tkinter import ALL
from rest_framework import serializers
from product.serializers import ResDomainSerializer, HostDomainSerializer, SharedHostingSerializer, VPSSerializer
from userProfile.models import Profile, CompanyProfile, FinanicalResponse, TechnicalResponse
from django.contrib.auth.models import User

class FinanicalResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanicalResponse
        fields = [
            'user',
            'financial_name',
            'phone',
            'email',
        ]
        read_only_fields = ['user']

    # financial_name = serializers.CharField()
    # phone = serializers.CharField()
    # email= serializers.CharField()

class TechnicalResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalResponse
        fields = [
            'user',
            'technical_name',
            'phone',
            'email',
        ]
        read_only_fields = ['user']
    # technical_name = serializers.CharField()
    # phone = serializers.CharField()
    # email= serializers.CharField()

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            'user',
            'customer_type',
            'customer_name',
            'country',
            'phone',
            'email',
        ]
        read_only_fields = ['user']
    # get_type = serializers.CharField()
    # customer_name = serializers.CharField()
    # country = serializers.CharField()
    # phone = serializers.CharField()
    # email = serializers.EmailField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'botpress',
            'facebook',
            'telegram',
            'gender',
            'is_complete'
        ]
        read_only_fields = ['user']
    # fbName = serializers.CharField(read_only=True)
    # telegram = serializers.CharField(read_only=True)
    # get_gender = serializers.CharField(read_only=True)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    profile = ProfileSerializer(read_only=True)
    companyprofile = CompanyProfileSerializer(read_only=True)
    technicalresponse = TechnicalResponseSerializer(read_only=True)
    finanicalresponse = FinanicalResponseSerializer(read_only=True)
    services = serializers.SerializerMethodField(read_only=True)

    def get_services(self, obj):
        resdomain_qs = obj.resdomain_set.all().filter(user=obj.id)
        hostdomain_qs = obj.hostdomain_set.all().filter(user=obj.id)
        sharedhosting_qs = obj.sharedhosting_set.all().filter(user=obj.id)
        vps_qs = obj.vps_set.all().filter(user=obj.id)
        return {
            'resdomain': ResDomainSerializer(resdomain_qs,read_only=True,many=True,context=self.context).data,
            'hostdomain': HostDomainSerializer(hostdomain_qs,read_only=True,many=True,context=self.context).data,
            'sharedhosting': SharedHostingSerializer(sharedhosting_qs,read_only=True,many=True,context=self.context).data,
            'vps': VPSSerializer(vps_qs,read_only=True,many=True,context=self.context).data,
        }

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields=[
            'id',
            'username',
        ]

class BotpressUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1