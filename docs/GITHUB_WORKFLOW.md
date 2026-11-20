# GitHub workflow for a group of 4 (so commit history shows everyone)

1. **Jay Christian Ramos** creates a repo on GitHub (`Project-IT120`), adds the other members and the instructor as collaborators (or makes it public).

2. Initialize and push:
   ```bash
   cd Project-IT120
   git init
   git add .
   git status            # confirm .env and venv/ are NOT listed
   git commit -m "Initial Django project setup"
   git branch -M main
   git remote add origin [https://github.com/jaychristianramos-spec/Project-IT120.git](https://github.com/jaychristianramos-spec/Project-IT120.git)
   git push -u origin main
   ```

3. **Each member** clones, creates a branch, commits their own work, and opens a pull request:
   ```bash
   git clone [https://github.com/jaychristianramos-spec/Project-IT120.git](https://github.com/jaychristianramos-spec/Project-IT120.git)
   git checkout -b feature/<your-part>
   git add .
   git commit -m "Describe what YOU changed"
   git push -u origin feature/<your-part>
   ```

4. Suggested split of commits so each member has real work to show:
   - **Jay Christian Ramos:** project settings, URLs, views, application logic.
   - **Cobie Brian O. Babor:** `forms.py`, templates, CSS, counter/preview JavaScript.
   - **Marc Nini C. Salundaguit:** `services.py` (Textbee), `.env.example`, `.gitignore`.
   - **Ronymar Tejano:** `models.py` (`SMSMessage` history + status), `tests.py`, README test table, demo video.
