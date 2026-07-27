# Frontend

The frontend is a server-rendered Next.js application using React, TypeScript and Tailwind CSS. Flask remains the source of truth for catalogue, stock, pricing and order creation.

Source boundaries:

- `app` — App Router pages, metadata, loading and error boundaries
- `components` — reusable discovery, catalogue, cart and purchase components
- `lib` — typed API client and domain contracts
- `public` — immutable public assets and PWA metadata
