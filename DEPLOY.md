# Deploy HealthHub for free

Stack: **Vercel** (frontend) + **Render free web** (API + Postgres) + optional **Upstash Redis** + **Gmail App Password**.

> **Render free tier does not support Celery background workers.** This project runs emails and CSV export **inside the web service** (`USE_CELERY=false`). Scheduled reminders use [cron-job.org](https://cron-job.org) (free).

---

## Fix a failed Blueprint sync

If you see `service type is not available for this plan` for Celery workers:

1. Pull latest `main` from GitHub (workers removed from `render.yaml`)
2. In Render → your Blueprint → **Manual sync** → **Clear build cache & deploy**

Or delete the Blueprint and create a new one from the repo.

---

## 1. Backend on Render

1. [render.com](https://render.com) → **New** → **Blueprint** → repo `24f1001022/HealthHub`
2. Blueprint creates **healthhub-api** (web) + **healthhub-db** (Postgres) only
3. Set env vars on **healthhub-api**:

| Variable | Required | Example |
|----------|----------|---------|
| `REDIS_URL` | Recommended | Upstash **Redis URL** (`rediss://...`) — **not** the REST `https://` URL |
| `PUBLIC_BASE_URL` | Yes | `https://healthhub-api.onrender.com` |
| `FRONTEND_URL` | Yes | Your Vercel URL (no trailing `/`) |
| `MAIL_USERNAME` | Yes | Gmail address |
| `MAIL_PASSWORD` | Yes | [Gmail App Password](https://myaccount.google.com/apppasswords) |
| `CRON_SECRET` | Auto | Copy from Render env (for scheduled emails) |

4. Test: `https://YOUR-API.onrender.com/health` → `{"status":"ok"}`

**Logs show `/api/departments` every 5 seconds?** That was Render’s health check (normal). New deploys use `/health` instead.

**Vercel env (required):** `VITE_API_BASE_URL` = `https://healthhub-api.onrender.com` (with or without `/api` — both work now)

**Upstash Redis URL (correct):** In [Upstash console](https://console.upstash.com) → your database → copy **Redis URL** (looks like `rediss://default:xxxxx@xxxxx.upstash.io:6379`). Paste as `REDIS_URL` on Render.

**Wrong:** `UPSTASH_REDIS_REST_URL` / `https://xxx.upstash.io` — that is HTTP REST, not for this app.

**Without valid `REDIS_URL`:** app still deploys using filesystem sessions.

**Admin:** `admin@admin.com` / `admin`

---

## 2. Frontend on Vercel

1. Import repo, **Root Directory:** `backend/frontend`
2. **Delete** `VITE_API_BASE_URL` from Vercel env (if set). Production uses `/api` proxy in `vercel.json` so **login cookies work**.
3. Deploy → set `FRONTEND_URL` on Render to `https://health-hub-gilt.vercel.app` (your real Vercel URL) → redeploy API

**Admin login:** `admin@admin.com` / `admin`

---

## 3. Scheduled emails (free cron)

On [cron-job.org](https://cron-job.org), create jobs that **POST** to your API:

| Job | URL | Schedule |
|-----|-----|----------|
| Daily reminders | `https://YOUR-API.onrender.com/api/cron/daily-reminders` | Daily 8:00 AM |
| Monthly reports | `https://YOUR-API.onrender.com/api/cron/monthly-reports` | 1st of month |

**Header:** `X-Cron-Secret: <your CRON_SECRET from Render>`

---

## 4. What works on free tier

| Feature | How |
|---------|-----|
| Login / signup | Web service |
| Welcome email | Sent immediately on signup |
| CSV export | Runs in web request (~few seconds) |
| Daily / monthly emails | cron-job.org hits `/api/cron/...` |

---

## Troubleshooting

- **Blueprint sync failed (workers):** Use latest `render.yaml` (no `type: worker` services).
- **API deploy failed:** Check Render logs; set `MAIL_*` and `DATABASE_URL` (auto from Postgres).
- **Login fails:** `FRONTEND_URL` must exactly match Vercel URL; `FLASK_ENV=production`.
- **Cold start:** First request after idle may take ~30s on Render free.
