from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'username',
        'email',
    )
    search_fields = (
        'name',
        'username',
        'email',
    )
    list_filter = (
        'name',
        'username',
        'email',
    )
