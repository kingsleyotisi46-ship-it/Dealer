# Coach JV Tech — Django website

Responsive white-and-blue Django starter with public pages, account registration/login, member dashboard, stock requests, funding requests, withdrawals, recovery case tracking and protected Django admin.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `/` and `/admin/`. Configure `DepositOption` and `PaymentWallet` records in the admin before testing deposits.

## Deploy with Neon PostgreSQL

This repository's `render.yaml` configures only a Render web service; it does **not** create a Render database. Create a PostgreSQL project in Neon, copy its pooled connection string, then import this repository in Render using **New → Blueprint**. When prompted, set the `DATABASE_URL` environment variable to your Neon connection string. Keep it private and never commit it to GitHub. Configure `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and production email settings, then run migrations and create a Django superuser through the service shell.

## Before real use

- Configure production email delivery, support contact details, backups and persistent private file storage.
- Verify actual received payment and set the exact `confirmed_amount` before confirming a deposit in admin.
- Add a safe audited refund workflow for rejected withdrawals before handling real funds.
- Stock requests are internal request records only; there is no brokerage connection, trade execution or live market valuation.
- Recovery outcomes cannot be guaranteed. Publish and review all fees and legal terms before charging users.
- Add security review, audit trails, file scanning, rate limiting and tests before production use.
