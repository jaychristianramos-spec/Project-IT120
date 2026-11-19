# Demonstration Video Script (target: about 6–7 minutes; allowed: 3–10)

**Before recording:** close the browser tabs showing the Twilio Console and your `.env` file. Do NOT open `.env`, the Twilio dashboard with the Auth Token, or any terminal that prints secrets. Use a verified test number. Record the screen with voice (OBS, Zoom, or Xbox Game Bar).

| Time | Who | What to show / say |
|---|---|---|
| 0:00–0:40 | Member 1 | Introduce the group and project: "A Django app that sends SMS through Twilio." State the purpose and users. |
| 0:40–1:30 | Member 1 | Show the GitHub repo: folder structure, README, requirements.txt, `.gitignore`, `.env.example`. Show the commit history with everyone's commits. Mention that real credentials are not in the repo. |
| 1:30–2:15 | Member 2 | Open the running app. Walk through the Compose page: phone field, message box, Send SMS button, live character counter, live preview. |
| 2:15–3:30 | Member 3 | **Successful send:** enter an authorized/verified number and a short message, click Send SMS. Show the green notice and point out it says delivery is *not yet confirmed*. Show the SMS arriving on the phone. |
| 3:30–4:30 | Member 2 | **Validation tests:** submit an empty number, then an empty message, then an invalid number (`12345`). Show each error message. |
| 4:30–5:15 | Member 3 | **Error handling:** show one provider/credential error (e.g. an unverified number on a trial account), or run `python manage.py test` and show 25 tests passing. |
| 5:15–6:00 | Member 3 | Open History: dashboard counts, statuses, click **Refresh status** and show it change to Delivered. |
| 6:00–7:00 | All | Briefly explain technologies (Django, Twilio SDK, python-dotenv, SQLite), where the code lives (`forms.py` validation, `services.py` Twilio, `views.py` logic), security (env variables, CSRF, no secrets in Git), and **each member's contribution**. |

**Tips:** rehearse once; keep the phone visible or screen-share its notification; every member should speak so each can show understanding.
