from django.urls import path
from main.views import (UsefulHabitListAPIView, UsefulHabitViewAPIView, UsefulHabitCreateAPIView,
                        UsefulHabitUpdateAPIView, UsefulHabitDeleteAPIView, UsefulHabitPublicListAPIView)
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('create/', UsefulHabitCreateAPIView.as_view(), name='useful_habit_create'),
    path('list/', UsefulHabitListAPIView.as_view(), name='useful_habit_list'),
    path('view/<int:pk>/', UsefulHabitViewAPIView.as_view(), name='useful_habit_view'),
    path('edit/<int:pk>/', UsefulHabitUpdateAPIView.as_view(), name='useful_habit_edit'),
    path('delete/<int:pk>/', UsefulHabitDeleteAPIView.as_view(), name='useful_habit_delete'),
    path('list_public/', UsefulHabitPublicListAPIView.as_view(), name='useful_habit_list_public'),
]
