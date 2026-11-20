# Textbox – Django SMS Sender

**Course:** IT 120 – Integrative Programming and Technologies (1st Sem SY 2026–2027)  
**Activity:** Group Assignment – Build a Django Application for Sending SMS

A Django web application that lets a user type a recipient phone number and a message, validates the input, sends the SMS through **Textbee** (used as a free, open-source alternative SMS gateway instead of Twilio), and shows clear success or failure feedback. Every attempt is saved so its delivery status can be tracked later.

## Group Members and Responsibilities

| Member | Responsibility |
| :--- | :--- |
| **Jay Christian Ramos** | Django project setup, views, URLs, application logic |
| **Cobie Brian O. Babor** | User interface (`HTML/CSS`), forms, phone normalization, validation, 3rd video presenter |
| **Marc Nino C. Salundaguit** | Textbee SMS gateway integration (`services.py`), environment security, 2nd video presenter |
| **Ronymar Tejano** | History & status tracking (`SMSMessage`), system testing, documentation, 1st video presenter |

All members reviewed and understand the whole system.

## Application Objectives
- **Purpose:** let a user send a short text message to a phone number from a web page using Textbee as a free alternative instead of Twilio.
- **Users:** anyone who needs to send quick notifications from a browser (here, the group and the instructor during testing).
- **SMS functionality:** validated form → Textbee API → success/failure feedback → saved history with delivery status.

## SMS Workflow
1. User opens the Compose page.
2. User enters the recipient number and the message (live character counter and preview help here).
3. Django validates both fields; the number is normalized to international (E.164) format, e.g. `09171234567` → `+639171234567`.
4. If valid, `services.send_sms()` submits the message to Textbee.
5. The result is saved as an `SMSMessage` record and shown to the user.
6. On the History page, **Refresh status** asks Textbee for the latest status.

**Submitted ≠ delivered.** When Textbee accepts a request the app reports *"submitted – delivery not confirmed"*. It only shows **Delivered** after delivery is confirmed.

## Main Features
- SMS compose form (recipient, message, Send SMS button)
- Input validation and friendly error messages
- Handling of missing/wrong credentials, network errors, and provider rejections (with no secrets exposed)
- Additional features: character counter with SMS segment count, live message preview, message history, dashboard of attempts, and delivery-status tracking
- CSRF protection, credentials in environment variables, masked phone numbers in the history list

## Technologies and Dependencies
Python 3.10+, Django, Requests (`requests`) for Textbee REST API integration (alternative to Twilio), `python-dotenv`, SQLite, HTML/CSS (no external front-end libraries). Full list with versions: `requirements.txt`.

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
```

## Installation and Setup

```bash
git clone [https://github.com/jaychristianramos-spec/Project-IT120.git](https://github.com/jaychristianramos-spec/Project-IT120.git)
cd Project-IT120

python -m venv venv
# Windows:      venv\Scripts\activate
# macOS/Linux:  source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env        # Windows: copy .env.example .env
# then edit .env and fill in your values (see next section)

python manage.py migrate
```

## Configuring Textbee (Alternative to Twilio)
We chose **Textbee** (`https://textbee.dev/`) as a free, open-source alternative instead of Twilio to avoid paid SMS credits and trial restrictions.

1. Create a free account at https://textbee.dev/.
2. Install the **Textbee Android App** on an active Android phone with a working SIM card and SMS load/promo, and link the phone to your Textbee dashboard.
3. In the Textbee dashboard, copy your **API Key** and **Device ID**.
4. Put the values in `.env`:
   - `TEXTBEE_API_KEY`, `TEXTBEE_DEVICE_ID`
   - `DEFAULT_COUNTRY_CODE=+63`
5. Never commit `.env`. It is already listed in `.gitignore`.

Generate a Django secret key for `.env` with:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

## Running the Application

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/. Optional admin: `python manage.py createsuperuser`, then http://127.0.0.1:8000/admin/.

## Testing

### Automated tests (Textbee API is mocked – no real SMS is sent)

```bash
python manage.py test
```

Result: 25 tests, all passing (phone normalization, form validation, missing credentials, invalid number, network error, provider rejection, success-without-false-delivery claim, CSRF, history, status refresh).

### Manual test results

| # | Test case | Expected result | Actual result | Pass? |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Valid recipient number + message | Message submitted; green notice says delivery not confirmed; entry in History | Message submitted via Textbee; green notice confirmed submission (delivery not confirmed); entry in History | Yes |
| 2 | Empty phone number | "Enter the recipient's phone number."; nothing sent | "Enter the recipient's phone number."; nothing sent | Yes |
| 3 | Empty message | "Write a message before sending."; nothing sent | "Write a message before sending."; nothing sent | Yes |
| 4 | Invalid number (`12345`) | "Enter a valid phone number…"; nothing sent | "Enter a valid phone number…"; nothing sent | Yes |
| 5 | Wrong API Key in `.env` | "Textbee rejected the credentials…"; no secrets shown | "Textbee rejected the credentials…"; no secrets shown | Yes |
| 6 | Missing credentials in `.env` | "The SMS service is not configured…" | "The SMS service is not configured…" | Yes |
| 7 | Internet disconnected | "Could not reach the SMS provider…" | "Could not reach the SMS provider…" | Yes |
| 8 | Offline/disconnected Android gateway device | Message about gateway device error/rejection | Gateway rejection error shown cleanly; no secrets exposed | Yes |
| 9 | Refresh status in History | Status updates to Delivered / Failed from Textbee | Status updated to Delivered / Failed from Textbee | Yes |

## Known Limitations
- No user login; anyone who can open the site can send messages (acceptable for a classroom demo, add authentication before any real deployment).
- Delivery status is fetched on demand (**Refresh status**) rather than via webhooks.
- Textbee depends on the paired Android phone staying connected to the internet with active mobile signal and SMS load.
- SQLite is used for simplicity.

## Security Notes
- Credentials are read from environment variables / `.env` (ignored by Git).
- CSRF middleware and `{% csrf_token %}` protect every form.
- Error messages shown to users never include credentials; technical details go to server logs only.
- Use only authorized test recipients and follow standard messaging policies.
