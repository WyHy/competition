from django.contrib import admin

# Register your models here.
from Activity.models import Answer


class AnswerAdmin(admin.ModelAdmin):
    fields = ('image', 'profile', 'answer',)
    list_display = ('id', 'image', 'profile', 'answer', 'create_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Answer, AnswerAdmin)
