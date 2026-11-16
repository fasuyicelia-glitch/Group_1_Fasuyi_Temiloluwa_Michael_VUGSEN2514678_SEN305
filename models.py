from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


class ServiceRequest(models.Model):
    class Category(models.TextChoices):
        IT = "IT", "IT Support"
        FACILITIES = "FAC", "Facilities"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        ASSIGNED = "ASSIGNED", "Assigned"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"
        URGENT = 4, "Urgent"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=3, choices=Category.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="service_requests"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="assigned_service_requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(null=True, blank=True, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_summary = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "due_at"], name="req_status_due_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(priority__gte=1) & Q(priority__lte=4),
                name="valid_request_priority",
            )
        ]

    def clean(self):
        super().clean()
        if self.status in {self.Status.RESOLVED, self.Status.CLOSED}:
            errors = {}
            if not self.resolved_at:
                errors["resolved_at"] = "Resolved or closed requests must have a resolution date."
            if not self.resolution_summary.strip():
                errors["resolution_summary"] = "Provide a resolution summary before resolving or closing."
            if errors:
                raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Enforce domain validation even when a caller does not use a ModelForm.
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return bool(
            self.due_at and self.due_at < timezone.now()
            and self.status not in {self.Status.RESOLVED, self.Status.CLOSED}
        )

    def __str__(self):
        return self.title
