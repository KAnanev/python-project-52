from django.contrib import admin

from task_manager.users.models import User


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Пользователи'
