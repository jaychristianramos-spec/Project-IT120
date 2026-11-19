
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import services
from .forms import SMSForm
from .models import SMSMessage


def send_sms_view(request):
    """Display the compose form and send SMS through TextBee."""

    if request.method == "POST":
        form = SMSForm(request.POST)

        if form.is_valid():
            recipient = form.cleaned_data["recipient"]
            body = form.cleaned_data["message"]

            result = services.send_sms(recipient, body)

            SMSMessage.objects.create(
                recipient=recipient,
                body=body,
                status=result.status or "rejected",
                provider_sid=result.sid,
                error_message=result.error,
            )

            if result.ok:
                messages.success(
                    request,
                    "SMS successfully submitted to TextBee! "
                    "Check History to confirm delivery."
                )
                return redirect("sms_app:send")

            messages.error(
                request,
                f"SMS sending failed: {result.error}"
            )

    else:
        form = SMSForm()

    recent = SMSMessage.objects.all()[:3]

    return render(
        request,
        "sms_app/send.html",
        {
            "form": form,
            "recent": recent,
        }
    )


def history_view(request):
    """Display SMS dashboard with search and status filters."""

    # Dashboard statistics
    stats = SMSMessage.objects.aggregate(
        total=Count("id"),

        delivered=Count(
            "id",
            filter=Q(
                status__in=SMSMessage.DELIVERED_STATUSES
            )
        ),

        submitted=Count(
            "id",
            filter=Q(
                status__in=SMSMessage.PENDING_STATUSES
            )
        ),

        failed=Count(
            "id",
            filter=Q(
                status__in=SMSMessage.FAILED_STATUSES
            )
        ),
    )

    # Get search and filter values
    search_query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "all").strip()

    # Start with all messages
    sms_queryset = SMSMessage.objects.all()

    # Search by recipient, message, or provider status
    if search_query:
        sms_queryset = sms_queryset.filter(
            Q(recipient__icontains=search_query) |
            Q(body__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    # Filter by delivery status
    if selected_status == "delivered":
        sms_queryset = sms_queryset.filter(
            status__in=SMSMessage.DELIVERED_STATUSES
        )

    elif selected_status == "failed":
        sms_queryset = sms_queryset.filter(
            status__in=SMSMessage.FAILED_STATUSES
        )

    elif selected_status == "pending":
        sms_queryset = sms_queryset.filter(
            status__in=SMSMessage.PENDING_STATUSES
        )

    # Limit displayed messages to the latest 100
    sms_list = sms_queryset[:100]

    return render(
        request,
        "sms_app/history.html",
        {
            "stats": stats,
            "sms_list": sms_list,
            "search_query": search_query,
            "selected_status": selected_status,
        }
    )


@require_POST
def refresh_status_view(request, pk):
    """Refresh SMS delivery status using TextBee."""

    sms = get_object_or_404(SMSMessage, pk=pk)

    if not sms.provider_sid:
        messages.error(
            request,
            "This SMS has no TextBee batch ID. "
            "Its delivery status cannot be refreshed."
        )
        return redirect("sms_app:history")

    result = services.fetch_status(sms.provider_sid)

    if result.status:
        sms.status = result.status

        if result.error:
            sms.error_message = result.error
        elif result.status in SMSMessage.DELIVERED_STATUSES:
            sms.error_message = ""

        sms.save()

        if result.status in SMSMessage.FAILED_STATUSES:
            messages.error(
                request,
                "TextBee reports that this SMS failed."
            )
        else:
            messages.success(
                request,
                f"Status updated: {sms.stage_label}."
            )

    else:
        messages.error(
            request,
            result.error or "Unable to retrieve SMS status."
        )

    return redirect("sms_app:history")


@require_POST
def delete_sms_view(request, pk):
    """Delete an SMS record from message history."""

    sms = get_object_or_404(SMSMessage, pk=pk)

    sms.delete()

    messages.success(
        request,
        "SMS record successfully deleted from history."
    )

    return redirect("sms_app:history")
