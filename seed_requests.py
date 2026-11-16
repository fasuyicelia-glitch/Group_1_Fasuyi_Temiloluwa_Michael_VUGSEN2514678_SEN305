from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from requests_app.models import ServiceRequest


class Command(BaseCommand):
    help = "Create 12 sample service requests for query analysis."

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username="sample_student")
        categories = [ServiceRequest.Category.IT, ServiceRequest.Category.FACILITIES]
        statuses = [
            ServiceRequest.Status.OPEN,
            ServiceRequest.Status.ASSIGNED,
            ServiceRequest.Status.RESOLVED,
        ]
        for i in range(12):
            status = statuses[i % 3]
            resolved = timezone.now() if status == ServiceRequest.Status.RESOLVED else None
            ServiceRequest.objects.get_or_create(
                title=f"Sample request {i + 1}",
                defaults={
                    "description": f"Synthetic demonstration request {i + 1}",
                    "category": categories[i % 2],
                    "status": status,
                    "priority": (i % 4) + 1,
                    "requester": user,
                    "due_at": timezone.now() + timedelta(days=i - 3),
                    "resolved_at": resolved,
                    "resolution_summary": "Completed for sample data" if resolved else "",
                },
            )
        self.stdout.write(self.style.SUCCESS("Created or confirmed 12 sample requests."))
