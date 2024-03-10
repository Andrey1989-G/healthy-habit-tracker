from django.contrib import admin

from main.models import UsefulHabit


@admin.register(UsefulHabit)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'is_good', 'period')
    list_filter = ('title', 'owner')
    search_fields = ('title', 'owner')