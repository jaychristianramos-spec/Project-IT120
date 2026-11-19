import re

from django import forms
from django.conf import settings

E164_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")


def normalize_phone_number(raw: str) -> str:
    """
    Clean a phone number and convert it to E.164 format (e.g. +639171234567).

    - Spaces, dashes, dots and parentheses are removed.
    - "0917..." is converted using DEFAULT_COUNTRY_CODE (default +63).
    - "00xx..." is treated as "+xx...".
    Raises forms.ValidationError if the result is not a valid E.164 number.
    """
    number = re.sub(r"[\s\-\.\(\)]", "", raw or "")
    if not number:
        raise forms.ValidationError("Enter the recipient's phone number.")

    if number.startswith("00"):
        number = "+" + number[2:]
    elif number.startswith("0"):
        number = settings.DEFAULT_COUNTRY_CODE + number[1:]

    if not E164_PATTERN.match(number):
        raise forms.ValidationError(
            "Enter a valid phone number, such as +639171234567 or 09171234567."
        )
    return number


class SMSForm(forms.Form):
    recipient = forms.CharField(
        label="Recipient phone number",
        max_length=25,
        widget=forms.TextInput(
            attrs={"placeholder": "+639171234567", "autocomplete": "tel", "inputmode": "tel"}
        ),
        error_messages={"required": "Enter the recipient's phone number."},
    )
    message = forms.CharField(
        label="Message",
        max_length=settings.SMS_MAX_LENGTH,
        widget=forms.Textarea(
            attrs={"rows": 5, "placeholder": "Type your message here", "maxlength": settings.SMS_MAX_LENGTH}
        ),
        error_messages={
            "required": "Write a message before sending.",
            "max_length": f"Messages can be at most {settings.SMS_MAX_LENGTH} characters.",
        },
    )

    def clean_recipient(self):
        return normalize_phone_number(self.cleaned_data["recipient"])

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if not message:
            raise forms.ValidationError("Write a message before sending.")
        return message
