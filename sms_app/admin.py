from django.contrib import admin

from .models import SMSMessage


@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ("recipient", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("recipient", "body", "provider_sid")
    readonly_fields = ("created_at", "updated_at")
