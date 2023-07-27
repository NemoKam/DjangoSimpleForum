from django.contrib import admin

from authapp.models import UserRequest

class UserRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip', 'request_count', 'request_started']
    ordering = ['id']
    list_display_links = ['ip']


admin.site.register(UserRequest, UserRequestAdmin)
