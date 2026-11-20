# Textbox – Django SMS Sender

**Course:** IT 120 – Integrative Programming and Technologies (1st Sem SY 2026–2027)  
**Activity:** Group Assignment – Build a Django Application for Sending SMS

A Django web application that lets a user type a recipient phone number and a message, validates the input, sends the SMS through **Textbee** (used as a free, open-source alternative SMS gateway instead of Twilio), and shows clear success or failure feedback. Every attempt is saved so its delivery status can be tracked later.

---

## Group Members and Responsibilities

| Member | Responsibility |
| :--- | :--- |
| **Jay Christian Ramos** | Django project setup, views, URLs, application logic |
| **Cobie Brian O. Babor** | User interface (`HTML/CSS`), forms, phone normalization, validation, video presenter |
| **Marc Nini C. Salundaguit** | Textbee SMS gateway integration (`services.py`), environment security, video presenter |
| **Ronymar Tejano** | History & status tracking (`SMSMessage`), system testing, documentation, demo video recording & presentation |


---

## Application Objectives
- **Purpose:** let a user send a short text message to a phone number from a web page using Textbee as a free alternative instead of Twilio.
- **Users:** anyone who needs to send quick notifications from a browser (here, the group and the instructor during testing).
- **SMS functionality:** validated form → Textbee API → success/failure feedback → saved history with delivery status.

---

## SMS Workflow
1. User opens the Compose page.
2. User enters the recipient number and the message (live character counter and preview help here).
3. Django validates both fields; the number is normalized to international (E.164) format, e.g. `09171234567` → `+639171234567`.
4. If valid, `services.send_sms()` submits the message to Textbee.
5. The result is saved as an `SMSMessage` record and shown to the user.
6. On the History page, **Refresh status** checks Textbee for the latest status.

> **Submitted ≠ delivered.** When Textbee accepts a request the app reports *"submitted – delivery not confirmed"*. It only shows **Delivered** after delivery is confirmed.

---

## Main Features
- SMS compose form (recipient, message, Send SMS button)
- Input validation and friendly error messages
- Handling of missing/wrong credentials, network errors, and provider rejections (with no secrets exposed)
- Additional features: character counter with SMS segment count, live message preview, message history, dashboard of attempts, and delivery-status tracking
- CSRF protection, credentials in environment variables, masked phone numbers in the history list

---

## Technologies and Dependencies
Python 3.10+, Django, Requests (`requests`) for Textbee REST API integration (alternative to Twilio), `python-dotenv`, SQLite, HTML/CSS (no external front-end libraries). Full list with versions: `requirements.txt`.

---

## Project Structure
```text
Project-IT120/          <- repository root
├── docs/               <- project documentation & guides
├── sms_project/        <- settings.py, urls.py
├── sms_app/            <- models.py, forms.py, services.py, views.py, urls.py, templates/, static/
├── .env.example        <- safe placeholders only
├── .gitattributes
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
