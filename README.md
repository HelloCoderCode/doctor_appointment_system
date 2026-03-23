# Doctor Appointment System
A Django project for managing doctor availability, patient bookings, and token‑based queues.

**What This Project Does**
1. Doctors create appointment availability with start/end time and average minutes per patient.
2. Patients book by date and receive a token number and estimated time.
3. Email confirmations are sent to patients.
4. Doctors manage patient lists and booking statuses.
5. Patient and doctor flows are separated with role‑based access.

---

## Quick Start

### 1. Clone Repository
```bash

git clone https://github.com/HelloCoderCode/doctor_appointment_system.git
cd doctors_appointments_system/django-doctor-appointment
```

### 2. Create Virtual Environment
```bash
python -m venv env
```

Activate (Windows PowerShell):
```bash
env\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

If issue:
```bash
pip install django pillow
```

### 4. Basic Django Setup
Go inside project:
```bash
cd doctor_appointment_system
```

Then back if needed:
```bash
cd ..
```

### 5. Migrations (IMPORTANT)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

Enter:
1. Username
2. Email
3. Password

### 7. Run Server
```bash
python manage.py runserver
```

Open browser:
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

---

## Core Features

### Doctor
1. Create appointment availability with time and department.
2. Set average minutes per patient for queue estimation.
3. Manage appointments, patient list, and booking statuses.

### Patient
1. Book by date, receive token number and estimated start time.
2. View booking confirmation and download PDF.
3. View appointment history.

### Booking Flow
1. Patient opens doctor booking URL.
2. Form preselects the doctor.
3. Booking is created with token number.
4. Estimated time calculated based on queue.
5. Confirmation email sent.

---

## Email Setup

### 8. Add SMTP Email (IMPORTANT)
Open:
```
doctor_appointment_system/settings.py
```

Add at bottom:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### Gmail App Password (VERY IMPORTANT)
Don’t use normal password. Use **App Password**.

Steps:
1. Go to Google Account
2. Security → 2‑Step Verification ON
3. Search “App Password”
4. Generate password
5. Use that in `EMAIL_HOST_PASSWORD`

---

## Environment Notes

### Default Database
SQLite is used by default:
```
db.sqlite3
```

### Media
Uploads stored in:
```
media/
```

---

## Common Troubleshooting

### Migrations Failing
```bash
python manage.py migrate --run-syncdb
```

### Port in Use
```bash
python manage.py runserver 8001
```

---

## Project Structure
```
django-doctor-appointment/
  accounts/
  appointment/
  doctor_appointment_system/
  templates/
  static/
  media/
```

---

## Documentation
Full technical details are in:
```
TECHNICAL_DOCS.md
```
