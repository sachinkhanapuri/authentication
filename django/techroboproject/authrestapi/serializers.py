from django.contrib import auth
from rest_framework import serializers
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50, min_length=3)
    username = serializers.CharField(max_length=30,min_length=3)
    password=serializers.CharField(max_length=20,min_length=6,write_only=True)
    class Meta:
        model=User
        fields=['email','username','password']


    def validate(self,request):
        email=request.get('email')
        username=request.get('username')
        password=request.get('password')
        user_qs=User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError({'info':'this user is already registered'})
        return request

    def create(self,validated_data):
        username=validated_data['username']
        email=validated_data['email']
        password=validated_data['password']
        user_obj=User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class VerifyEmailSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555,write_only=True)
    class Meta:
        model=User
        field=['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50,min_length=3)
    username=serializers.CharField(max_length=20,read_only=True)
    password=serializers.CharField(max_length=20)
    #tokens=serializers.CharField(max_length=20, min_length=6,read_only=True)

    class Meta:
        model=User
        fields=['email','username','password']


    def validate(self,attrs):
        email=attrs.get('email',None)
        password =attrs['password']
        user=auth.authenticate(email=email,password=password)
        print(user)
        if not email and not password:
            raise serializers.ValidationError({'info':'username and password must be compulsory'})
        if not user:
            raise serializers.ValidationError({'info':'Invalid cerdentials please try again'})
        if not user.is_active:
            raise serializers.ValidationError({'info':'Account disable,contact admin'})
        if not user.is_verified:
            raise serializers.ValidationError({'info':'email is not verified'})

        return super().validate(attrs)

class PasswordResetEmailViewSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(min_length=2,max_length=80)
    class Meta:
        model=User
        fields=['email']

class PasswordTokenCheckAPISerilaizer(serializers.ModelSerializer):
    email=serializers.EmailField(min_length=2,max_length=80)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    class Meta:
        model=User
        fields=['email','token','uidb64']

class SetnewPasswordViewSerializer(serializers.ModelSerializer):
    password=serializers.CharField(min_length=6,max_length=15,write_only=True)
    confirm_password = serializers.CharField(min_length=6,max_length=15,write_only=True)
    token=serializers.CharField(min_length=1)
    uidb64= serializers.CharField(min_length=1)
    class Meta:
        model=User
        fields=['password','confirm_password','token','uidb64']

    def validate(self, data):
        confirm_password=data.get('confirm_password')
        token = data.get('token')
        uidb64 = data.get('uidb64')
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed('The reset link is invalid')
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password') == data.get('confirm_password'):
            user.set_password(confirm_password)
            user.save()
        return data
