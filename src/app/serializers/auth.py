from django.core.validators import RegexValidator
from rest_framework import serializers

from app.models import User, phone_number_validator

confirm_code_validator = RegexValidator(
    regex=r'^[0-9]{4}$',
    message='Код подтверждения должен быть длиной 4 и состоять из цифр.'
)


class PhoneSerializer(serializers.Serializer):
    phone_number  = serializers.CharField(validators=[phone_number_validator])


class ConfirmCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_number_validator])
    code = serializers.CharField(validators=[confirm_code_validator])

