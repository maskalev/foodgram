from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'username',
        'email',
    )
    search_fields = (
        'title',
        'username',
        'email',
    )
    list_filter = (
        'title',
        'username',
        'email',
    )
