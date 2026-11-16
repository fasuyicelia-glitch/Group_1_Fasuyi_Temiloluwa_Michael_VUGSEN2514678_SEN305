from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from .models import ServiceRequest
from .selectors import requests_due_before, active_requests_in_category
from .services import resolve_request

User = get_user_model()


class ServiceRequestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="student1", password="test-pass-123")
        self.other = User.objects.create_user(username="staff1", password="test-pass-123")

    def make_request(self, **kwargs):
        defaults = dict(
            title="Network issue", category=ServiceRequest.Category.IT,
            requester=self.user,
        )
        defaults.update(kwargs)
        return ServiceRequest.objects.create(**defaults)

    def test_due_before_query_returns_only_earlier_due_requests(self):
        now = timezone.now()
        earlier = self.make_request(due_at=now - timedelta(days=1))
        self.make_request(due_at=now + timedelta(days=1))
        results = requests_due_before(now)
        self.assertEqual(list(results), [earlier])

    def test_resolved_request_requires_date_and_summary(self):
        item = ServiceRequest(
            title="Fixed issue", category=ServiceRequest.Category.IT,
            requester=self.user, status=ServiceRequest.Status.RESOLVED,
        )
        with self.assertRaises(ValidationError):
            item.save()

    def test_service_can_resolve_request(self):
        item = self.make_request()
        resolve_request(item, "Network configuration corrected.")
        item.refresh_from_db()
        self.assertEqual(item.status, ServiceRequest.Status.RESOLVED)
        self.assertIsNotNone(item.resolved_at)
        self.assertTrue(item.resolution_summary)

    def test_active_category_query_orders_priority_then_created(self):
        low = self.make_request(title="Low", priority=ServiceRequest.Priority.LOW)
        high = self.make_request(title="High", priority=ServiceRequest.Priority.HIGH)
        resolved = self.make_request(title="Resolved", status=ServiceRequest.Status.RESOLVED,
                                     resolved_at=timezone.now(), resolution_summary="Done")
        results = list(active_requests_in_category(ServiceRequest.Category.IT))
        self.assertEqual(results[:2], [high, low])
        self.assertNotIn(resolved, results)
