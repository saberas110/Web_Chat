import re
from django.utils import timezone

from django.template.context_processors import request
from rest_framework import serializers

from accounts.models import OTP, User


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate_phone(self, value):
        value = value.strip()

        if not re.match(r"^\d+$", value):
            raise serializers.ValidationError("شماره تلفن باید فقط شامل ارقام باشد.")

        if len(value) != 11:
            raise serializers.ValidationError("شماره تلفن باید دقیقا ۱۱ رقم باشد.")

        if not value.startswith('09'):
            raise serializers.ValidationError("شماره تلفن معتبر نمیباشد.شماره باید با (09) اغاز شود")
        
        return value

class OtpSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate_otp_code(self, value):
        value = value.strip()
        request = self.context['request']
        phone = request.session['phone']
        if phone == None:
            raise serializers.ValidationError('شماره ای وارد نشده است.')

        try:
            otp = OTP.objects.get(phone=phone)
            if otp.code != value:
                raise serializers.ValidationError("کد وارد شده اشتباه است")

            if otp.expired_time < timezone.now():
                raise serializers.ValidationError("کد وارد شده منقضی شده است")
            otp.delete()
            return int(phone)
        except OTP.DoesNotExist:
            raise serializers.ValidationError("هیچ کدی برای این شماره در سیستم ثبت نشده است")



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone_number']