# API reference

The public API is versioned under `/api/v1`.

## Health

`GET /api/v1/health` returns service readiness metadata.

## Products

`GET /api/v1/products` returns the active catalogue with stable identifiers, slugs, brands, effective prices, and current stock. Browser commerce actions currently use CSRF-protected form routes so sessions and progressive enhancement work without client-side JavaScript.

Future mobile and integration endpoints will use short-lived JWT access tokens, rotating refresh tokens, explicit scopes, and the same domain services as browser routes.

