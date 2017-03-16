from django.contrib import admin
from app.models import Monitor, Privilege

# Register your models here.
class MonitorAdmin(admin.ModelAdmin):
    list_display = ['monitor_name', 'monitor_text', 'monitor_month', 'monitor_day', 'monitor_hour', 'monitor_minute', 'email_enable', 'email_to', 'email_subject', 'created_at', 'updated_at']
    list_filter = [
        'monitor_name', 'monitor_month', 'monitor_day', 'created_at',
    ]
    search_fields = ['monitor_name', 'monitor_text']
    # exclude = ['signin_password']
    editable = ['monitor_name', 'monitor_text', 'monitor_month', 'monitor_day', 'monitor_hour', 'monitor_minute', 'email_enable', 'email_to', 'email_subject']

admin.site.register(Monitor)
admin.site.register(Privilege)
