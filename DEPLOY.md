# Deploy HealthHub for free

Stack: **Vercel** (Vue frontend) + **Render** (Flask API, Postgres, Celery) + **Upstash** (Redis) + **Gmail App Password** (email).

Estimated cost: **$0/month** on free tiers (Render web/workers may sleep when idle).

---

## 1. Push this repo to GitHub

Repo: [24f1001022/HealthHub](https://github.com/24f1001022/HealthHub)

```bash
git add .
git commit -m "Add production deployment configuration"
git push origin main
```

**Security:** If `backend/.env` was ever committed, rotate your Gmail App Password and remove `.env` from Git history (`git rm --cached backend/.env`).

---

## 2. Redis (Upstash — free)

1. Sign up at [upstash.com](https://upstash.com)
2. Create a **Redis** database (region near you)
3. Copy the **Redis URL** (`rediss://...` or `redis://...`)

You will paste this as `REDIS_URL` on all Render services.

---

## 3. Backend on Render

1. Go to [render.com](https://render.com) → **New** → **Blueprint**
2. Connect GitHub repo `24f1001022/HealthHub`
3. Render reads `render.yaml` and creates:
   - `healthhub-api` (web)
   - `healthhub-celery-worker`
   - `healthhub-celery-beat`
   - `healthhub-db` (Postgres)

4. When prompted, set these **manual** env vars on **all three** Python services:

| Variable | Example |
|----------|---------|
| `REDIS_URL` | `rediss://default:xxx@xxx.upstash.io:6379` |
| `PUBLIC_BASE_URL` | `https://healthhub-api.onrender.com` (your web service URL) |
| `FRONTEND_URL` | `https://your-app.vercel.app` (after step 4) |
| `MAIL_USERNAME` | your Gmail address |
| `MAIL_PASSWORD` | 16-char [Gmail App Password](https://myaccount.google.com/apppasswords) |

5. Deploy and wait until **healthhub-api** is live. Open `https://YOUR-API.onrender.com/api/departments` — you should get `[]` or JSON.

**Gmail:** Turn on 2-Step Verification, then create an App Password. Use that as `MAIL_PASSWORD` (not your normal Gmail password).

**Admin login (seeded on first start):** `admin@admin.com` / `admin`

---

## 4. Frontend on Vercel

1. [vercel.com](https://vercel.com) → **Add New Project** → import `HealthHub`
2. Set **Root Directory** to `backend/frontend`
3. Framework: **Vite** (auto-detected)
4. Environment variable:

| Name | Value |
|------|--------|
| `VITE_API_BASE_URL` | `https://YOUR-API.onrender.com/api` |

5. Deploy

6. Copy your Vercel URL (e.g. `https://health-hub-xxx.vercel.app`) and set **`FRONTEND_URL`** on Render `healthhub-api` to that exact URL (no trailing slash). Redeploy the API if needed.

---

## 5. Verify features

| Feature | How to test |
|---------|-------------|
| Login / signup | Register patient → login |
| Welcome email | Sign up with your email; check spam |
| Sessions | Login persists after refresh |
| CSV export | Patient → Treatment → Export CSV (needs worker + email) |
| Daily reminders | Celery beat (scheduled in `celery_app.py`) |
| Monthly doctor report | Celery beat on 1st of month |

**Celery worker** must be **Running** on Render for background email and exports. **Beat** runs scheduled reminders/reports.

---

## 6. Local development

```bash
# Terminal 1 — Redis (Docker) or local Redis
redis-server

# Terminal 2 — API
cd backend
cp .env.example .env   # edit values
pip install -r requirements.txt
python app.py

# Terminal 3 — Celery worker
cd backend
celery -A celery_app.celery worker --loglevel=info

# Terminal 4 — Frontend
cd backend/frontend
npm install
npm run dev
```

---

## Troubleshooting

- **Login fails after deploy:** `FRONTEND_URL` must match Vercel URL exactly; API must use `FLASK_ENV=production`.
- **Emails not sent:** Check `MAIL_*`, worker logs, and Gmail App Password.
- **Export stuck:** Ensure `REDIS_URL` is set on API and worker; worker service must be running.
- **Render cold start:** Free tier sleeps ~15s on first request after idle.
