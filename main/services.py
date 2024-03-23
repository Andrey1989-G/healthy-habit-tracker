from django_celery_beat.models import CrontabSchedule, PeriodicTask
from config import settings


# функции для работы с задачами
def create_schedule_and_habit_periodic_task(habit):
    """Создание задачи"""
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=habit.time.minute,
        hour=habit.time.hour,
        day_of_week=f'*/{habit.period}',
        month_of_year='*',
        timezone=settings.TIME_ZONE
    )

    PeriodicTask.objects.create(
        crontab=schedule,
        name=f'HabitTask{habit.id}',
        task='main.tasks.send_message_bot',
        args=[habit.id],
    )


def delete_habit_periodic_task(habit):
    """Удаление задачи"""

    PeriodicTask.objects.filter(name=f'HabitTask{habit.id}').delete()


def update_habit_periodic_task(habit):
    """Пересоздание задачи"""
    delete_habit_periodic_task(habit)
    create_schedule_and_habit_periodic_task(habit)
