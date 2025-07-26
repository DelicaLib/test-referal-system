from django.core.paginator import Paginator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import User
from app.serializers.base import ErrorResponse, MessageResponse, PaginationSerializer
from app.serializers.profile import UserSerializer, ReferralsSerializer, ReferralCodeSerializer


class ProfileViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: UserSerializer
        },
        description="Получить информацию о текущем пользователе",
        summary="Получить профиль пользователя",
        tags=["profile"]
    )
    def list(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page', description='Номер страницы',
                required=False, type=OpenApiTypes.INT, default=1
            ),
            OpenApiParameter(
                name='page_size', description='Размер страницы',
                required=False, type=OpenApiTypes.INT, default=20
            ),
        ],
        responses={
            200: ReferralsSerializer
        },
        description="Получить список номеров телефонов людей, которые активировали код авторизованного пользователя",
        summary="Получить список рефералов",
        tags=["profile"]
    )
    @action(detail=False, methods=["get"], url_path='referrals')
    def get_referrals(self, request):
        user = request.user
        invite_code = user.invite_code
        serializer = PaginationSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        page_size = serializer.validated_data['page_size']
        page_number = serializer.validated_data['page']

        referrals_phones = User.objects.filter(activated_code=invite_code).only('phone_number').order_by('phone_number')
        paginator = Paginator(referrals_phones, page_size)
        page = paginator.get_page(page_number).object_list

        return Response(ReferralsSerializer(page).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ReferralCodeSerializer, responses={
            200: MessageResponse,
            400: ErrorResponse,
        },
        description="Ввести реферальный код",
        summary="Ввести реферальный код",
        tags=["profile"]
    )
    @action(detail=False, methods=["post"], url_path='activate_referral_code')
    def activate_referral_code(self, request):
        user = request.user
        serializer = ReferralCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data['code']
        if user.activated_code is not None:
            return Response({"detail": {"message": "У вас уже активирован код"}}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(invite_code=invite_code).first() is None:
            return Response({"detail": {"message": "Неизвестный код"}}, status=status.HTTP_400_BAD_REQUEST)
        if user.invite_code == invite_code:
            return Response({"detail": {"message": "Вы не можете ввести свой реферальный код"}}, status=status.HTTP_400_BAD_REQUEST)
        user.activated_code = invite_code
        user.save()
        return Response({"message": "Код активирован!"}, status=status.HTTP_200_OK)
