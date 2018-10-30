from django.contrib import admin

# Register your models here.
from Label.models import Cell


class CellAdmin(admin.ModelAdmin):
    fields = ('image', 'x', 'y', 'w', 'h', 'cell_type')
    list_display = ('id', 'image', 'x', 'y', 'w', 'h', 'cell_type', 'create_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Cell, CellAdmin)
