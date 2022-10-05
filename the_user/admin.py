from django.contrib import admin

from .models import BooleanSettings, Profile
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(BooleanSettings)
class BooleanSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'value')
    list_filter = ('user',)
    search_fields = ('key',)
    # date_hierarchy = 'created_date'
    ordering = ('key',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website_language','communication_language')
    list_filter = ('user',)
    search_fields = ('user',)
    # date_hierarchy = 'created_date'
    ordering = ('user',)

    def name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserBooleanSettingsInline(admin.TabularInline):
    model = BooleanSettings
    can_delete = False
    verbose_name_plural = 'settings'
    extra = 0
    readonly_fields = ['key']


class MyUserAdmin(UserAdmin):
    inlines = UserProfileInline, UserBooleanSettingsInline

    def get_inline_instances(self, request, obj = None):
        if not obj:
            return list()
        return super(MyUserAdmin, self).get_inline_instances(request, obj)


# Register your models here
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)