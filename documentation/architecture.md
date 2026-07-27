# Architecture

Shield is a split full-stack application with a single user-facing interface.

```text
Browser
  |
  v
Next.js 16 App Router + React 19 + Motion
  |  /backend/* rewrite
  v
Python 3.14 + Flask JSON API
  |
  +--> SQL database
  +--> M-Pesa
  +--> mail and operational integrations
```

Next.js owns every rendered customer and staff screen: discovery, product detail, cart, checkout, authentication, account history, care, and the operations dashboard. There are no Flask/Jinja page templates.

Flask remains the operational authority. It authenticates users, enforces roles and order transitions, recalculates pricing, controls stock, records CRM/audit activity, and communicates with payment providers. Browser totals and interface state are never authoritative.

Motion is used through `motion/react` for page transitions, tab state, dashboard entrances, authentication surfaces, and reduced-motion-aware interaction. Server components remain the default; client components are limited to stateful or animated boundaries.
