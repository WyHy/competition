from django.contrib import admin

# Register your models here.
from Question.models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ('title', 'image', 'choices', 'remark')
    list_display = ('id', 'title', 'image', 'remark', 'create_time')
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Question, QuestionAdmin)
