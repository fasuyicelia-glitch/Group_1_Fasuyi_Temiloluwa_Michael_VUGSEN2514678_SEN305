from django.utils import timezone
from .models import ServiceRequest


def overdue_requests():
    return ServiceRequest.objects.filter(
        due_at__lt=timezone.now(),
        due_at__isnull=False,
    ).exclude(status__in=[
        ServiceRequest.Status.RESOLVED,
        ServiceRequest.Status.CLOSED,
    ])


def requests_due_before(moment):
    return ServiceRequest.objects.filter(
        due_at__isnull=False,
        due_at__lt=moment,
    ).order_by("due_at")


def active_requests_in_category(category):
    return ServiceRequest.objects.filter(
        category=category,
        status__in=[ServiceRequest.Status.OPEN, ServiceRequest.Status.ASSIGNED],
    ).order_by("-priority", "created_at")
