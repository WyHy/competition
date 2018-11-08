from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile


# Register your models here.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'user', 'type']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        users = User.objects.exclude(is_superuser=True).order_by('id')
        self.fields['user'].queryset = users if users else None


class ProfileAdmin(admin.ModelAdmin):
    fields = ('nickname', 'user', 'type',)
    list_display = ('id', 'nickname', 'user', 'type', 'create_time', 'update_time')
    form = ProfileForm
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Profile, ProfileAdmin)
