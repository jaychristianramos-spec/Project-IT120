
"""
SMS provider integration using TextBee.

Views call send_sms() and fetch_status().
TextBee sends SMS through your registered Android phone.
"""

import logging
from dataclasses import dataclass

import requests
from django.conf import settings
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

TEXTBEE_BASE_URL = "https://api.textbee.dev/api/v1"


@dataclass
class SendResult:
    ok: bool
    status: str = ""
    sid: str = ""
    error: str = ""


def credentials_missing() -> list[str]:
    """Check whether TextBee credentials are configured."""

    missing = []

    if not getattr(settings, "TEXTBEE_API_KEY", ""):
        missing.append("TEXTBEE_API_KEY")

    return missing


def _headers():
    return {
        "x-api-key": settings.TEXTBEE_API_KEY,
        "Content-Type": "application/json",
    }


def _get_data(result):
    """Safely extract the API data object."""

    data = result.get("data", result)

    return data if isinstance(data, dict) else {}


def send_sms(to: str, body: str) -> SendResult:
    """Send an SMS using TextBee."""

    missing = credentials_missing()

    if missing:
        return SendResult(
            ok=False,
            status="rejected",
            error="TextBee is not configured. Check your API key.",
        )

    payload = {
        "recipients": [to],
        "message": body,
    }

    device_id = getattr(settings, "TEXTBEE_DEVICE_ID", "")

    if device_id:
        payload["deviceId"] = device_id

    try:
        response = requests.post(
            f"{TEXTBEE_BASE_URL}/gateway/send-sms",
            headers=_headers(),
            json=payload,
            timeout=30,
        )

        if not response.ok:
            try:
                error_data = response.json()
                error_message = (
                    error_data.get("message")
                    or error_data.get("error")
                    or "Check your TextBee account and device."
                )
            except ValueError:
                error_message = "Check your TextBee account and device."

            logger.warning(
                "TextBee rejected SMS. HTTP %s",
                response.status_code,
            )

            return SendResult(
                ok=False,
                status="rejected",
                error=f"TextBee error (HTTP {response.status_code}): {error_message}",
            )

        result = response.json()
        data = _get_data(result)

        if data.get("success") is False:
            return SendResult(
                ok=False,
                status="rejected",
                error=data.get(
                    "message",
                    "TextBee could not accept the message.",
                ),
            )

        batch_id = data.get("smsBatchId", "")

        # Some immediate-dispatch responses provide counts
        # instead of a batch ID.
        if not batch_id:
            failure_count = data.get("failureCount", 0)
            success_count = data.get("successCount", 0)

            if failure_count:
                return SendResult(
                    ok=False,
                    status="failed",
                    error="TextBee reports that the SMS could not be sent.",
                )

            if success_count:
                return SendResult(
                    ok=True,
                    status="sent",
                )

        return SendResult(
            ok=True,
            status="pending",
            sid=batch_id,
        )

    except RequestException as exc:
        logger.warning(
            "TextBee connection error: %s",
            type(exc).__name__,
        )

        return SendResult(
            ok=False,
            status="rejected",
            error="Could not connect to TextBee. Check your internet connection.",
        )

    except (ValueError, TypeError, AttributeError):
        logger.exception("Invalid TextBee response")

        return SendResult(
            ok=False,
            status="rejected",
            error="TextBee returned an invalid response.",
        )

    except Exception:
        logger.exception("Unexpected TextBee sending error")

        return SendResult(
            ok=False,
            status="rejected",
            error="Something went wrong while sending. Please try again.",
        )


def fetch_status(sid: str) -> SendResult:
    """
    Check the status of a TextBee SMS batch.

    Reads the individual message status rather than relying
    only on the overall batch status.
    """

    missing = credentials_missing()

    if missing:
        return SendResult(
            ok=False,
            error="TextBee is not configured. Check your API key.",
        )

    device_id = getattr(settings, "TEXTBEE_DEVICE_ID", "")

    if not device_id:
        return SendResult(
            ok=False,
            error="Configure TEXTBEE_DEVICE_ID to check delivery status.",
        )

    if not sid:
        return SendResult(
            ok=False,
            error="No TextBee batch ID is available for this message.",
        )

    try:
        response = requests.get(
            f"{TEXTBEE_BASE_URL}/gateway/devices/{device_id}/sms-batch/{sid}",
            headers=_headers(),
            timeout=30,
        )

        if not response.ok:
            return SendResult(
                ok=False,
                error=f"Could not retrieve TextBee status (HTTP {response.status_code}).",
            )

        result = response.json()
        data = _get_data(result)

        batch = data.get("batch", data)

        # Read the individual recipient's status.
        sms_messages = data.get("messages", [])

        if sms_messages:
            message = sms_messages[0]
            status = message.get("status", "unknown")

            error_message = (
                message.get("errorMessage")
                or message.get("error_message")
                or ""
            )

        else:
            # Fallback to batch status if individual
            # message information is unavailable.
            batch_status = batch.get("status", "unknown")

            batch_status_map = {
                "pending": "pending",
                "processing": "processing",
                "completed": "sent",
                "partial_success": "unknown",
                "failed": "failed",
                "unknown": "unknown",
            }

            status = batch_status_map.get(
                batch_status,
                "unknown",
            )

            error_message = ""

        status = str(status).lower()

        # TextBee delivery_failed is also treated as a failure.
        if status == "delivery_failed":
            status = "failed"

        return SendResult(
            ok=True,
            status=status,
            sid=sid,
            error=error_message,
        )

    except RequestException as exc:
        logger.warning(
            "TextBee status connection error: %s",
            type(exc).__name__,
        )

        return SendResult(
            ok=False,
            error="Could not connect to TextBee to check delivery status.",
        )

    except (ValueError, TypeError, AttributeError):
        logger.exception("Invalid TextBee status response")

        return SendResult(
            ok=False,
            error="TextBee returned an invalid status response.",
        )

    except Exception:
        logger.exception("Unexpected TextBee status error")

        return SendResult(
            ok=False,
            error="Something went wrong while checking SMS status.",
        )
