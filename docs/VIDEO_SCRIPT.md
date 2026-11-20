# Demonstration Video Script (target: about 6–7 minutes; allowed: 3–10)

**Before recording:** close the browser tabs showing the Textbee Dashboard and your `.env` file. Do NOT open `.env`, the Textbee dashboard with the API Key, or any terminal that prints secrets. Use an authorized test number and keep the paired Android gateway phone active. Record the screen with voice (OBS, Zoom, or Xbox Game Bar).

| Time | Who | What to show / say |
| :--- | :--- | :--- |
| 0:00–0:40 | **Ronymar Tejano** | Introduce the group and project: *"A Django app that sends SMS through Textbee (used as a free alternative to Twilio)."* State the purpose and users, and credit **Jay Christian Ramos** for the Django project setup, views, URLs, and core logic. |
| 0:40–1:30 | **Ronymar Tejano** | Show the GitHub repo (`Project-IT120`): folder structure, `README.md`, `requirements.txt`, `.gitignore`, `.env.example`. Show the commit history with everyone's commits. Mention that real credentials are not in the repo. |
| 1:30–2:15 | **Ronymar Tejano** | Open the running app. Walk through the Compose page: phone field, message box, Send SMS button, live character counter, and live preview. |
| 2:15–3:30 | **Marc Nino C. Salundaguit** | **Successful send:** enter an authorized test number and a short message, click **Send SMS**. Show the green notice and point out it says delivery is *not yet confirmed*. Show the SMS arriving on the phone. |
| 3:30–4:30 | **Marc Nino C. Salundaguit** | **Validation & error handling:** test empty number, empty message, and invalid number (`12345`), and explain how credential/network errors are safely caught without exposing secrets. |
| 4:30–5:15 | **Cobie Brian O. Babor** | **Automated tests:** run `python manage.py test` in VS Code and show 25 tests passing (with mocked Textbee requests). |
| 5:15–6:00 | **Cobie Brian O. Babor** | Open **History**: dashboard counts, masked numbers, statuses, click **Refresh status** and show the updated delivery status. |
| 6:00–7:00 | **Cobie Brian O. Babor** | Briefly explain technologies (Django, Requests for Textbee REST API, `python-dotenv`, SQLite, HTML/CSS), where the code lives (`forms.py`, `services.py`, `views.py`, `models.py`), security (env variables, CSRF, no secrets in Git), and **all 4 members' contributions** (Jay, Ronymar, Marc Nino, and Cobie). |

**Tips:** rehearse once; keep the receiving phone visible or screen-share its notification; all presenters should speak clearly to demonstrate full system understanding.
