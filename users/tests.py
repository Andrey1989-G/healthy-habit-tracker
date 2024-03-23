from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UsersTestCase(APITestCase):

    def test_create_user_error(self):
        """Ошибка заполнения обязательного поля при создании пользователя"""
        data_user = {
            'email': 'test@test.ru',
            'password': '1234'
        }

        response = self.client.post(
            '/users/create/',
            data=data_user
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'chat_id': ['Обязательное поле.']}
        )

    def test_create_user(self):
        """Тест создания пользователя"""
        data_user = {
            'email': 'test@test.ru',
            'chat_id': 159482673,
            'password': '1594'
        }

        response = self.client.post(
            '/users/create/',
            data=data_user
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json().get('is_active') is not None and response.json().get('is_active'),
            True
        )

    def tearDown(self):
        User.objects.all().delete()
