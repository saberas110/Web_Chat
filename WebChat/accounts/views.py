from datetime import timedelta
from django.utils import timezone
from random import randint
from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import OTP, User


class CSRFTokenView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({'message':'CSRFToken set successfully'})
    
class OtpView(APIView):
    def post(self, request):
        phone = request.POST.get('phone')
        request.session['phone'] = phone
        print(request.session, 'session')
        random_code = randint(100000,999999)

        otp = OTP.objects.create(phone=phone, code=random_code,
                                 expired_time=timezone.now()+timedelta(minutes=2) )
        print(otp)
        return Response({'message': 'we sent otp_code to your phone_number'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        user_otp = request.POST.get('otp')
        phone = request.session['phone']
        try:
            otp_object = OTP.objects.get(phone=phone)
            if otp_object.code != user_otp:
                return Response({'message':{'کد وارد شده اشتباه است'}}, status.HTTP_400_BAD_REQUEST)
            if otp_object.expired_time < timezone.now():
                return Response({'message':'کد وارد شده منقضی شده است. لطفا روی ارسال دوباره کد کلیک کنید'}
                                ,status.HTTP_400_BAD_REQUEST)
            user, create = User.objects.get_or_create(phone_number=phone)
            response = Response({'message': 'ثبت نام موفقیت امیز بود'}, status.HTTP_201_CREATED)
            if user:
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                response.set_cookie(
                    key= 'access',
                    value= str(access),
                    httponly= True,
                    secure= False,
                    samesite= 'lax',
                )
                response.set_cookie(
                    key= 'refresh',
                    value= str(refresh),
                    httponly= True,
                    secure= 'lax',
                    samesite='lax',
                )
            if create:
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                response.set_cookie(
                    key='access',
                    value=str(access),
                    httponly=True,
                    secure=False,
                    samesite='lax',
                )
                response.set_cookie(
                    key='refresh',
                    value=str(refresh),
                    httponly=True,
                    secure='lax',
                    samesite='lax',
                )
            return response
        except OTP.DoesNotExist:
            return Response({'message':'شماره ی شما در سیستم وجود ندارد'}, status.HTTP_400_BAD_REQUEST)



