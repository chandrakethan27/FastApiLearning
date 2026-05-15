# Lesson 10: Deployment — From Localhost to the Internet

## The Problem
Your app runs on http://127.0.0.1:8000 — only YOU can access it.
To let anyone use it, you need to deploy it to a server.

## Deployment Options

| Platform | Free Tier | Difficulty | Best For |
|----------|-----------|------------|----------|
| **Render** | Yes | Easy | Beginners, side projects |
| **Railway** | Yes (limited) | Easy | Quick prototypes |
| **Fly.io** | Yes (limited) | Medium | Production apps |
| **AWS/GCP/Azure** | Free tier | Hard | Enterprise, full control |
| **Docker + VPS** | $5/mo | Medium | Full control, any provider |

## What You Need for Deployment

### 1. requirements.txt — your dependencies
```
fastapi==0.111.0
uvicorn==0.29.0
sqlalchemy==2.0.30
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.0.1
httpx==0.28.1
```
Tells the server "install these packages."

### 2. Environment Variables — secrets out of code!
NEVER deploy with hardcoded secrets. Use environment variables:
```python
import os
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-for-dev-only")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
```

### 3. Procfile (for Render/Heroku) — how to start the app
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
- `--host 0.0.0.0` = accept connections from anywhere (not just localhost)
- `--port $PORT` = use the port the platform assigns

### 4. Dockerfile (for Docker/Fly.io) — portable container
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Production Checklist

### Security
- [ ] SECRET_KEY is from environment variable (not hardcoded)
- [ ] DATABASE_URL is from environment variable
- [ ] Debug mode is OFF
- [ ] CORS is configured (only allow your frontend domain)
- [ ] HTTPS is enabled (most platforms do this automatically)

### Performance
- [ ] Use PostgreSQL in production (not SQLite)
- [ ] Use multiple workers: `uvicorn ... --workers 4`
- [ ] Add database connection pooling
- [ ] Set up database migrations with Alembic

### Reliability
- [ ] Health check endpoint exists (GET / returns 200)
- [ ] Logging is configured
- [ ] Error monitoring (Sentry, etc.)
- [ ] Tests pass before deploying

## CORS — Cross-Origin Resource Sharing
When your frontend (React, etc.) is on a different domain than your API,
browsers block the requests by default. CORS fixes this:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # or ["*"] for dev
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Database Migrations with Alembic
SQLite is fine for learning. In production, use PostgreSQL + Alembic:
- Alembic tracks database schema changes (like git for your DB)
- `alembic revision --autogenerate -m "add email column"`
- `alembic upgrade head` — applies changes

## Deploy to Render (easiest free option)
1. Push your code to GitHub
2. Go to render.com → New Web Service
3. Connect your GitHub repo
4. Set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (SECRET_KEY, DATABASE_URL)
6. Deploy!

Your API is now live at https://your-app.onrender.com/docs
