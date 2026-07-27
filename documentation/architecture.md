# System architecture

## Goals

Shield Pharmacy must deliver a fast, accessible commerce experience while protecting health-adjacent customer data and allowing business capabilities to evolve independently. The architecture uses a modular monolith initially: it has clear domain seams without the deployment and consistency cost of premature microservices.

## Runtime topology

```text
Browser / PWA
    |
    | HTTPS, JSON API, secure session or short-lived JWT
    v
Vercel static frontend  ----->  Render Flask API
                                      |
                         +------------+------------+
                         |            |            |
                      MySQL 8      Mail provider   M-Pesa
                         |
                 encrypted backups
```

The browser never connects directly to MySQL or payment providers. The Flask service owns validation, authorization, order pricing, inventory decisions, and payment initiation. Client totals are display-only and are recalculated on the server.

## Backend boundaries

- **Auth** owns credentials, sessions, verification, password recovery, and rate limits.
- **Catalog** owns products, brands, categories, media metadata, search, and merchandising.
- **Customers** owns profiles, addresses, wishlists, and consent preferences.
- **Orders** owns carts after checkout submission, order state, order items, and fulfillment history.
- **Inventory** owns stock ledgers, reservations, availability, and low-stock reporting.
- **Coupons** owns promotion rules, eligibility, redemption limits, and audit records.
- **Payments** exposes a provider-neutral interface; M-Pesa is the first adapter.
- **Content** owns testimonials, health articles, contact messages, and site settings.
- **Admin** composes authorized operational views but does not duplicate domain logic.

Cross-module work goes through explicit service interfaces. SQLAlchemy models may share one transaction when consistency requires it, while module services remain the only business entry points.

## Frontend architecture

Pages are server-addressable HTML entry points for resilient navigation and SEO. Reusable components provide consistent navigation, product cards, forms, feedback, and dialogs. Feature modules own cart, search, account, and checkout state. Alpine is limited to declarative component state; complex workflows use testable ES modules.

Design tokens expose the approved palette, spacing, typography, radii, shadows, and motion. Dark-mode tokens are designed in Phase 5 but remain disabled until every page meets contrast requirements.

## Security baseline

- HttpOnly, Secure, SameSite cookies for browser sessions
- CSRF tokens on every state-changing cookie-authenticated request
- Argon2id or Werkzeug's current strong password hash with upgrade-on-login
- strict request schemas, output serialization, and upload allowlists
- per-IP and per-account throttles on authentication and contact endpoints
- least-privilege database credentials and environment-managed secrets
- immutable audit events for admin, inventory, order, coupon, and payment changes
- CSP, HSTS, Referrer-Policy, Permissions-Policy, and frame protections
- no prescription or sensitive upload stored on local ephemeral disks

## Data and transaction principles

Money is stored as integer minor units or fixed-precision decimal values, never floating point. Order items snapshot product names, SKUs, prices, and tax facts so historical orders do not change with catalog edits. Inventory uses an append-only movement ledger plus a current balance for reliable reconciliation. Every payment callback is authenticated and idempotent.

## Performance and accessibility budgets

- mobile LCP at or below 2.5 seconds at the 75th percentile
- CLS at or below 0.1 and INP at or below 200 ms
- initial route JavaScript kept below 100 KB gzip where practical
- responsive AVIF/WebP images with explicit dimensions and lazy loading below the fold
- keyboard-complete operation, visible focus, semantic landmarks, and WCAG 2.2 AA contrast
- reduced-motion behavior for every non-essential animation

## Future enhancement seams

The following are intentionally disabled: AI recommendations, prescription workflows, loyalty, refill reminders, delivery tracking, courier/ERP/accounting integrations, Google Merchant Center, advanced analytics, supplier management, reviews, native mobile apps, and an AI chatbot. They will integrate through versioned service interfaces and domain events; no inactive UI controls or speculative database columns are added now.

