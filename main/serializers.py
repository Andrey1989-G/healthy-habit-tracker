from rest_framework import serializers
from main.models import UsefulHabit
from main.validators import (one_of_related_habit_or_award, time_to_complete_no_more_120seconds,
                             only_good_habit_into_related_habit, good_habit_cannot_have_award_or_related_habit)


class UsefulHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Привычки"""

    class Meta:
        model = UsefulHabit
        fields = '__all__'
        extra_kwargs = {'owner': {'required': False}}

        validators = [
            one_of_related_habit_or_award,
            time_to_complete_no_more_120seconds,
            only_good_habit_into_related_habit,
            good_habit_cannot_have_award_or_related_habit,
        ]

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
