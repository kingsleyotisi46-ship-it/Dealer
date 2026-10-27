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

## Deploy

This repository includes a Render Blueprint (`render.yaml`). In Render, choose **New → Blueprint**, connect this repository, and apply the blueprint to create the web service and database. Then create a Django superuser using the Render service shell. A repository upload alone is not a live deployment.

## Before real use

- Configure production email delivery, support contact details, backups and persistent private file storage.
- Verify actual received payment and set the exact `confirmed_amount` before confirming a deposit in admin.
- Add a safe audited refund workflow for rejected withdrawals before handling real funds.
- Stock requests are internal request records only; there is no brokerage connection, trade execution or live market valuation.
- Recovery outcomes cannot be guaranteed. Publish and review all fees and legal terms before charging users.
- Add security review, audit trails, file scanning, rate limiting and tests before production use.
