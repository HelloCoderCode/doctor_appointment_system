# Technical Documentation

## Architecture Overview

### Apps
1. `accounts`  
   Handles authentication, roles, and user profiles.
2. `appointment`  
   Core booking logic, doctor availability, tokens, and confirmations.

### Roles
1. Doctor  
   Can create appointment availability and manage bookings.
2. Patient  
   Can book appointments and view history.

---

## Data Model (Key Fields)

### `Appointment`
Represents a doctor’s availability.
1. `uuid` (UUID)  
   Public identifier used in booking URLs.
2. `full_name` (string)  
   Doctor’s name.
3. `department` (string)  
   Doctor specialty.
4. `start_time` (TimeField)  
   Daily availability start.
5. `end_time` (TimeField)  
   Daily availability end.
6. `avg_minutes_per_patient` (int)  
   Estimated minutes per patient.
7. `slug` (slug)  
   Auto‑generated from name.

### `TakeAppointment`
Represents a patient booking.
1. `booking_id` (string)  
   Public identifier in confirmation URLs.
2. `appointment_date` (date)  
   Booking date.
3. `token_number` (int)  
   Queue position.
4. `estimated_start_time` (datetime)  
   ETA based on queue.
5. `email`, `phone_number`, `full_name`

---

## Booking Flow

1. Patient opens booking URL using doctor UUID.  
   Example: `/patient-take-appointment/<uuid>`
2. Doctor is preselected on booking form.
3. Patient selects appointment date (default = next day).
4. System calculates capacity:
   ```
   capacity = (end_time - start_time) / avg_minutes_per_patient
   ```
5. If capacity is full, booking is rejected.
6. Token is assigned and ETA calculated.
7. Confirmation email sent.

---

## Token Logic

Estimated time:
```
estimated_start = start_time + (token_number - 1) * avg_minutes_per_patient
```

Token assignment:
1. Find last token for doctor + date.
2. New token = last + 1.

---

## Views (Key)

### Booking
1. `TakeAppointmentView`  
   Saves booking, assigns token, sends email.

### Confirmation
1. `TakeAppointmentConfirmView`  
   Uses `booking_id` in URL.

### PDF
1. `TakeAppointmentPdfView`  
   Generates a simple PDF confirmation.

---

## Templates

### Booking Confirmation Email
1. `templates/appointment/emails/booking_confirmation.html`
2. `templates/appointment/emails/booking_confirmation.txt`

---

## URLs

### Booking
```
/patient-take-appointment/<doctor-uuid>
```

### Confirmation
```
/patient-take-appointment/confirm/<booking-id>
```

---

## Email Delivery

Uses `EmailMultiAlternatives`:
1. HTML body
2. Plain‑text fallback

---

## Security Notes

1. Booking confirmation URLs use `booking_id` to avoid guessing sequential IDs.
2. Doctor booking URLs use UUID.
3. All patient/doctor actions require authentication and role checks.

---

## Known Warnings

Django warns about default auto fields:
```
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
You can add this in `settings.py` if desired.

---

## Future Improvements

1. Add doctor notification emails.
2. Replace SQLite with Postgres for production.
3. Add analytics on average wait times.

