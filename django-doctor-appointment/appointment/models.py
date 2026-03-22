from django.db import models
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
import uuid

DEFAULT_DEPARTMENTS = (
    ('Dentistry', "Dentistry"),
    ('Cardiology', "Cardiology"),
    ('ENT Specialists', "ENT Specialists"),
    ('Astrology', 'Astrology'),
    ('Neuroanatomy', 'Neuroanatomy'),
    ('Blood Screening', 'Blood Screening'),
    ('Eye Care', 'Eye Care'),
    ('Physical Therapy', 'Physical Therapy'),
)

def _default_appt_date():
    return timezone.localdate()


def _default_appt_time():
    return timezone.localtime().time()


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=100)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    qualification_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    avg_minutes_per_patient = models.PositiveSmallIntegerField(default=15)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    # return reverse('appointment:delete-appointment', kwargs={'pk': self.pk})


class TakeAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=12, unique=True, editable=False, default="")
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='applied')
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    phone_number = models.CharField(max_length=120)
    appointment_date = models.DateField(default=_default_appt_date)
    appointment_time = models.TimeField(default=_default_appt_time)
    appointment_duration_minutes = models.PositiveSmallIntegerField(default=15)
    appointment_end_time = models.TimeField(default=_default_appt_time)
    token_number = models.PositiveIntegerField(default=0)
    estimated_start_time = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Short, human-friendly unique id
            self.booking_id = uuid.uuid4().hex[:12].upper()
        return super().save(*args, **kwargs)
