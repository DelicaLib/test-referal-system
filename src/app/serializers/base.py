from rest_framework import serializers


class ErrorResponse(serializers.Serializer):
    detail = serializers.DictField(
        child=serializers.CharField()
    )

class MessageResponse(serializers.Serializer):
    message = serializers.CharField()