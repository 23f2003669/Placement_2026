# Placement Portal Application V2

Placement Portal Application V2 is a multi-user web application developed for the Modern Application Development II project.

The system provides role-based functionality for Admin, Company, and Student users to manage campus placement activities.

## Tech Stack

- Flask - REST API backend
- Vue.js 3 - Frontend
- Vite - Frontend build tool
- Bootstrap - UI styling
- SQLite - Database
- Redis - Caching
- Celery - Scheduled and asynchronous jobs
- Chart.js - Dashboard charts

## Project Structure

- `backend/` - Flask API, database models, routes, caching, and Celery jobs
- `frontend/` - Vue.js user interface
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Frontend dependencies

## Backend Setup

Open a terminal and move to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Create the environment configuration file:

```bash
cp .env.example .env
```

Update the required environment variables in `.env`:

```text
SECRET_KEY            - any random string, used to sign JWTs
ADMIN_EMAIL            - email for the pre-created admin account
ADMIN_PASSWORD          - password for the pre-created admin account
REDIS_URL              - Redis connection string for caching
CELERY_BROKER_URL        - Redis connection string for the Celery broker
CELERY_RESULT_BACKEND      - Redis connection string for Celery results
MAIL_SERVER, MAIL_PORT      - SMTP server details (default: Gmail SMTP)
MAIL_USERNAME, MAIL_PASSWORD   - sender email + app password (see comment in .env.example)
MAIL_DEFAULT_SENDER        - "From" address for outgoing mail
```

Email variables power the daily reminders, monthly report, and interview-scheduled notifications. If left unset, those Celery tasks run and log a skipped-send message instead of failing.

Start the Flask application:

```bash
python3 app.py
```

The backend runs on `http://127.0.0.1:5000` by default. The frontend
(`frontend/src/services/api.js`) is hardcoded to this address — if you change
the Flask port, update it there too.


## Frontend Setup

Open another terminal and move to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the Vue development server:

```bash
npm run dev
```

## Redis

Redis is used for application caching and Celery.

Start the Redis server:

```bash
redis-server
```

## Celery

Celery is used for scheduled and asynchronous background jobs. Redis must be
running first (see above). Open two more terminals from the `backend/`
directory (with the venv activated):

Start the Celery worker (runs the background jobs):

```bash
cd ~/Placement_2026/backend
source venv/bin/activate
celery -A celery_config.celery_app worker --loglevel=info
```

Start Celery beat (triggers the scheduled jobs — daily reminders at 9 AM UTC,
monthly report on the 1st at 8 AM UTC):

```bash
cd ~/Placement_2026/backend
source venv/bin/activate
celery -A celery_config.celery_app beat --loglevel=info
```

The CSV export job doesn't need beat — it's triggered on-demand from the
student dashboard and only needs the worker running.

The application implements:

- Daily application deadline reminders
- Monthly placement activity reports
- Asynchronous CSV export of student application history

## Default Admin

The admin user is created programmatically during database initialization.

Admin credentials are configured using the following environment variables:

```text
ADMIN_EMAIL
ADMIN_PASSWORD
```

## Main Features

### Admin

- View placement statistics
- Approve or reject company registrations
- Approve or reject placement drives
- Manage students and companies
- View student applications
- Search students and companies
- Blacklist or deactivate users

### Company

- Register company profile
- Create placement drives after admin approval
- View applicants
- Shortlist students
- Update application status
- Schedule interviews
- Update final selection results

### Student

- Register and login
- Update profile
- Upload resume
- View approved placement drives
- Search and filter placement drives
- Apply to eligible placement drives
- View application status
- View placement history
- Export application history as CSV

## Background Jobs

The application implements the following background jobs:

- Daily reminders for upcoming placement drive deadlines
- Monthly placement activity reports
- User-triggered asynchronous CSV export

## Additional Feature

The application includes offer letter generation for selected students.

## Database

SQLite is used as the application database.

Database tables are created programmatically using SQLAlchemy.

The default admin user is also created programmatically during database initialization.