<<<<<<< HEAD

# Fruits Shop - Simple E-commerce Demo

This is a small e-commerce demo (fruits shop) with:

- Django backend with products + cart API endpoints
- Static frontend (HTML/JS/CSS) to add/remove items from a cart (bucket) and preview before confirm

Local development (MySQL)

This repository is configured to run with MySQL for local development. We still support a zero‑setup SQLite mode, but the primary instructions below assume you will run the project with a local MySQL server.

1. Create a virtual environment and install requirements:

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

2. Prepare MySQL and credentials (choose one):

- Option A — manual SQL (recommended if you prefer SQL commands):

```sql
CREATE DATABASE ecom_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecom_user'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON ecom_db.* TO 'ecom_user'@'localhost';
FLUSH PRIVILEGES;
```

- Option B — use the included helper script to create the database and user (runs with your MySQL root credentials):

```powershell
# from project root
#.venv\Scripts\Activate
python scripts/create_mysql_setup.py --host 127.0.0.1 --port 3306 --root-user root --root-password <root-password>
```

3. Configure environment variables for Django to use MySQL.

Copy the example and update values (do not commit real secrets):

```powershell
copy .env.example .env
# edit .env and fill MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT
```

On Windows PowerShell, load the variables into the current session (we provide `set_mysql_env.ps1`):

```powershell
. .\set_mysql_env.ps1
```

The loader sets `MYSQL_DB`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, and `USE_PYMYSQL` so `ecom_site/settings.py` will use MySQL instead of SQLite.

4. Run migrations, seed data, and start the dev server:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

Notes:

- If you use `PyMySQL` (easy on Windows) ensure `PyMySQL` is installed in your venv. Some MySQL auth methods require `cryptography` — the `requirements.txt` includes these where needed.
- The project also ships `scripts/create_mysql_setup.py` and `set_mysql_env.ps1` to automate local DB/user setup and env loading.

Quick helper to run with MySQL using a `.env` file (Windows PowerShell)

1. Copy the example file and edit credentials:

```powershell
copy .env.example .env
# edit .env in Notepad or another editor and fill values
```

2. Load the `.env` into your current PowerShell session (dot-source the loader so variables persist):

```powershell
. .\set_mysql_env.ps1
```

3. Run migrations, seed, and start the server:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```

This script sets `MYSQL_DB`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, and `USE_PYMYSQL` in your session so `ecom_site/settings.py` will use MySQL instead of SQLite.

Note: you provided `dbms123` as the MySQL password. If you add it to your `.env` file it will look like this:

```text
MYSQL_DB=ecom_db
MYSQL_USER=ecom_user
MYSQL_PASSWORD=dbms123
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
USE_PYMYSQL=1
```

Warning: do not commit a `.env` file with real credentials to version control. Keep `.env` local and secure.

Switching to MySQL (optional)

If you prefer to use MySQL instead of the default SQLite, update your environment and `ecom_site/settings.py` accordingly. Basic steps:

1. Install MySQL Server and create a database and user:

```sql
CREATE DATABASE ecom_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecom_user'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON ecom_db.* TO 'ecom_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Install a Python MySQL driver in your venv. Recommended: `mysqlclient` (native) or `PyMySQL` (pure Python).

Windows (mysqlclient may require build tools/wheel):

```powershell
pip install mysqlclient
# If installation is difficult on Windows, install PyMySQL instead:
pip install PyMySQL
```

3. Configure `ecom_site/settings.py` database section. Example (mysqlclient):

```python
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'ecom_db',
		'USER': 'ecom_user',
		'PASSWORD': 'your-password',
		'HOST': '127.0.0.1',
		'PORT': '3306',
		'OPTIONS': {
			'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
		},
	}
}
```

If you used `PyMySQL`, add the following to `ecom_site/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

4. Run migrations against MySQL and seed data:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py seed_products
```

5. Start the server:

```powershell
python manage.py runserver
```

Endpoints:

- `GET /api/products` - list products
- `GET /api/cart` - current cart
- `POST /api/cart/add` - add item to cart
- `POST /api/cart/remove` - remove item from cart
- `POST /api/cart/checkout` - confirm (clears cart)

Files:

- `manage.py` - Django manage command
- `ecom_site/` - Django project settings and URLs
- `shop/` - Django app with models and API views
- `templates/index.html` - frontend template (Bootstrap UI)
- # `static/` - frontend static files (`styles.css`, `main.js`)

# ecom-site

> > > > > > > f99579f32c6b4e5f4bb091b4b6b8a56106de79a1

## Render / Aiven deployment notes

If you deploy this project to Render and connect to an Aiven (or other managed) MySQL instance, follow these steps:

- Ensure `requirements.txt` includes `PyMySQL` and `dj-database-url` (done).
- Provide either `DATABASE_URL` (standard) or `MYSQL_*` env vars (`MYSQL_DB`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`).
- If Aiven requires SSL, add the CA certificate as an environment variable named `MYSQL_SSL_CA_BASE64` (base64 of the PEM file). The app will write this to a temp file and pass it to the DB driver.
- To fail fast during start, add this check to your Render Start Command before launching Gunicorn / the app process:

```bash
python manage.py check_db || exit 1
# then start your server, e.g.:
gunicorn ecom_site.wsgi:application --bind 0.0.0.0:$PORT
```

Watch build logs to confirm `pip install -r requirements.txt` completed and that `PyMySQL` and `dj-database-url` were installed. If a package fails to build on Windows during local testing, try running in WSL or check Render logs (Render builds on Linux and usually installs prebuilt wheels).
