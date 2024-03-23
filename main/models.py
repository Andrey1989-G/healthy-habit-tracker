from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

NULLABLE = {'null': True, 'blank': True}


class UsefulHabit(models.Model):
    """Модель привычек. Подробное описание см в Readme"""

    PERIOD_DAY01 = 1
    PERIOD_DAY02 = 2
    PERIOD_DAY03 = 3
    PERIOD_DAY04 = 4
    PERIOD_DAY05 = 5
    PERIOD_DAY06 = 6
    PERIOD_DAY07 = 7

    PERIODS = (
        (PERIOD_DAY01, 'раз в день'),
        (PERIOD_DAY02, 'раз в 2 дня'),
        (PERIOD_DAY03, 'раз в 3 дня'),
        (PERIOD_DAY04, 'раз в 4 дня'),
        (PERIOD_DAY05, 'раз в 5 дней'),
        (PERIOD_DAY06, 'раз в 6 дней'),
        (PERIOD_DAY07, 'раз в неделю'),
    )

    title = models.CharField(max_length=256, verbose_name='наименование')
    location = models.CharField(max_length=256, verbose_name='место')
    action = models.CharField(max_length=256, verbose_name='действие')
    is_good = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    award = models.CharField(max_length=256, **NULLABLE, verbose_name='вознаграждение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    period = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)], default=PERIOD_DAY01,
                                 choices=PERIODS, verbose_name='периодичность')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    time_to_complete = models.DurationField(default=timedelta(seconds=120), verbose_name='время на выполнение')
    time = models.TimeField(default=datetime.time(datetime.now()), **NULLABLE, verbose_name='время выполнения')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='связанная привычка')

    def __str__(self):
        return f'{self.title} - {self.owner}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('title',)
