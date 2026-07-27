# Backend

The backend is a Flask application built around an application factory. Domain modules live under `app/modules`, infrastructure adapters under `app/integrations`, and shared cross-cutting services under `app/core`.

Planned module boundaries are `auth`, `catalog`, `customers`, `orders`, `inventory`, `coupons`, `content`, `payments`, and `admin`. Modules own their routes, services, validation schemas, and authorization policies; they do not reach into another module's persistence implementation directly.

