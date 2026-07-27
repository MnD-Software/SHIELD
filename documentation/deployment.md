# Deployment

Shield is deployed as two coordinated services:

- `frontend/`: Next.js 16 on Vercel or a Node.js 20+ host.
- repository root: Python 3.14 Flask API on Render, container infrastructure, or another WSGI host.

Set `BACKEND_URL` for Next.js server-side API reads and `NEXT_PUBLIC_BACKEND_URL` only when a browser-visible backend origin is required. In the normal same-origin flow, browser requests use `/backend/*`, which Next.js rewrites to `BACKEND_URL` and preserves the authentication cookie.

Set `FRONTEND_URL` on Flask so compatibility routes return visitors to the Next.js application. Production also requires `DATABASE_URL`, a strong `SECRET_KEY`, secure cookies, allowed mail settings, and the M-Pesa variables documented in `.env.example`.

Build the UI with `npm.cmd run build`; serve it with `npm.cmd start`. Run the API with Gunicorn using the command in `render.yaml` or the root `Dockerfile`.
