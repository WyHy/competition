from django.contrib import admin

from .models import Image


# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    fields = ('name', 'path', 'progress', 'result_auto', 'result_manual', 'result_status')
    list_display = (
        'id', 'name', 'path', 'progress', 'result_auto', 'result_manual', 'result_status', 'create_time', 'update_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Image, ImageAdmin)