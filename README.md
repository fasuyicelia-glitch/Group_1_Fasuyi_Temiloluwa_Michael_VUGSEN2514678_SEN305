# Service Request Management System (SEN305)

An original Django starter project for managing service requests. It includes:
- Service requests with categories, priorities and statuses
- Due dates and overdue filtering
- Resolution summaries and validation for resolved/closed requests
- Django Admin configuration
- Automated tests and a sample-data command

## Setup

Python 3.10+ is recommended.

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ and sign in.

## Sample records

```bash
python manage.py seed_requests
```

This creates 12 sample requests across two categories and three statuses.

## Tests

```bash
python manage.py test
```

## Database

SQLite is configured by default so the project can run immediately. To use MySQL,
update `DATABASES` in `config/settings.py` and install `mysqlclient` for your system.
Do not commit database passwords or secret keys.
