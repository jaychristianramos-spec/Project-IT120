"""
Automated tests. Twilio is always mocked, so no real SMS is sent and no
credentials are needed. Run with:  python manage.py test
"""
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from django.urls import reverse
from requests.exceptions import ConnectionError as RequestsConnectionError
from twilio.base.exceptions import TwilioRestException

from . import services
from .forms import SMSForm, normalize_phone_number
from .models import SMSMessage

GOOD_CREDS = dict(
    TWILIO_ACCOUNT_SID="ACtest", TWILIO_AUTH_TOKEN="token",
    TWILIO_PHONE_NUMBER="+15005550006", TWILIO_MESSAGING_SERVICE_SID="",
)


class PhoneNormalizationTests(TestCase):
    def test_local_number_converted(self):
        self.assertEqual(normalize_phone_number("0917 123 4567"), "+639171234567")

    def test_international_number_kept(self):
        self.assertEqual(normalize_phone_number("+63 917-123-4567"), "+639171234567")

    def test_double_zero_prefix(self):
        self.assertEqual(normalize_phone_number("0063917 1234567"), "+639171234567")

    def test_invalid_numbers_rejected(self):
        for bad in ["abc", "12345", "+12", "+0123456789", "9171234567890123456"]:
            with self.subTest(bad=bad):
                with self.assertRaises(Exception):
                    normalize_phone_number(bad)


class FormValidationTests(TestCase):
    def test_empty_phone(self):
        form = SMSForm({"recipient": "", "message": "Hi"})
        self.assertFalse(form.is_valid())
        self.assertIn("recipient", form.errors)

    def test_empty_message(self):
        form = SMSForm({"recipient": "+639171234567", "message": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_whitespace_only_message(self):
        form = SMSForm({"recipient": "+639171234567", "message": "   \n "})
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_message_too_long(self):
        form = SMSForm({"recipient": "+639171234567", "message": "x" * 481})
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        form = SMSForm({"recipient": "09171234567", "message": " Hello "})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["recipient"], "+639171234567")
        self.assertEqual(form.cleaned_data["message"], "Hello")


@override_settings(**GOOD_CREDS)
class ServiceTests(TestCase):
    @patch("sms_app.services.Client")
    def test_success_is_submission_not_delivery(self, client_cls):
        client_cls.return_value.messages.create.return_value = SimpleNamespace(sid="SM123", status="queued")
        result = services.send_sms("+639171234567", "Hi")
        self.assertTrue(result.ok)
        self.assertEqual(result.status, "queued")
        self.assertEqual(result.sid, "SM123")

    @override_settings(TWILIO_ACCOUNT_SID="", TWILIO_AUTH_TOKEN="")
    def test_missing_credentials(self):
        result = services.send_sms("+639171234567", "Hi")
        self.assertFalse(result.ok)
        self.assertIn("not configured", result.error)

    @patch("sms_app.services.Client")
    def test_invalid_number_rejected_by_provider(self, client_cls):
        client_cls.return_value.messages.create.side_effect = TwilioRestException(400, "uri", "bad", code=21211)
        result = services.send_sms("+639171234567", "Hi")
        self.assertFalse(result.ok)
        self.assertIn("not valid", result.error)

    @patch("sms_app.services.Client")
    def test_wrong_credentials_error_hides_secrets(self, client_cls):
        client_cls.return_value.messages.create.side_effect = TwilioRestException(401, "uri", "Authenticate", code=20003)
        result = services.send_sms("+639171234567", "Hi")
        self.assertFalse(result.ok)
        self.assertNotIn("token", result.error.lower().replace("auth token", ""))
        self.assertNotIn("ACtest", result.error)

    @patch("sms_app.services.Client")
    def test_network_error(self, client_cls):
        client_cls.return_value.messages.create.side_effect = RequestsConnectionError("boom")
        result = services.send_sms("+639171234567", "Hi")
        self.assertFalse(result.ok)
        self.assertIn("Could not reach", result.error)

    @patch("sms_app.services.Client")
    def test_fetch_status_delivered(self, client_cls):
        client_cls.return_value.messages.return_value.fetch.return_value = SimpleNamespace(
            status="delivered", sid="SM123", error_code=None
        )
        result = services.fetch_status("SM123")
        self.assertTrue(result.ok)
        self.assertEqual(result.status, "delivered")


@override_settings(**GOOD_CREDS)
class ViewTests(TestCase):
    def post(self, recipient, message):
        return self.client.post(reverse("sms_app:send"), {"recipient": recipient, "message": message}, follow=True)

    def test_page_loads(self):
        r = self.client.get(reverse("sms_app:send"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Send SMS")

    @patch("sms_app.views.services.send_sms")
    def test_empty_phone_not_sent(self, send):
        r = self.post("", "Hello")
        self.assertContains(r, "Enter the recipient")
        send.assert_not_called()
        self.assertEqual(SMSMessage.objects.count(), 0)

    @patch("sms_app.views.services.send_sms")
    def test_empty_message_not_sent(self, send):
        r = self.post("+639171234567", "")
        self.assertContains(r, "Write a message")
        send.assert_not_called()

    @patch("sms_app.views.services.send_sms")
    def test_invalid_phone_not_sent(self, send):
        r = self.post("12345", "Hello")
        self.assertContains(r, "valid phone number")
        send.assert_not_called()

    @patch("sms_app.views.services.send_sms")
    def test_success_message_does_not_claim_delivery(self, send):
        send.return_value = services.SendResult(ok=True, status="queued", sid="SM1")
        r = self.post("+639171234567", "Hello")
        self.assertContains(r, "submitted to Twilio")
        self.assertContains(r, "not confirmed")
        sms = SMSMessage.objects.get()
        self.assertEqual(sms.stage, "submitted")
        self.assertEqual(sms.provider_sid, "SM1")

    @patch("sms_app.views.services.send_sms")
    def test_provider_failure_shown_and_logged(self, send):
        send.return_value = services.SendResult(ok=False, status="rejected", error="The recipient phone number is not valid.")
        r = self.post("+639171234567", "Hello")
        self.assertContains(r, "Message not sent")
        self.assertEqual(SMSMessage.objects.get().stage, "failed")

    def test_csrf_enforced(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        r = c.post(reverse("sms_app:send"), {"recipient": "+639171234567", "message": "Hi"})
        self.assertEqual(r.status_code, 403)

    def test_history_empty_and_populated(self):
        self.assertContains(self.client.get(reverse("sms_app:history")), "No messages yet")
        SMSMessage.objects.create(recipient="+639171234567", body="Hi", status="queued", provider_sid="SM1")
        r = self.client.get(reverse("sms_app:history"))
        self.assertContains(r, "Refresh status")
        self.assertContains(r, "delivery not confirmed")

    @patch("sms_app.views.services.fetch_status")
    def test_refresh_updates_to_delivered(self, fetch):
        sms = SMSMessage.objects.create(recipient="+639171234567", body="Hi", status="queued", provider_sid="SM1")
        fetch.return_value = services.SendResult(ok=True, status="delivered", sid="SM1")
        self.client.post(reverse("sms_app:refresh", args=[sms.pk]))
        sms.refresh_from_db()
        self.assertEqual(sms.stage, "delivered")

    def test_refresh_requires_post(self):
        sms = SMSMessage.objects.create(recipient="+639171234567", body="Hi", status="queued", provider_sid="SM1")
        self.assertEqual(self.client.get(reverse("sms_app:refresh", args=[sms.pk])).status_code, 405)
