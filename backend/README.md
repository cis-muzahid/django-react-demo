# Django Application Setup

This guide will walk you through setting up and running your Django application with a PostgreSQL database.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python
- Django
- PostgreSQL
- pip (Python package installer)
- virtualenv

## Setting Up the Project

1. **Clone the repository:**

   ```sh
   git clone https://github.com/cis-muzahid/django-react-demo
   cd backend/django_demo
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

## Setting Up PostgreSQL

1. **Install PostgreSQL:**

   Follow the instructions for your operating system to install PostgreSQL.

2. **Create a database and user:**

   ```sh
   sudo -u postgres psql
   ```

   Inside the PostgreSQL prompt, run the following commands:

   ```sql
   CREATE DATABASE your_db_name;
   CREATE USER your_db_user WITH PASSWORD 'your_db_password';
   ALTER ROLE your_db_user SET client_encoding TO 'utf8';
   ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE your_db_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   \q
   ```

3. **Configure Django to use PostgreSQL:**

   Open `django_demo/settings.py` and update the `DATABASES` setting:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Applying Migrations and Creating a Superuser

1. **Creating new migrations:**

   ```sh
   python manage.py makemigrations
   ```

2. **Apply database migrations:**

   ```sh
   python manage.py migrate
   ```

3. **Create a superuser:**

   ```sh
   python manage.py createsuperuser
   ```

   Follow the prompts to create a superuser account.

## Running the Development Server

1. **Start the server:**

   ```sh
   python manage.py runserver
   ```

2. **Access the application:**

   Open your web browser and navigate to `http://127.0.0.1:8000/`.