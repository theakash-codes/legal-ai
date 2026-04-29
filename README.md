<<<<<<< HEAD
# legal-ai
LegalAI Pro is an intelligent legal document assistant that uses machine learning to summarize documents, detect risks, identify fraud patterns, and provide simplified legal insights through an interactive web interface
=======
# Django Backend for Provided Frontend

This project is a minimal Django REST backend to work with the static frontend you uploaded.
It provides:

- Signup, Login, Logout endpoints using token authentication.
- `/upload` endpoint (POST) to upload a file (text or PDF) and receive a simple summary.
- `/generate` endpoint (POST) to generate a simple draft from text/summary.
- `/api/documents/` (GET) to list uploaded documents.

## Quick setup (on your machine)

1. Create a Python virtualenv and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations and create a superuser (optional):
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```

5. The frontend expects endpoints at:
   - `http://127.0.0.1:8000/upload` for file uploads (POST form-data `file`, `target_lang`)
   - `http://127.0.0.1:8000/generate` for draft generation (POST JSON `{'text': '...'}`)
   - `http://127.0.0.1:8000/auth/signup` and `/auth/login` for auth (POST JSON `username`, `password`)
   - `http://127.0.0.1:8000/api/documents/` to list uploaded documents

## Notes

- This backend uses a very simple summarization function; replace it with an NLP model or API if needed.
- Token authentication is used. After login/signup, the frontend should include the header:
  `Authorization: Token <token>` for endpoints that require user identification.
- CORS is enabled for all origins to simplify local development. Tighten this for production.

Enjoy! 👩‍💻👨‍💻
>>>>>>> 03776e1 (Initial commit - Legal AI project)
