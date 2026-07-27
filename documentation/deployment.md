# Deployment guide

## Render

Create a MySQL 8 database, set `DATABASE_URL`, and deploy the repository using `render.yaml`. Replace every generated or example secret. Set `SESSION_COOKIE_SECURE=true` in the production configuration before accepting customer traffic.

## Frontend topology

The current production build is server-rendered by Flask because authenticated forms, CSRF protection, and SEO routes share one deployable surface. A later independent Vercel frontend can consume `/api/v1` without changing domain services. Until that split, deploy the complete application to Render rather than publishing a disconnected static shell.

## Release checks

Run `pytest`, probe `/api/v1/health`, verify database backups, confirm HTTPS/security headers at the edge, and complete a sandbox M-Pesa callback test before enabling payment collection.

