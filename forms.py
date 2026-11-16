from django import forms
from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["title", "description", "category", "priority", "due_at"]
        widgets = {
            "due_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
