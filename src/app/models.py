from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

import shortuuid

MAX_TRIES = 500

invite_code_validator = RegexValidator(
    regex=r'^[A-Za-z0-9]{6}$',
    message='Инвайт код должен состоять из 6 латинских букв и/или цифр.'
)

phone_number_validator = RegexValidator(
    regex=r'^\+\d{10,15}$',
    message='Номер телефона должен быть в формате: +71234567890 (от 10 до 15 цифр)'
)


class UserManager(BaseUserManager):
    def create_user(self, phone_number, *args, **kwargs):
        if not phone_number:
            raise ValueError('Телефон обязателен')
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_unusable_password()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(
        max_length=15, unique=True,
        blank=False, null=False,
        validators=[phone_number_validator]
    )
    invite_code = models.CharField(
        max_length=6, unique=True,
        blank=False, null=False,
        validators=[invite_code_validator]
    )
    activated_code = models.CharField(
        max_length=6, unique=True,
        null=True, validators=[invite_code_validator]
    )

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = invite_code_generator()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.phone_number}; invite_code: {self.invite_code}"


def invite_code_generator() -> str:
    for _ in range(MAX_TRIES):
        code = shortuuid.ShortUUID(alphabet='0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxy') \
            .random(length=6)
        if not User.objects.filter(invite_code=code).exists():
            return code
    raise ValueError("Не удалось сгенерировать уникальный код")
