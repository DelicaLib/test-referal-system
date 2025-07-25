from rest_framework import serializers

from app.models import User, invite_code_validator
from app.serializers.auth import PhoneSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'invite_code', 'activated_code')

class ReferralsSerializer(serializers.ListSerializer):
    child = PhoneSerializer()

class ReferralCodeSerializer(serializers.Serializer):
    code = serializers.CharField(validators=[invite_code_validator])
