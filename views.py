from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ServiceRequestForm
from .models import ServiceRequest


@login_required
def request_list(request):
    items = ServiceRequest.objects.filter(requester=request.user)
    return render(request, "requests_app/request_list.html", {"requests": items})


@login_required
def request_create(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.requester = request.user
            item.save()
            return redirect("request_list")
    else:
        form = ServiceRequestForm()
    return render(request, "requests_app/request_form.html", {"form": form})


@login_required
def request_detail(request, pk):
    item = get_object_or_404(ServiceRequest, pk=pk, requester=request.user)
    return render(request, "requests_app/request_detail.html", {"item": item})
