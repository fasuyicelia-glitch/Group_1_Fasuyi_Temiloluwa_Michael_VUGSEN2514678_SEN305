from django.contrib import admin
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "title", "category", "status", "priority", "requester",
        "assigned_to", "due_at", "overdue",
    )
    list_filter = ("category", "status", "priority", "due_at")
    search_fields = ("title", "description", "requester__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    @admin.display(boolean=True, description="Overdue")
    def overdue(self, obj):
        return obj.is_overdue
