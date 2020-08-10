from django.urls import path
from .views import RegisterView,VerifyEmailView,LoginApiView,PasswordTokenCheckAPI,PasswordResetEmailView,SetnewPasswordView

urlpatterns = [
    path('RegisterView/',RegisterView.as_view(),name='RegisterView'),
    path('VerifyEmail/',VerifyEmailView.as_view(),name='VerifyEmail'),
    path('loginapi/',LoginApiView.as_view(),name='loginapi'),
    path('password-reset-email/',PasswordResetEmailView.as_view(),name='password-reset-email'),
    path('password-reset/<uidb64>/<token>',PasswordTokenCheckAPI.as_view(),name='password-reset'),
    path('SetnewPassword/',SetnewPasswordView.as_view(),name='SetnewPasswordView'),

]
