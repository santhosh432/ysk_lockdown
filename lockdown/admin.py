from django.contrib import admin
from lockdown.models import LockDown
# Register your models here.


@admin.register(LockDown)
class LockDownAdmin(admin.ModelAdmin):
    list_display = ['lock_user', 'attempt', 'status', 'last_attempt']