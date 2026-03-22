from collections import OrderedDict
from datetime import datetime, time, timedelta
from django import forms
from django.db import transaction
from django.utils import timezone
from .models import Appointment, TakeAppointment, DEFAULT_DEPARTMENTS


class CreateAppointmentForm(forms.ModelForm):
    department_other = forms.CharField(required=False)

    def _build_department_choices(self, current_value=None):
        defaults = [d[0] for d in DEFAULT_DEPARTMENTS]
        choices = [("", "Select Department")] + list(DEFAULT_DEPARTMENTS)

        extra_values = (
            Appointment.objects.exclude(department__isnull=True)
            .exclude(department__exact='')
            .values_list('department', flat=True)
            .distinct()
        )
        extras = sorted(
            {d.strip() for d in extra_values if d and d.strip() and d.strip() not in defaults},
            key=str.lower,
        )
        for value in extras:
            choices.append((value, value))

        if current_value and current_value not in defaults and current_value not in extras:
            choices.append((current_value, current_value))
        choices.append(("Other", "Other"))
        return choices

    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "Full Name"
        self.fields['image'].label = "Image"
        current_department = (self.instance.department or "").strip() if self.instance else ""
        department_choices = self._build_department_choices(current_department)
        self.fields['department'] = forms.ChoiceField(choices=department_choices, required=False)
        if current_department:
            self.fields['department'].initial = current_department
        self.fields['department'].label = "Department"
        self.fields['start_time'].label = "Start Time"
        self.fields['hospital_name'].label = "Hospital Name"
        self.fields['qualification_name'].label = "Qualification"
        self.fields['institute_name'].label = "Institute"
        self.fields['avg_minutes_per_patient'].label = "Average Minutes per Patient"
        self.fields['department_other'].label = "Custom Department (optional)"

        self.fields['full_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )

        self.fields['image'].help_text = "Recommended size: 800×600 px (max 2 MB)."

        self.fields['department'].widget.attrs.update(
            {
                'placeholder': 'Select Your Service',
            }
        )
        self.fields['department_other'].widget.attrs.update(
            {
                'placeholder': 'Type your department if not listed',
            }
        )

        if 'department' in self.fields and 'department_other' in self.fields:
            reordered = OrderedDict()
            for name, field in self.fields.items():
                if name == 'department_other':
                    continue
                reordered[name] = field
                if name == 'department':
                    reordered['department_other'] = self.fields['department_other']
            if 'department_other' not in reordered:
                reordered['department_other'] = self.fields['department_other']
            self.fields = reordered

        self.fields['start_time'].widget.attrs.update(
            {
                'placeholder': 'Ex : 9 AM',
            }
        )
        self.fields['end_time'].widget.attrs.update(
            {
                'placeholder': 'Ex: 5 PM',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'Ex : Uttara, Dhaka',
            }
        )

        self.fields['hospital_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Hospital Name',
            }
        )

        self.fields['qualification_name'].widget.attrs.update(
            {
                'placeholder': 'Ex : MBBS, BDS',
            }
        )

        self.fields['institute_name'].widget.attrs.update(
            {
                'placeholder': 'Ex : DMC',
            }
        )
        self.fields['avg_minutes_per_patient'].widget.attrs.update(
            {
                'placeholder': 'Ex : 15',
            }
        )

    class Meta:
        model = Appointment
        fields = ['full_name', 'image', 'department', 'start_time', 'end_time', 'location',
                  'hospital_name', 'qualification_name', 'institute_name', 'avg_minutes_per_patient']

    def clean(self):
        cleaned = super().clean()
        department = (cleaned.get('department') or '').strip()
        department_other = (cleaned.get('department_other') or '').strip()
        if department == "Other":
            if not department_other:
                self.add_error('department_other', 'Please enter your department.')
            else:
                cleaned['department'] = department_other
        elif department_other:
            cleaned['department'] = department_other
        elif not department:
            self.add_error('department', 'Please select or type a department.')
        return cleaned

    def is_valid(self):
        valid = super(CreateAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(CreateAppointmentForm, self).save(commit=False)
        department = (self.cleaned_data.get('department') or '').strip()
        if department:
            appointment.department = department
        if commit:
            appointment.save()
        return appointment


class TakeAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TakeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['appointment'].label = "Choose Your Doctor"
        self.fields['full_name'].label = "Full Name"
        self.fields['email'].label = "Email"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['message'].label = "Message"
        self.fields['appointment_date'].label = "Appointment Date"

        self.fields.pop('appointment_time', None)
        self.fields.pop('appointment_duration_minutes', None)
        self.fields.pop('appointment_end_time', None)

        def appointment_label(obj):
            name = (obj.full_name or "").strip()
            if not name and obj.user_id:
                name = f"{(obj.user.first_name or '').strip()} {(obj.user.last_name or '').strip()}".strip()
            if not name and obj.user_id:
                name = obj.user.email or ""
            if not name:
                name = "Doctor"
            dept = (obj.department or "").strip()
            return f"{name} ({dept})" if dept else name

        self.fields['appointment'].label_from_instance = appointment_label
        self.fields['appointment'].empty_label = "Select a doctor"

        self.fields['appointment'].widget.attrs.update(
            {
                'placeholder': 'Choose Your Doctor',
            }
        )

        self.fields['full_name'].widget.attrs.update(
            {
                'placeholder': 'Write Your Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email Address',
            }
        )

        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        self.fields['message'].widget.attrs.update(
            {
                'placeholder': 'Write a short message',
            }
        )
        self.fields['appointment_date'].widget.attrs.update(
            {
                'type': 'date',
            }
        )

    class Meta:
        model = TakeAppointment
        fields = ['appointment', 'appointment_date', 'full_name', 'email', 'phone_number', 'message']

    def _parse_start_time(self, raw_time):
        if isinstance(raw_time, time):
            return raw_time
        if not raw_time:
            return time(9, 0)
        candidates = ["%I %p", "%I:%M %p", "%H:%M", "%H:%M:%S"]
        for fmt in candidates:
            try:
                return datetime.strptime(raw_time.strip(), fmt).time()
            except ValueError:
                continue
        return time(9, 0)

    def clean(self):
        cleaned = super().clean()
        appointment = cleaned.get('appointment')
        appointment_date = cleaned.get('appointment_date')

        return cleaned

    def is_valid(self):
        valid = super(TakeAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        booking = super(TakeAppointmentForm, self).save(commit=False)
        appointment = booking.appointment
        appointment_date = booking.appointment_date

        start_time = self._parse_start_time(appointment.start_time)
        avg_minutes = appointment.avg_minutes_per_patient or 15

        with transaction.atomic():
            last_token = (
                TakeAppointment.objects.filter(
                    appointment=appointment,
                    appointment_date=appointment_date,
                )
                .order_by('-token_number')
                .values_list('token_number', flat=True)
                .first()
            )
            booking.token_number = (last_token or 0) + 1

            start_dt = datetime.combine(appointment_date, start_time)
            estimated_dt = start_dt + timedelta(minutes=avg_minutes * (booking.token_number - 1))
            if timezone.is_naive(estimated_dt):
                estimated_dt = timezone.make_aware(estimated_dt)
            booking.estimated_start_time = estimated_dt

            booking.appointment_time = start_time
            booking.appointment_duration_minutes = avg_minutes
            booking.appointment_end_time = (estimated_dt + timedelta(minutes=avg_minutes)).time()

            if commit:
                booking.save()

        return booking
