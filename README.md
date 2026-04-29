# MediWay

MediWay is a Django-based medical store and pharmacy management application. It supports medicine browsing, cart checkout, prescription uploads, Razorpay payment flow, order tracking, admin medicine management, and invoice billing.

## Features

- User signup, login, logout, and profile updates
- Medicine catalog with search and fuzzy matching
- Cart management with quantity updates and item removal
- Prescription upload flow for medicines that require prescriptions
- Razorpay payment integration
- Customer order history and order detail pages
- Admin dashboard for adding, editing, deleting, and bulk uploading medicines
- Admin order management with status updates
- Billing module with customer details, bill items, invoice view, and PDF invoice download

## Tech Stack

- Python
- Django 4.2
- SQLite
- HTML templates
- Razorpay
- xhtml2pdf
- pandas
- fuzzywuzzy

## Project Structure

```text
MediWay/
|-- core/                 # Main Django app: models, views, urls, admin
|-- mediway/              # Django project settings and root URL config
|-- templates/            # HTML templates
|-- static/               # Static assets
|-- media/                # Uploaded media files, ignored by git
|-- manage.py             # Django management script
`-- db.sqlite3            # Local development database, ignored by git
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install django xhtml2pdf pandas fuzzywuzzy razorpay openpyxl python-Levenshtein
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Create an admin user:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Open the app:

```text
http://127.0.0.1:8000/
```

## Common Routes

- `/` - medicine catalog
- `/login/` - login
- `/signup/` - signup
- `/cart/` - shopping cart
- `/orders/` - user orders
- `/dashboard/` - admin medicine dashboard
- `/admin-orders/` - admin order management
- `/billing/` - billing and invoice workflow
- `/admin/` - Django admin

## Bulk Medicine Upload

Admins can upload medicines from CSV or Excel files through the dashboard. The file should include these columns:

```text
name, price, company, size, image
```

## Payment Configuration

Razorpay keys are currently configured in `mediway/settings.py` for development. For production, move secrets into environment variables, set `DEBUG = False`, configure `ALLOWED_HOSTS`, and use production-safe database and static file settings.

## Notes

- Uploaded prescriptions and media files are stored under `media/`.
- The local SQLite database is ignored by git.
- This project is configured for local development and should be hardened before deployment.
