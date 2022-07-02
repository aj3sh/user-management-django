# Django User Management
Django User Management project provides api for managing users and profiles.

## Installation

### Minimum Requirements
- Python ≥ 3.8
- Pip (Python ≥ 3.8)

### Installation Steps
- Activate python virtualenv
- Install project requirements. `pip install -r requirements.txt`
- If any extra configuration is need then update or create `user_management/.env` file.
- Migrate database. `python manage.py migrate`

### Creating Superuser

```bash
python manage.py createsuperuser
```

## Running the project
```bash
python manage.py runserver
```