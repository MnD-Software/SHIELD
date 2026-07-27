# Shield Pharmacy administrator guide

## Sign in

Open `/login`, sign in with the administrator account, and choose **Admin dashboard** from the account page. Replace the seeded development password before launch.

## Catalogue and inventory

- Choose **Add product** to enter its SKU, category, price, stock, content, image, and featured status.
- Use **Edit** on a product row to update any catalogue or stock field.
- Create product categories from the category form.
- Deleting an item with order history safely archives it at zero stock; an unused item is removed.

## Orders and customers

- Change an order through Pending, Processing, Ready, Dispatched, Completed, or Cancelled from the Orders table.
- Review registered customer contact information in the Customers table.
- Contact messages appear under Customer enquiries and can be marked resolved.

## Payments

Cash on delivery works without external configuration. For M-Pesa, copy `.env.example`, set `MPESA_ENABLED=true`, supply Safaricom Daraja credentials, and use the public HTTPS callback URL `/api/v1/payments/mpesa/callback`. Complete a sandbox transaction before switching `MPESA_ENVIRONMENT` to `production`.

## Launch checklist

- Replace the example administrator password and all secrets.
- Confirm the pharmacy contact details and replace the provisional Nairobi map pin with the branch address.
- Upload the client-approved logo, product catalogue, pricing, and images.
- Enable HTTPS and `SESSION_COOKIE_SECURE=true`.
- Verify M-Pesa sandbox callbacks, COD operations, email delivery, backups, and the contact inbox.
- Run `python -m pytest -q` and `npm.cmd run build` before deployment.
