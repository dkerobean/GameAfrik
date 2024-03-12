from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import (Profile, CustomUser, Tournament,
                         Game, Clips)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','email', 'password1', 'password2', 'is_staff', 'is_active')} # noqa
        ), # noqa
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Profile)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game)
admin.site.register(Tournament)
admin.site.register(Clips)
# admin.site.register(GameCategory)
