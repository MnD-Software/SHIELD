# Deployment

Shield is deployed as two coordinated services:

- `frontend/`: Next.js 16 on Vercel or a Node.js 20+ host.
- repository root: Python 3.14 Flask API on Render, container infrastructure, or another WSGI host.

### Render

Choose **New → Blueprint**, connect `MnD-Software/SHIELD`, and use the root `render.yaml`. It provisions:

- `shield-pharmacy-api`, built from the Python 3.14 Dockerfile.
- `shield-pharmacy-db`, a managed PostgreSQL database.
- a generated `SECRET_KEY`, secure session cookies, and database wiring.

When prompted, set `FRONTEND_URL` to the final Vercel URL. Mail values can remain blank for the first deployment. M-Pesa remains disabled until merchant credentials and a public callback URL are configured.

### Vercel

Import the same GitHub repository and set **Root Directory** to `frontend`. Keep the detected Next.js framework and standard build settings. Add these Production, Preview, and Development variables as appropriate:

```text
BACKEND_URL=https://shield-pharmacy-api.onrender.com
NEXT_PUBLIC_SITE_URL=https://your-shield-project.vercel.app
```

Replace both example hostnames with the URLs actually assigned to the projects. `BACKEND_URL` is consumed by Next.js server rendering and the `/backend/*` rewrite. Browser requests remain same-origin, so session cookies work without client-side CORS configuration.

Set `FRONTEND_URL` on Flask so compatibility routes return visitors to the Next.js application. Production also requires the Blueprint-provided `DATABASE_URL` and `SECRET_KEY`; mail and M-Pesa settings are documented in `.env.example`.

Build the UI with `npm.cmd run build`; serve it with `npm.cmd start`. Run the API with Gunicorn using the command in `render.yaml` or the root `Dockerfile`.
