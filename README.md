# Textbox – Django SMS Sender

**Course:** IT 120 – Integrative Programming and Technologies (1st Sem SY 2026–2027)  
**Activity:** Group Assignment – Build a Django Application for Sending SMS

A Django web application that lets a user type a recipient phone number and a message, validates the input, sends the SMS through the **Textbee SMS Gateway API** (chosen as a free, open-source alternative instead of Twilio), and shows clear success or failure feedback. Every attempt is saved so its status can be tracked later.

---

## Group Members and Responsibilities

| Member | Responsibility |
| :--- | :--- |
| **[Jay Christian Ramos]** | Django project setup, views, URLs, application logic |
| **[Cobie Brian O. Babor]** | User interface (`HTML/CSS`), forms, phone normalization, validation, video presenter |
| **[Marc Nini C. Salundaguit]** | Textbee SMS gateway integration (`services.py`), environment security, video presenter |
| **[Ronymar Tejano]** | History & status tracking (`SMSMessage`), system testing, documentation, demo video recording & presentation |


---

## SMS Provider Choice (Why Textbee Instead of Twilio)

Instead of Twilio—which requires paid credits or paid upgrades for full SMS sending—our group implemented **Textbee** (`https://textbee.dev/`) as an alternative SMS gateway. Textbee is an open-source Android-based SMS gateway that connects our Django backend to a paired Android smartphone via a REST API, allowing us to send real SMS messages using an existing mobile SIM and SMS promo without paid third-party gateway fees.

---

## Application Objectives

* **Purpose:** Let a user send a short text message to a phone number from a web page using a free Android-based SMS gateway alternative (Textbee) instead of Twilio.
* **Users:** Anyone who needs to send quick notifications from a browser (here, the group and the instructor during testing).
* **SMS Functionality:** Validated form → Textbee REST API → success/failure feedback → saved history with status tracking.

---

## SMS Workflow

1. User opens the **Compose** page (`send.html`).
2. User enters the recipient number and the message (live character counter and preview help here).
3. Django validates both fields; the number is normalized to international (E.164) format (e.g., `09171234567` → `+639171234567`).
4. If valid, `services.send_sms()` sends an HTTP POST request to the Textbee REST API using the configured API Key and Device ID.
5. The result is saved as an `SMSMessage` record and shown to the user.
6. On the **History** page (`history.html`), users can review past dispatch logs and track message status.

> **Submitted ≠ Delivered:** When Textbee accepts an API request, the app reports *"submitted – delivery not confirmed"*, since final carrier delivery depends on the connected Android device's mobile network.

---

## Main Features

* **SMS Compose Form:** Recipient phone number field, message body input, and **Send SMS** button.
* **Input Validation & Error Handling:** Friendly error messages for missing fields, invalid phone formats, missing/invalid API keys, disconnected gateway devices, network errors, and provider rejections (with no secrets exposed).
* **Additional Features:**
  * Live character counter with SMS segment count
  * Live message preview box
  * Message history log and dashboard of attempts
  * Status tracking in the History view
* **Security Features:** Django CSRF protection (`{% csrf_token %}`), API credentials stored in environment variables (`.env`), and masked phone numbers in the history list.

---

## Technologies and Dependencies

* **Backend:** Python 3.10+, Django
* **HTTP / SMS Gateway Integration:** `requests` library communicating with **Textbee SMS Gateway API** (`https://api.textbee.dev`) as a free alternative to Twilio
* **Environment Management:** `python-dotenv`
* **Database:** SQLite
* **Frontend:** Custom HTML/CSS (`static/sms_app/style.css`, no external front-end libraries)

Full package list with exact versions is located in `requirements.txt`.

---

## Project Structure

```text
sms_project/                <- repository root
├── manage.py
├── requirements.txt
├── .env.example            <- safe placeholders only
├── .gitignore
├── sms_project/            <- settings.py, urls.py
└── sms_app/
    ├── models.py           <- SMSMessage (history + status)
    ├── forms.py            <- validation + phone normalization
    ├── services.py         <- all Textbee API communication + error handling
    ├── views.py, urls.py, admin.py, tests.py
    ├── templates/sms_app/  <- base.html, send.html, history.html
    └── static/sms_app/style.css
