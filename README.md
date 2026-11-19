# Textbox – Django SMS Sender

**Course:** IT 120 – Integrative Programming and Technologies (1st Sem SY 2026–2027)
**Activity:** Group Assignment – Build a Django Application for Sending SMS

A Django web application that lets a user type a recipient phone number and a message, validates the input, sends the SMS through **Twilio**, and shows clear success or failure feedback. Every attempt is saved so its delivery status can be tracked later.

## Group Members and Responsibilities

| Member | Responsibility |
|---|---|
| [Member 1 name] | Django project setup, views, URLs, application logic |
| [Member 2 name] | User interface, forms, validation, user feedback |
| [Member 3 name] | Twilio integration, testing, documentation, demo video |

> Replace the placeholders above. All members reviewed and understand the whole system.

## Application Objectives
- **Purpose:** let a user send a short text message to a phone number from a web page.
- **Users:** anyone who needs to send quick notifications from a browser (here, the group and the instructor during testing).
- **SMS functionality:** validated form → Twilio API → success/failure feedback → saved history with delivery status.

## SMS Workflow
1. User opens the **Compose** page.
2. User enters the recipient number and the message (live character counter and preview help here).
3. Django validates both fields; the number is normalized to international (E.164) format, e.g. `09171234567` → `+639171234567`.
4. If valid, `services.send_sms()` submits the message to Twilio.
5. The result is saved as an `SMSMessage` record and shown to the user.
6. On the **History** page, **Refresh status** asks Twilio for the latest status.

> **Submitted ≠ delivered.** When Twilio accepts a request the app reports *"submitted – delivery not confirmed"*. It only shows **Delivered** after Twilio reports `delivered`.

## Main Features
- SMS compose form (recipient, message, Send SMS button)
- Input validation and friendly error messages
- Handling of missing/wrong credentials, network errors, and provider rejections (with no secrets exposed)
- **Additional features:** character counter with SMS segment count, live message preview, message history, dashboard of attempts, and delivery-status tracking
- CSRF protection, credentials in environment variables, masked phone numbers in the history list

## Technologies and Dependencies
Python 3.10+, Django, Twilio Python SDK, python-dotenv, SQLite, HTML/CSS (no external front-end libraries). Full list with versions: `requirements.txt`.

## Project Structure
```
sms_project/            <- repository root
├── manage.py
├── requirements.txt
├── .env.example        <- safe placeholders only
├── .gitignore
├── sms_project/        <- settings.py, urls.py
└── sms_app/
    ├── models.py       <- SMSMessage (history + status)
    ├── forms.py        <- validation + phone normalization
    ├── services.py     <- all Twilio communication + error handling
    ├── views.py, urls.py, admin.py, tests.py
    ├── templates/sms_app/  <- base.html, send.html, history.html
    └── static/sms_app/style.css
```

## Installation and Setup
```bash
git clone <your-repository-url>
cd sms_project

python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env        # Windows: copy .env.example .env
# then edit .env and fill in your values (see next section)

python manage.py migrate
```

## Configuring Twilio
1. Create an account at <https://www.twilio.com/try-twilio>.
2. In the **Twilio Console** dashboard, copy your **Account SID** and **Auth Token**.
3. Get a Twilio phone number (Console → Phone Numbers → Buy/Get a number; the trial gives one) **or** create a Messaging Service and copy its SID.
4. **Trial accounts** can only text numbers you have verified: Console → Phone Numbers → *Verified Caller IDs* → add and verify the recipient. Also check that your Twilio geo-permissions allow the destination country (Console → Messaging → Settings → Geo permissions).
5. Put the values in `.env`:
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
   - `TWILIO_PHONE_NUMBER` **or** `TWILIO_MESSAGING_SERVICE_SID`
6. Never commit `.env`. It is already listed in `.gitignore`.

Generate a Django secret key for `.env` with:
```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

## Running the Application
```bash
python manage.py runserver
```
Open <http://127.0.0.1:8000/>. Optional admin: `python manage.py createsuperuser`, then <http://127.0.0.1:8000/admin/>.

## Testing

### Automated tests (Twilio is mocked – no real SMS is sent)
```bash
python manage.py test
```
Result: **25 tests, all passing** (phone normalization, form validation, missing credentials, invalid number, network error, provider rejection, success-without-false-delivery claim, CSRF, history, status refresh).

### Manual test results
Fill in the *Actual result* column after running each case yourself with your own Twilio account.

| # | Test case | Expected result | Actual result | Pass? |
|---|---|---|---|---|
| 1 | Valid verified number + message | Message submitted; green notice says delivery not confirmed; entry in History | | |
| 2 | Empty phone number | "Enter the recipient's phone number."; nothing sent | | |
| 3 | Empty message | "Write a message before sending."; nothing sent | | |
| 4 | Invalid number (`12345`) | "Enter a valid phone number…"; nothing sent | | |
| 5 | Wrong Auth Token in `.env` | "Twilio rejected the credentials…"; no secrets shown | | |
| 6 | Missing credentials in `.env` | "The SMS service is not configured…" | | |
| 7 | Internet disconnected | "Could not reach the SMS provider…" | | |
| 8 | Unverified recipient on trial account | Message about verifying the number in Twilio | | |
| 9 | Refresh status in History | Status updates to Delivered / Failed from Twilio | | |

## Known Limitations
- No user login; anyone who can open the site can send messages (acceptable for a classroom demo, add authentication before any real deployment).
- Delivery status is fetched on demand (Refresh status) rather than via Twilio webhooks.
- Twilio trial accounts can only message verified numbers and prefix messages with a trial notice.
- SQLite is used for simplicity.

## Security Notes
- Credentials are read from environment variables / `.env` (ignored by Git).
- CSRF middleware and ``{% csrf_token %}`` protect every form.
- Error messages shown to users never include credentials; technical details go to server logs only.
- Use only authorized test recipients and follow Twilio's messaging policy.
