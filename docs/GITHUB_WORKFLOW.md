GitHub Workflow for a Group of 4 (So Commit History Shows Everyone)
Repository Setup:

Jay Christian Ramos created the repository ([https://github.com/jaychristianramos-spec/Project-IT120](https://github.com/jaychristianramos-spec/Project-IT120)), added all group members as collaborators, and set the repository to Public so the instructor (prala-an@carsu.edu.ph) can inspect the code and commit history.

Initialize and Push the Base Project:

Bash
cd Project-IT120
git init
git add .
git status            # confirm .env and venv/ are NOT listed
git commit -m "Initial Django project setup"
git branch -M main
git remote add origin https://github.com/jaychristianramos-spec/Project-IT120.git
git push -u origin main
Each Member Clones, Creates a Branch, Commits Their Work, and Opens a Pull Request:

Bash
git clone https://github.com/jaychristianramos-spec/Project-IT120.git
cd Project-IT120
git checkout -b feature/<your-part>
git add .
git commit -m "Describe what YOU changed"
git push -u origin feature/<your-part>
(After pushing, open a Pull Request on GitHub and merge into main.)

Task & Commit Split Across All 4 Group Members:

Jay Christian Ramos: Django project setup (sms_project/settings.py, urls.py), views (views.py), and core application logic (feature/django-setup).

Cobie Brian O. Babor: Custom HTML/CSS user interface (templates/, static/sms_app/style.css), forms.py, phone number normalization, validation, and live character counter/preview (feature/ui-and-validation).

Marc Nini C. Salundaguit: Textbee REST API integration (services.py), environment configuration (.env.example, .gitignore), and sanitized error handling (feature/textbee-integration).

Ronymar Tejano: SMSMessage history and status tracking (models.py), unit tests (tests.py), README.md manual test results table, and demonstration video (feature/history-and-testing).

Security & Commit Hygiene:

Make small, meaningful commits rather than a single giant upload so every contributor appears clearly in the GitHub Insights/Commit history.

Before the final push, double-check that .env and venv/ were never committed. If an API key (TEXTBEE_API_KEY) is ever committed by accident, immediately revoke and regenerate a new key in the Textbee Dashboard (deleting the file alone does not remove it from Git history).
