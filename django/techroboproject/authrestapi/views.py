from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import RegisterSerializer,LoginSerializer,VerifyEmailSerializer,PasswordResetEmailViewSerializer,PasswordTokenCheckAPISerilaizer,SetnewPasswordViewSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util



# swagger import module
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        #print(user_data)
        #print(user_data['email'])  # { 'email':'93sachinkhanapuri@gmail.com' ,'username':'sachin09'}#
        user=User.objects.get(email=user_data['email'])
        #print('email=',user)                            # 93sachinkhanapuri@gmail.com#
        token=RefreshToken.for_user(user).access_token

    # verification mail send to registered mail id
        current_site=get_current_site(request).domain
        relativeLink=reverse('VerifyEmail')
        absurl='http://'+current_site+relativeLink+"?token="+str(token)
        email_body='hi, '+user.username+' \n use link below to verify your email \n'+absurl
        data = {
            'email_body':email_body,'to_email':user.email,'email_subject':'verify your email','token':token
        }

        Util.send_email(data)
        return Response({'user_data':user_data,'info':" please go to your email to verify your email"},status=status.HTTP_200_OK)

class VerifyEmailView(views.APIView):
    serializer_class =VerifyEmailSerializer
    #token_param_config=openapi.Parameter('token',in_=openapi.IN_QUERY,description='description',type=openapi.TYPE_STRING)

    #@swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY)
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'success':'successfully activated'} ,status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'activation failed'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        print("serializer=",serializer)
        if serializer.is_valid():
            return Response({'data':serializer.data,'success':'Login is done successfully'},status=status.HTTP_200_OK)
        return Response({'error':'login not done successfully'})


class PasswordResetEmailView(generics.GenericAPIView):
    serializer_class = PasswordResetEmailViewSerializer
    def post(self, request):
        data=request.data
        serializer=PasswordResetEmailViewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user_data=serializer.data
        email=request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes((user.id)))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello ,\n hi use link below to reset password password \n' + absurl
            data = {
                'email_body': email_body, 'to_email': user.email, 'email_subject': 'reset your password'
            }

            Util.send_email(data)
        return Response({'user_data':user_data,'info':'we have send a link to reset password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class=PasswordTokenCheckAPISerilaizer
    def get(self,request,uidb64,token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error': 'Token is not valid please request a new one'})
            return Response({'success':'cerdentials valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid please request a new one'})


class SetnewPasswordView(generics.GenericAPIView):
    serializer_class = SetnewPasswordViewSerializer
    def patch(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response({'data':serializer.data,'success':'password reset successfully'},status=status.HTTP_201_CREATED)



