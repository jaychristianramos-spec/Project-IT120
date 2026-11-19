
from django.db import models


class SMSMessage(models.Model):
    """One SMS sending attempt using TextBee."""

    # TextBee statuses that mean the message is still being processed
    # or accepted by the phone gateway.
    PENDING_STATUSES = {
        "pending",
        "processing",
        "dispatched",
        "sent",
        "completed",
        "partial_success",
        "unknown",
    }

    # Only confirmed delivery statuses belong here.
    DELIVERED_STATUSES = {
        "delivered",
        "read",
    }

    # Failed or rejected messages.
    FAILED_STATUSES = {
        "failed",
        "undelivered",
        "canceled",
        "rejected",
    }

    recipient = models.CharField(max_length=20)
    body = models.TextField()

    status = models.CharField(max_length=30, default="failed")

    # TextBee SMS batch ID
    provider_sid = models.CharField(max_length=100, blank=True)

    error_message = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.recipient} [{self.status}] "
            f"{self.created_at:%Y-%m-%d %H:%M}"
        )

    @property
    def stage(self):
        """Classify the SMS sending status."""

        status = self.status.lower()

        if status in self.DELIVERED_STATUSES:
            return "delivered"

        if status in self.FAILED_STATUSES:
            return "failed"

        return "submitted"

    @property
    def stage_label(self):
        """Display a readable SMS status."""

        return {
            "delivered": "Delivered",
            "submitted": "Submitted to TextBee (delivery not confirmed)",
            "failed": "Failed",
        }[self.stage]

    @property
    def masked_recipient(self):
        """Hide part of the recipient's phone number."""

        r = self.recipient

        return (
            f"{r[:4]}{'*' * max(len(r) - 7, 0)}{r[-3:]}"
            if len(r) > 7
            else r
        )
