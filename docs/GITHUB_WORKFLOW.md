# GitHub workflow for a group of 3 (so commit history shows everyone)



**One member** creates a repo on GitHub (e.g. `it120-django-sms`), adds the other members and the instructor as collaborators (or makes it public).
Initialize and push:
```bash

cd sms_project

git init

git add .

git status # confirm .env and .venv are NOT listed

git commit -m "Initial Django project setup"

git branch -M main

git remote add origin https://github.com/<user>/<repo>.git

git push -u origin main

```

3. **Each member** clones, creates a branch, commits their own work, and opens a pull request:

```bash

git clone https://github.com/<user>/<repo>.git

git checkout -b feature/<your-part>

git add .

git commit -m "Describe what YOU changed"

git push -u origin feature/<your-part>

```

4. Suggested split of commits so each member has real work to show:

**Member 1:** project settings, URLs, views, model + migration.
**Member 2:** `forms.py`, templates, CSS, counter/preview JavaScript.
**Member 3:** `services.py` (Twilio), `tests.py`, README test table, demo video.
5. Make small, meaningful commits (not one giant upload). Before the final push, double check no secrets were ever committed. If a key was committed by accident, **rotate it in the Twilio Console** (deleting the file is not enough). make it just like this
