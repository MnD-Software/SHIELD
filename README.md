# Shield Pharmacy

Shield Pharmacy is a production-oriented pharmacy commerce platform for Kenya. It uses a Next.js 16 App Router interface, Motion for React interactions, a Python 3.14 Flask JSON API, and a MySQL-compatible data layer.

## Delivery status

- [x] Phase 1 — folder structure and architecture
- [x] Phase 2 — normalized database schema and seed catalogue
- [x] Phase 3 — backend APIs
- [x] Phase 4 — authentication and account security
- [x] Phase 5 — customer storefront
- [x] Phase 6 — admin dashboard
- [x] Phase 7 — shopping cart
- [x] Phase 8 — checkout and payment architecture
- [x] Phase 9 — deployment configuration
- [x] Phase 10 — testing and optimization baseline

All proposal Phase I features have an executable baseline, including catalogue discovery, accounts, cart/checkout, editable administration, inventory, contact enquiries, Google Maps, WhatsApp, COD, and the M-Pesa STK/callback workflow. Live M-Pesa collection remains safely disabled until merchant credentials and a public callback URL are configured. Prescription workflows and the proposal's Phase II enhancements remain intentionally out of scope.

## Repository map

```text
SHIELD/
├── backend/          Flask application and API modules
├── database/         Schema documentation, migrations, and seed strategy
├── documentation/    Architecture and engineering decisions
├── frontend/         Next.js customer, account, checkout and admin application
├── static/uploads/   Backend-served catalogue uploads only
├── tests/            Cross-application and end-to-end tests
└── uploads/          Local development uploads only
```

## Architecture

Read [documentation/architecture.md](documentation/architecture.md) before adding features. Engineering conventions and phase acceptance criteria are in [documentation/development.md](documentation/development.md).

## Local prerequisites

- Python 3.14.6
- Node.js 20+
- MySQL 8+

## Run locally

```powershell
python -m pip install -r requirements.txt
python run.py
```

In another terminal, start the React storefront:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open `http://127.0.0.1:3000` for every user-facing surface, including `/login`, `/account`, and `/admin`. Flask on `http://127.0.0.1:5000` is API-only; its former browser routes redirect to Next.js for compatibility. Local development uses SQLite automatically; production uses the MySQL `DATABASE_URL`.

The seeded local administrator is `admin@shield.test` with password `ShieldAdmin123!`. Replace it before deployment. See [documentation/admin-guide.md](documentation/admin-guide.md) for handover and training.
