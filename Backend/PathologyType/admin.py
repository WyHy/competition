from django.contrib import admin

from .models import Type


# Register your models here.


class TypeAdmin(admin.ModelAdmin):
    fields = ('name', 'color', 'description',)
    list_display = ('id', 'name', 'color', 'description', 'create_time', 'update_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Type, TypeAdmin)
