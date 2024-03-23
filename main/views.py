from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.models import UsefulHabit
from main.serializers import UsefulHabitSerializer
from main.permissions import IsOwner
from main.paginators import MainPaginator

from main.services import create_schedule_and_habit_periodic_task, update_habit_periodic_task


class UsefulHabitCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания экземпляра модели Привычка.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer

    def perform_create(self, serializer):
        """
        После создания (сохранения) экземпляра модели Привычка вызываем функцию создания расписания напоминания.
        """
        new_habit = serializer.save()
        create_schedule_and_habit_periodic_task(new_habit)


class UsefulHabitListAPIView(generics.ListAPIView):
    """
    Представление для отображения реквизитов списка экземпляров модели Привычка принадлежащих Владельцу.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer
    pagination_class = MainPaginator

    def get_queryset(self):
        """
        Накладываем отбор по Владельцу экземпляров модели Привычка.
        :return: Набор экземпляров модели Привычка с наложенным отбором по Владельцу.
        """
        return UsefulHabit.objects.filter(owner=self.request.user)


class UsefulHabitViewAPIView(generics.RetrieveAPIView):
    """Отображение одной привычки"""
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()


class UsefulHabitUpdateAPIView(generics.UpdateAPIView):
    """Обновления данных привычки"""
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()

    def perform_update(self, serializer):
        """Обновление расписания"""
        new_habit = serializer.save()
        update_habit_periodic_task(new_habit)


class UsefulHabitDeleteAPIView(generics.DestroyAPIView):
    """Удаление привычки"""
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()


class UsefulHabitPublicListAPIView(generics.ListAPIView):
    """Отображение списка публичных привычек"""
    permission_classes = [IsAuthenticated]
    serializer_class = UsefulHabitSerializer

    def get_queryset(self):
        """Фильтр по признаку публичность"""
        return UsefulHabit.objects.filter(is_public=True)
