from django.contrib import admin

# Register your models here.
from Label.models import Cell, ScreenShot


class CellAdmin(admin.ModelAdmin):
    fields = ('image', 'x', 'y', 'w', 'h', 'cell_type', 'source_type')
    list_display = ('id', 'image', 'x', 'y', 'w', 'h', 'cell_type', 'source_type', 'create_time')
    list_per_page = 50
    ordering = ('id',)


class ScreenShotAdmin(admin.ModelAdmin):
    fields = ('image', 'x', 'y', 'w', 'h')
    list_display = ('id', 'image', 'x', 'y', 'w', 'h', 'create_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Cell, CellAdmin)
admin.site.register(ScreenShot, ScreenShotAdmin)
