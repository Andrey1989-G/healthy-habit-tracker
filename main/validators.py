from rest_framework import serializers
from datetime import timedelta


def one_of_related_habit_or_award(value):
    """Проверка на исключение одномоментного выбора связанной привычки и вознаграждения."""

    if (value.get('related_habit') is not None
            and value.get('award') is not None):
        raise serializers.ValidationError('Ошибка. Нельзя связать эту привычку и вознаграждение')


def time_to_complete_no_more_120seconds(value):
    """Проверка на запрет использования времени выполнения привычки более 2-х минут"""

    if value['time_to_complete'] > timedelta(minutes=2):
        raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд.')


def only_good_habit_into_related_habit(value):
    """Проверка на использование в связанных привычках приятные привычки."""

    if (value.get('related_habit') is not None
            and not value['related_habit'].is_good):
        raise serializers.ValidationError('Ошибка. Привычка должна быть приятной')


def good_habit_cannot_have_award_or_related_habit(value):
    """Проверка на использование в приятных привычках вознаграждения или связанной привычки."""

    if (value['is_good'] and
            ((value.get('related_habit') is not None
              or value.get('award') is not None))):
        raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
