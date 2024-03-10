from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    chat_id = models.IntegerField(unique=True, verbose_name='идентификатор телеграм')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def create_user(self, email, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError('Поле имэйл должен быть заполнен')
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create(self, validated_data):
    #     user = User.objects.create(**validated_data)
    #     user.set_password(user.password)
    #     user.save()
    #     return user

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

