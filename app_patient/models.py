import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
import jdatetime
import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels


class Patient(models.Model):
    class Meta:
        verbose_name_plural = 'patients'
        db_table = 'app_patient_patient'
    national_code = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True)
    past_medical_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def clean(self, *args, **kwargs):
        if not re.match(pattern='^[0-9]+$', string=self.national_code):
            raise ValidationError(
                _("incorrect national id, must be made of digits!")
            )

    @property
    def age(self):
        return jdatetime.datetime.now().year - self.birth_year


class Phone(models.Model):
    class Meta:
        verbose_name = 'phone number'
        verbose_name_plural = 'phone numbers'
        db_table = 'app_patient_phone'
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE)
    number1 = models.CharField(max_length=11, null=True, blank=True)
    number2 = models.CharField(max_length=11, null=True, blank=True)
    number3 = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return self.patient.full_name


class Visit(models.Model):
    class Meta:
        verbose_name_plural = 'visits'
        db_table = 'app_patient_visit'
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    chief_complaint = models.TextField(null=True, blank=True)
    physical_exam = models.TextField(null=True, blank=True)
    para_clinic = models.TextField(null=True, blank=True)
    manipulation = models.BooleanField(default=False)
    needle = models.BooleanField(default=False)
    injection = models.BooleanField(default=False)
    emg = models.BooleanField(default=False)
    physiotherapy = models.BooleanField(default=False)
    procedure = models.TextField(null=True, blank=True)
    datetime = jmodels.jDateTimeField(default=jdatetime.datetime.now)
    payment = models.IntegerField(default=0)

    def __str__(self):
        return str(self.patient) + " : " + str(self.datetime)


class Prescription(models.Model):
    class Meta:
        verbose_name_plural = 'prescriptions'
        db_table = 'app_patient_prescription'
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    medicine_list = models.TextField(null=True, blank=True)
    datetime = jmodels.jDateTimeField(default=jdatetime.datetime.now)
    image = models.ImageField(upload_to='prescriptions', null=True, blank=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.patient)


@receiver(post_save, sender=Patient)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Phone.objects.create(patient=instance)


@receiver(models.signals.pre_save, sender=Prescription)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Prescription.objects.get(pk=instance.pk).image
    except Prescription.DoesNotExist:
        return False

    try:
        new_file = instance.image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except:
        pass


@receiver(models.signals.post_delete, sender=Prescription)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)