from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import time, timedelta

from main.models import UsefulHabit
from users.models import User
from django_celery_beat.models import PeriodicTask


class UsefulHabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', password='test', chat_id='1234567890')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.course_id_01 = UsefulHabit.objects.create(
            title='Привычка №1',
            location='Тренажерный зал',
            action='Поддерживать пульс 120 более 70 минут',
            is_good=True,
            is_public=False,
            period=1,
            time_to_complete=timedelta(seconds=120),
            time=time(17, 30),
            owner=self.user
        )

        self.course_id_02 = UsefulHabit.objects.create(
            title='Привычка №2',
            location='Повышать квалификацию',
            action='Читать техническую литературу',
            is_good=False,
            is_public=False,
            period=1,
            time_to_complete=timedelta(seconds=120),
            time=time(20, 30),
            award='Посмотреть ютубчик',
            owner=self.user
        )

        self.course_id_03 = UsefulHabit.objects.create(
            title='Привычка №3',
            location='Автомобиль',
            action='Включать массажное кресло',
            is_good=False,
            is_public=True,
            period=1,
            time_to_complete=timedelta(seconds=90),
            time=time(7, 0),
            related_habit=self.course_id_01,
            owner=self.user
        )

    def test_create_habit_periodic_task(self):
        """Тестирование создания задачи при создании привычки."""

        data_habit = {'title': 'Привычка №4', 'location': 'Марс', 'action': 'Работа с дыханием',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '18:00'}

        self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            PeriodicTask.objects.filter(name=f'HabitTask{self.course_id_03.id + 1}').exists(),
            True
        )

    def test_create_habit_error_required_field(self):
        """Ошибка заполнения обязательного поля при создании привычки."""

        data_habit = {'title': 'Привычка №4', 'location': 'Марс',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '18:00'}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'action': ['Обязательное поле.']}
        )

    def test_create_habit_error_validator_one_of_related_habit_or_award(self):
        """Ошибка одномоментного использования связанной привычки и вознаграждения."""

        data_habit = {'title': 'Привычка №04', 'location': 'Марс', 'action': 'Работа с дыханием',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '18:00', 'award': 'Купи себе медаль', 'related_habit': self.course_id_01.id}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Ошибка. Нельзя связать эту привычку и вознаграждение']}
        )

    def test_create_habit_error_validator_time_to_complete_no_more_120seconds(self):
        """Тестирование ошибки использования времени выполнения привычки более 2-х минут."""

        data_habit = {'title': 'Привычка №4', 'location': 'Марс', 'action': 'Работа с дыханием',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 999,
                      'time': '18:00', 'award': 'Купи себе медаль!'}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Время выполнения должно быть не больше 120 секунд.']}
        )

    def test_create_habit_error_validator_only_good_habit_into_related_habit(self):
        """Тестирование ошибки использования в связанных привычках не приятные привычки."""

        data_habit = {'title': 'Привычка №4', 'location': 'Марс', 'action': 'Работа с дыханием',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 120,
                      'time': '18:00', 'related_habit': self.course_id_02.id}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Ошибка. Привычка должна быть приятной']}
        )

    def test_create_habit_error_validator_good_habit_cannot_have_award_or_related_habit(self):
        """Тестирование ошибки добавления вознаграждения или связанной привычки в приятные привычки."""

        data_habit = {'title': 'Привычка №4', 'location': 'Марс', 'action': 'Работа с дыханием',
                      'is_good': 'True', 'is_public': 'True', 'period': 1, 'time_to_complete': 120,
                      'time': '18:00', 'related_habit': self.course_id_01.id}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']}
        )

    def test_create_habit(self):
        """Тестирование создания привычки."""

        data_habit = {'title': 'Привычка №4', 'location': 'Марс', 'action': 'Работа с дыханием',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '18:00'}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': self.course_id_03.id + 1, 'title': 'Привычка №4', 'location': 'Марс', 'action': 'Работа с дыханием',
             'is_good': False, 'award': None, 'is_public': True, 'period': 1,
             'time_to_complete': '00:01:00', 'time': '18:00:00', 'owner': 1, 'related_habit': None}
        )

    def test_create_habit_periodic_task(self):
        """Тестирование создания задачи при создании привычки."""

        data_habit = {'title': 'Привычка №4', 'location': 'Марс', 'action': 'Работа с дыханием',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '18:00'}

        self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            PeriodicTask.objects.filter(name=f'HabitTask{self.course_id_03.id + 1}').exists(),
            True
        )

    def test_list_habit(self):
        """Тестирование отображения привычки пользователя"""

        response = self.client.get(
            '/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json().get('count') is not None and response.json().get('count') == 3,
            True
        )

    def test_view_habit(self):
        """Тестирование отображения одной привычки."""

        response = self.client.get(
            f'/view/{self.course_id_02.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.course_id_02.id, 'title': self.course_id_02.title,
             'location': self.course_id_02.location, 'action': self.course_id_02.action,
             'is_good': self.course_id_02.is_good, 'award': self.course_id_02.award,
             'is_public': self.course_id_02.is_public, 'period': self.course_id_02.period,
             'time_to_complete': '0' + str(self.course_id_02.time_to_complete),
             'time': str(self.course_id_02.time),
             'owner': self.user.id, 'related_habit': None}
        )

    def test_update_habit(self):
        """Тестирование редактирования привычки. """

        data = {'id': self.course_id_02.id, 'title': 'Попытка поменять название',
                'location': self.course_id_02.location, 'action': self.course_id_02.action,
                'is_good': self.course_id_02.is_good, 'award': self.course_id_02.award,
                'is_public': self.course_id_02.is_public, 'period': self.course_id_02.period,
                'time_to_complete': self.course_id_02.time_to_complete, 'time': self.course_id_02.time,
                'owner': self.user.id}

        response = self.client.patch(
            f'/edit/{self.course_id_02.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.course_id_02.id, 'title': 'Попытка поменять название',
             'location': self.course_id_02.location, 'action': self.course_id_02.action,
             'is_good': self.course_id_02.is_good, 'award': self.course_id_02.award,
             'is_public': self.course_id_02.is_public, 'period': self.course_id_02.period,
             'time_to_complete': '0' + str(self.course_id_02.time_to_complete),
             'time': str(self.course_id_02.time),
             'owner': self.user.id, 'related_habit': None}
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки."""

        response = self.client.delete(
            f'/delete/{self.course_id_02.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_list_habit_public(self):
        """Тестирование отображения публичных привычек"""

        response = self.client.get(
            '/list_public/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json()[0].get('id') is not None and response.json()[0].get('id') == self.course_id_03.id,
            True
        )

    def tearDown(self):
        UsefulHabit.objects.all().delete()
