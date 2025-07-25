import random

from django.contrib.auth import login, logout
from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from app.models import User
from app.serializers.auth import PhoneSerializer, ConfirmCodeSerializer
from app.clients import PhoneSender
from app.serializers.base import MessageResponse, ErrorResponse
from referal_system.settings import MOCK_PHONE_SENDER


class AuthViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    _CODE_LIVE_TIME = 300

    @extend_schema(
        request=PhoneSerializer, responses={
            200: MessageResponse
        },
        description="Отправить смс с кодом подтверждения по указанному номеру телефона",
        summary="Отправить смс с кодом подтверждения",
        tags=["auth"]
    )
    @action(detail=False, methods=["post"], url_path="send-code")
    def send_code(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone_number"]
        code = str(random.randint(1000, 9999))
        cache.set(f"auth: {phone}", make_password(code), timeout=self._CODE_LIVE_TIME)
        PhoneSender.send_code_phone_number(phone, code)
        message = f"Код отправлен на {phone}. Код действует {self._CODE_LIVE_TIME // 60} минут"
        if MOCK_PHONE_SENDER:
            return Response({"message": message, "code": code}, status=status.HTTP_200_OK)
        return Response({"message": message}, status=status.HTTP_200_OK)

    @extend_schema(
        request=ConfirmCodeSerializer, responses={
            200: MessageResponse,
            401: ErrorResponse
        },
        description="Авторизоваться используя номер телефона и код подтверждения",
        summary="Авторизоваться с кодом подтверждения",
        tags=["auth"]
    )
    @action(detail=False, methods=["post"], url_path="confirm")
    def confirm(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]
        hashed_code = cache.get(f"auth: {phone}")
        if hashed_code is None or not check_password(code, hashed_code):
            return Response({"detail": {"message": "Код не соответствует"}}, status=status.HTTP_401_UNAUTHORIZED)
        cache.delete(f"auth: {phone}")
        user = User.objects.filter(phone_number=phone).first()
        if user is None:
            user = User.objects.create_user(phone_number=phone)
        login(request, user)
        return Response({"message": f"Вы успешно авторизовались"}, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            200: MessageResponse,
            401: ErrorResponse
        },
        description="Узнать статус авторизации. Залогинен или нет.",
        summary="Узнать статус авторизации",
        tags=["auth"]
    )
    @action(detail=False, methods=["get"], url_path="status")
    def status(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({"message": f"Вы авторизованы"}, status=status.HTTP_200_OK)
        return Response({"detail": {"message": "Вы не авторизованы"}}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        responses={
            200: MessageResponse,
            401: ErrorResponse
        },
        description="Разлогинится. Выйти из аккаунта",
        summary="Разлогинится",
        tags=["auth"]
    )
    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": {"message": "Вы не авторизованы"}}, status=status.HTTP_401_UNAUTHORIZED)

        logout(request)
        return Response({"message": f"Теперь вы не авторизованы"}, status=status.HTTP_200_OK)