# Study Assistant Telegram Bot

Telegram bot for study help powered by Gemini + Groq fallback.

## Features

- Text Q&A
- Image understanding (homework photos, textbook pages)
- Basic user profile/settings
- AI provider routing (Gemini first, Groq fallback)
- Dialogue history in database

## Tech Stack

- Python 3.12
- aiogram 3
- SQLAlchemy (async)
- Alembic
- SQLite (default) or PostgreSQL (Railway)

## Local Run

1. Create `.env` from template:

```bash
cp .env.example .env
```

2. Fill required variables in `.env`.
3. Install dependencies and run:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Docker Run

```bash
docker compose up --build -d
```

## GitHub Preparation Checklist

1. Make sure `.env` is not committed (already ignored in `.gitignore`).
2. Use only placeholder values in `.env.example`.
3. Initialize git and first commit:

```bash
git init -b main
git add .
git commit -m "Initial commit"
```

4. Create an empty GitHub repository and push:

```bash
git remote add origin <your-repo-url>
git push -u origin main
```

## Deploy on Railway

This project is ready for Railway via `Dockerfile` + `railway.json`.

### Option A: Deploy from GitHub (recommended)

1. Push project to GitHub.
2. In Railway: `New Project` -> `Deploy from GitHub repo`.
3. Select this repository.
4. Add environment variables in Railway service settings.
5. Deploy.

### Option B: Deploy with Railway CLI

```bash
railway login
railway init
railway up
```

## Required Environment Variables

- `BOT_TOKEN`
- `GEMINI_API_KEY`
- `GROQ_API_KEY`

## Optional Environment Variables

- `DATABASE_URL` (default: `sqlite+aiosqlite:///./app.db`)
- `APP_ENV` (default: `development`)
- `LOG_LEVEL` (default: `INFO`)
- `MAX_CONTEXT_MESSAGES` (default: `12`)
- `MAX_IMAGE_SIZE_MB` (default: `10`)
- `DEFAULT_UI_LANGUAGE` (default: `ru`)

## Railway Database Notes

- If you add a Railway PostgreSQL service, set/attach `DATABASE_URL` from Railway.
- The app auto-normalizes `postgres://...` / `postgresql://...` to async SQLAlchemy format.

## Security Note

If any real API keys were ever exposed in git history or shared publicly, rotate them immediately:

- Telegram bot token in BotFather
- Gemini API key
- Groq API key
