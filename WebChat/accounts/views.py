from datetime import timedelta
from django.utils import timezone
from random import randint
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from chat.models import UserProfile
from .models import OTP, User
from .serializers import PhoneSerializer, OtpSerializer, UserSerializer


class CSRFTokenView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({'message':'CSRFToken set successfully'})
    
class OtpView(APIView):
    def post(self, request):
        srz_data = PhoneSerializer(data=request.data)
        if not srz_data.is_valid():
            return Response(srz_data.errors, status.HTTP_400_BAD_REQUEST)
        phone = srz_data.validated_data['phone']
        request.session['phone'] = phone
        random_code = randint(100000,999999)

        otp = OTP.objects.create(phone=phone, code=random_code,
                                 expired_time=timezone.now()+timedelta(minutes=2) )
        print(otp)
        return Response({'message': 'we sent otp_code to your phone_number', 'code':random_code}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        srz_data = OtpSerializer(data=request.data, context={'request':request})
        if not srz_data.is_valid():
            return Response(srz_data.errors, status.HTTP_400_BAD_REQUEST)
        phone = srz_data.validated_data['otp_code']
        print('phone from post register view', phone)
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
            user = create
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


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
       user = request.user
       srz_data =UserSerializer(user)
       return Response(srz_data.data, status.HTTP_200_OK)



