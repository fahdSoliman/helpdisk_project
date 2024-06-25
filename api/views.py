from api.permissions import isBotpressPermission
from product.models import Product, Type, ResDomain, HostDomain, SharedHosting, VPS
from product.serializers import TypeSerializer, ProductSerializer, ResDomainSerializer, HostDomainSerializer, SharedHostingSerializer, VPSSerializer
from userProfile.serializers import UserReservationsSerializer , TechnicalResponseSerializer, FinanicalResponseSerializer, CompanyProfileSerializer, ProfileSerializer, UserSerializer
from userProfile.models import Profile, CompanyProfile, FinanicalResponse, TechnicalResponse
from django.contrib.auth.models import User
from rest_framework import generics, mixins
from .authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication

##################################
# All Product Info Retrieve View #
##################################

class ProductListView(generics.RetrieveAPIView):
    queryset = Type.objects.all()
    lookup_field = 'type_name'
    serializer_class = TypeSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

Type_list_view = ProductListView.as_view()


######################################
# User objects Retrieve/Update Views #
######################################

class UserRetrieveView(generics.RetrieveAPIView):
    '''
    view for retrieve all the user information based on the ID given,
    for read only and view all by side the services was registred by the user,
    and all that for more base-info for botpress bot.
    Methods: GET
    '''
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

User_Retrieve_View = UserRetrieveView.as_view()

class UserRetrieveView2(generics.RetrieveAPIView):
    '''
    view for retrieve all the user information based on the Username given,
    for read only and view all by side the services was registred by the user,
    and all that for more base-info for botpress bot.
    Methods: GET
    '''
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

User_Retrieve_View2 = UserRetrieveView2.as_view()

class UserReservationsRetrieveView(generics.RetrieveAPIView):
    '''
    view for retrieve all the user information based on the ID given,
    for read only and view all by side the services was registred by the user,
    and all that for more base-info for botpress bot.
    Methods: GET
    '''
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserReservationsSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

User_Reservations_Retrieve_View = UserReservationsRetrieveView.as_view()


class UserBotpressRetrieveView(generics.RetrieveAPIView):
    '''
    view for retrieve all the user information based on the botpress id 
    to be proactive.
    Methods: GET
    '''
    queryset = Profile.objects.all()
    lookup_field = 'botpress'
    serializer_class = ProfileSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

User_Botpress_Retrieve_View = UserBotpressRetrieveView.as_view()


class UserUpdateProfileView(
    generics.RetrieveUpdateAPIView
    ):
    '''
    View for retrieve/update Profile model connected to the user by a given user_ID.
    Methods: GET, PUT
    '''
    queryset = Profile.objects.all()
    lookup_field = 'user'
    serializer_class = ProfileSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

Use_Profile_View = UserUpdateProfileView.as_view()


class UserCompanyProfileView(generics.RetrieveUpdateAPIView):
    '''
    View for Retrieve/Update only CompanyProfile model connected with a given User.
    Methods: GET, PUT
    '''
    queryset = CompanyProfile.objects.all()
    lookup_field = 'user'
    serializer_class = CompanyProfileSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

User_CompanyProfile_View = UserCompanyProfileView.as_view()


class UserFinanicalResponseView(generics.RetrieveUpdateAPIView):
    '''
    View for Retrieve/Update only FinResponse model connected with a given User.
    Methods: GET, PUT
    '''
    queryset = FinanicalResponse.objects.all()
    lookup_field = 'user'
    serializer_class = FinanicalResponseSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

User_FinanicalResponse_View = UserFinanicalResponseView.as_view()


class UserTechnicalResponseView(generics.RetrieveUpdateAPIView):
    '''
    View for Retrieve/Update only TechResponse model connected with a given User.
    Methods: GET, PUT
    '''
    queryset = TechnicalResponse.objects.all()
    lookup_field = 'user'
    serializer_class = TechnicalResponseSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

User_TechResponse_View = UserTechnicalResponseView.as_view()


class UserTelegramView(generics.RetrieveAPIView):
    '''
    View to search of user using telegram field.
    Methods: GET
    '''
    queryset = Profile.objects.all()
    lookup_field = 'telegram'
    serializer_class = ProfileSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
User_Telegram_View = UserTelegramView.as_view()

######################################################
# Services Reservations Retrieve/Update/Create Views #
######################################################


class ResDomainAPI(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    '''
    API for Retrieve/Update/Create Reservation Domain Instance.
    Methods: GET, PUT, POST
    '''
    queryset = ResDomain.objects.all()
    lookup_field = 'id'
    serializer_class = ResDomainSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)

ResDomain_Retrieve_Update_API = ResDomainAPI.as_view()


class HostDomainAPI(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    '''
    API for Retrieve/Update/Create Hosting Domain Instance.
    Methods: GET, PUT, POST
    '''
    queryset = HostDomain.objects.all()
    lookup_field = 'id'
    serializer_class = HostDomainSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)

HostDomain_Retrieve_Update_API = HostDomainAPI.as_view()


class SharedHostingAPI(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    '''
    API for Retrieve/Update/Create Shared Hosting Instance.
    Methods: GET, PUT, POST
    '''
    queryset = SharedHosting.objects.all()
    lookup_field = 'id'
    serializer_class = SharedHostingSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)

Shared_Retrieve_Update_API = SharedHostingAPI.as_view()


class VPS_API(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    '''
    API for Retrieve/Update/Create Virtual Private Server Hosting Instance.
    Methods: GET, PUT, POST
    '''
    queryset = VPS.objects.all()
    lookup_field = 'id'
    serializer_class = VPSSerializer
    permission_classes = [isBotpressPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)

VPS_Retrieve_Update_API = VPS_API.as_view()