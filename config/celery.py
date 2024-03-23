from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Переменные окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Получение настроек из config
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автообнаружение и регистрация задач из файлов tasks.py
app.autodiscover_tasks()
