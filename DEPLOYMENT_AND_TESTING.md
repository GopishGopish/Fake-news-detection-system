# Deployment Guide

To deploy this application to a production server (like Heroku, AWS, or DigitalOcean), follow these best practices.

## 1. Production Web Server
Do NOT use the built-in Flask development server in production. Instead, use a WSGI server like **Gunicorn**.
```bash
pip install gunicorn
```

## 2. Environment Variables
Update your `app.py` or use a `.env` file to manage secrets:
- `SECRET_KEY`: Generate a long random string.
- `DATABASE_URI`: Point to a production database (e.g., PostgreSQL).

## 3. Deployment Steps (Example: Heroku)
1. **Procfile**: Create a file named `Procfile` with:
   `web: gunicorn app:app`
2. **Commit changes**: `git add . && git commit -m "Ready for deployment"`
3. **Push to Heroku**: `git push heroku main`

## 4. Static Files
In production, you should serve static files (CSS/JS) through a dedicated service or a web server like Nginx, or use WhiteNoise for Flask.

---

# Testing Instructions

## 1. Unit Testing (ML)
- Run `train_model.py` and verify that `accuracy_score` is above 0.85.
- Check the `model.pkl` and `vectorizer.pkl` exist after training.

## 2. Manual UI Testing
1. **Registration**: Register a new user at `/register` and verify redirection to login.
2. **Login**: Log in with credentials and verify access to `/predict`.
3. **Prediction**: 
   - Paste a real news headline (e.g., "NASA finds water on moon").
   - Paste a fake news headline (e.g., "Aliens steal the Eiffel Tower").
   - Verify the results and confidence scores.
4. **History**: Check if your predictions appear in the `/history` table.
5. **Admin Access**: Log in as 'admin' and verify the `/dashboard` displays valid stats and charts.

## 3. Input Validation
- Try submitting an empty news text (should trigger an alert).
- Try registering with an existing email (should trigger an error).
