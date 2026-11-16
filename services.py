from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import ServiceRequest


def resolve_request(request_obj, summary):
    summary = (summary or "").strip()
    if not summary:
        raise ValidationError({"resolution_summary": "A resolution summary is required."})
    request_obj.status = ServiceRequest.Status.RESOLVED
    request_obj.resolved_at = timezone.now()
    request_obj.resolution_summary = summary
    request_obj.full_clean()
    request_obj.save()
    return request_obj


def close_request(request_obj, summary):
    summary = (summary or "").strip()
    if not summary:
        raise ValidationError({"resolution_summary": "A resolution summary is required."})
    request_obj.status = ServiceRequest.Status.CLOSED
    request_obj.resolved_at = request_obj.resolved_at or timezone.now()
    request_obj.resolution_summary = summary
    request_obj.full_clean()
    request_obj.save()
    return request_obj
