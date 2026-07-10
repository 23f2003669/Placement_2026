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
python3 -m venv venv
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

Update the required environment variables in `.env`.

Start the Flask application:

```bash
python app.py
```

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

Celery is used for scheduled and asynchronous background jobs.

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