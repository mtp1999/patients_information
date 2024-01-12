from django import forms
from .models import Patient, Phone, Prescription, Visit


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'




