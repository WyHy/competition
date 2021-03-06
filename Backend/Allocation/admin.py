from django.contrib import admin

from .models import Allocation


# Register your models here.
class AllocationAdmin(admin.ModelAdmin):
    fields = ('profile', 'tiff',)
    list_display = ('id', 'profile', 'tiff', 'create_time', 'update_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Allocation, AllocationAdmin)
