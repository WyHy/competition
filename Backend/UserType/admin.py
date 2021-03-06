from django.contrib import admin

from .models import UserType


# Register your models here.


class UserTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'description',)
    list_display = ('id', 'name', 'description', 'create_time', 'update_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(UserType, UserTypeAdmin)
