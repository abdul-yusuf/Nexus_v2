from email.headerregistry import Address
from rest_framework import serializers
from .models import User
from .utills import send_mail, send_msg
from rest_framework.authtoken.models import Token
from rest_auth.registration.serializers import RegisterSerializer
from store.serializers import VendorSerializer
from core.serializers import AddressSerializer

from allauth.account.utils import user_email

# from django.http import HttpRequest
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError as DjangoValidationError


try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

import re

email_regx = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')

class UserSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(many=False)
    address_set = AddressSerializer(many=True)
    class Meta:
        model = User
        # fields = ('pk','username','email','address','is_vendor','password')
        fields = '__all__'
        extra_kwargs = {'password':{'write_only': True}}
        read_only_fields = ('pk','email','username')

    def create(self, validated_data):
        # address = 
        user = User(
            email = validated_data['email'],
            username = validated_data['phone_no'],
            # phone_no = validated_data['phone_no'],
            # address = validated_data['address'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class UserRegSerializer(
                            # RegisterSerializer,
                            # serializers.Serializer,
                            serializers.ModelSerializer
                            ):

    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=True)
    # password1 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('pk','username','email','password')
        extra_kwargs = {'password':{'write_only': True}}

    # def create(self, validated_data):
    #     # address = 
    #     user = User(
    #         email = validated_data['email'],
    #         username = validated_data['username'],
    #         # phone_no = validated_data['phone_no'],
    #         # address = validated_data['address'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     user_email(user, self.email)
    #     Token.objects.create(user=user)
    #     return user


    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        # if data['password1'] != data['password2']:
        #     raise serializers.ValidationError(("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        
        # adapter.clean_password(self.cleaned_data['password'], user=user)
        user.set_password(self.cleaned_data['password'])
    
        print(user,adapter,'=====',self.cleaned_data)
        user.save()
        # send_mail(user, '12892')
        # self.custom_signup(request, user)
        # setup_user_email(request, user, [])
        return user  
  






# def user_email(user, email):
#     print(user,email)
    # username = serializers.CharField(
    #     max_length=get_username_max_length(),
    #     min_length=allauth_settings.USERNAME_MIN_LENGTH,
    #     required=allauth_settings.USERNAME_REQUIRED,
    # )
    # email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    # password1 = serializers.CharField(write_only=True)
    # # password2 = serializers.CharField(write_only=True)

    # def validate_username(self, username):
    #     username = get_adapter().clean_username(username)
    #     return username

    # def validate_email(self, email):
    #     email = get_adapter().clean_email(email)
    #     if allauth_settings.UNIQUE_EMAIL:
    #         if email and email_address_exists(email):
    #             raise serializers.ValidationError(
    #                 _('A user is already registered with this e-mail address.'),
    #             )
    #     return email

    # def validate_password1(self, password):
    #     return get_adapter().clean_password(password)

    # def validate(self, data):
    #     # if data['password1'] != data['password2']:
    #     #     raise serializers.ValidationError(_("The two password fields didn't match."))
    #     return data

    # def custom_signup(self, request, user):
    #     pass

    # def get_cleaned_data(self):
    #     return {
    #         'username': self.validated_data.get('username', ''),
    #         'password1': self.validated_data.get('password1', ''),
    #         'email': self.validated_data.get('email', ''),
    #     }

    # def save(self, request):
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     self.cleaned_data = self.get_cleaned_data()
    #     user = adapter.save_user(request, user, self, commit=False)
    #     if "password1" in self.cleaned_data:
    #         try:
    #             adapter.clean_password(self.cleaned_data['password1'], user=user)
    #         except DjangoValidationError as exc:
    #             raise serializers.ValidationError(
    #                 detail=serializers.as_serializer_error(exc)
    #         )
    #     # user.set_password(self.validated_data['password'])
    #     user.save()
    #     self.custom_signup(request, user)
    #     setup_user_email(request, user, [])
    #     return user





# class VerifyEmailSerializer(serializers.Serializer):
#     key = serializers.CharField()