from rest_framework import serializers


class ErrorResponse(serializers.Serializer):
    detail = serializers.DictField(
        child=serializers.CharField()
    )

class MessageResponse(serializers.Serializer):
    message = serializers.CharField()

class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1, default=1)
    page_size = serializers.IntegerField(min_value=1, max_value=100, default=20)
