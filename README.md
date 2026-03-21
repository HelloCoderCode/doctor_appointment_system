

#  1. Clone Repository

```bash
git clone https://github.com/SoftwareTechnology-Hub/doctors_appointments_systems.git
cd doctors_appointments_systems/django-doctor-appointment
```

---

#  2. Create Virtual Environment

```bash
python -m venv env
```

### Activate (Windows PowerShell):

```bash
env\Scripts\activate
```

---

#  3. Install Requirements

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

If not:

```bash
pip install django pillow
```

---

#  4. Basic Django Setup

Go inside project:

```bash
cd doctor_appointment_system
```

Then back if needed:

```bash
cd ..
```

---

#  5. Migrations (IMPORTANT)

```bash
python manage.py makemigrations
python manage.py migrate
```

---

#  6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Enter:

* Username
* Email
* Password

---

#  7. Run Server

```bash
python manage.py runserver
```

Open browser:

 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

#  8. Add SMTP Email (IMPORTANT)

Open:

```bash
doctor_appointment_system/settings.py
```

Add this at bottom 

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

---

##  Gmail App Password (VERY IMPORTANT)

 Don’t use normal password
 Use **App Password**

Steps:

1. Go to Google Account
2. Security → 2-Step Verification ON
3. Search “App Password”
4. Generate password
5. Use that in `EMAIL_HOST_PASSWORD`

---


# 9. .gitignore (IMPORTANT)

```bash
env/
__pycache__/
*.pyc
db.sqlite3
media/
```

---

#  10. Common Fixes

###  Error: no module named django

```bash
pip install django
```

---

###  Migrations issue

```bash
python manage.py migrate --run-syncdb
```

---

###  Port already in use

```bash
python manage.py runserver 8001
```

---

# Final Flow (Short)

```bash
git clone <repo>
cd project
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


