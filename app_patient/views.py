from django.shortcuts import redirect, render
import django.views.generic as cbv
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Patient, Phone, Visit, Prescription
from .forms import PatientForm, PhoneForm, VisitForm, PrescriptionForm


class NotFoundView(cbv.TemplateView):
    template_name = '404.html'


class HomeView(cbv.TemplateView):
    template_name = 'app_patient/home.html'


class PatientListView(cbv.TemplateView):
    template_name = 'app_patient/patient_list.html'

    def post(self, *args, **kwargs):

        try:
            patients = None
            if national_code := self.request.POST.get('national_code'):
                patients = Patient.objects.filter(national_code=national_code)
            elif last_name := self.request.POST.get('last_name'):
                patients = Patient.objects.filter(last_name__contains=last_name)
            return render(self.request, 'app_patient/patient_list.html', context={'patients': patients})
        except:
            messages.error(self.request, "مراجعه کننده مورد نظر یافت نشد!")
            return redirect('app_patient:home')


class PatientDetailView(LoginRequiredMixin, cbv.DetailView):
    template_name = 'app_patient/patient_detail.html'
    context_object_name = 'patient'

    def get_queryset(self):
        patient = Patient.objects.filter(pk=self.kwargs.get('pk'))
        return patient


class PatientCreateView(LoginRequiredMixin, cbv.CreateView):
    template_name = 'app_patient/create_patient.html'
    form_class = PatientForm

    def get_success_url(self):
        patient = Patient.objects.get(national_code=self.request.POST.get('national_code'))
        messages.success(self.request, 'پرونده با موفقیت ایجاد شد!')
        return reverse('app_patient:patient_detail', kwargs={'pk': patient.pk})

    def form_invalid(self, form):
        messages.error(self.request, "کد ملی وارد شده صحیح نمیباشد!")
        return redirect('app_patient:create_patient')


class PatientUpdateView(LoginRequiredMixin, cbv.UpdateView):
    template_name = 'app_patient/update_patient.html'
    form_class = PatientForm

    def get_queryset(self):
        patient = Patient.objects.filter(pk=self.kwargs.get('pk'))
        return patient

    def get_success_url(self):
        patient = Patient.objects.get(national_code=self.request.POST.get('national_code'))
        messages.success(self.request, 'بروزرسانی با موفقیت انجام شد!')
        return reverse('app_patient:patient_detail', kwargs={'pk': patient.pk})

    def form_invalid(self, form):
        messages.error(self.request, "اطلاعات وارد شده صحیح نمیباشد!")
        return redirect('app_patient:update_patient', pk=self.get_queryset()[0].pk)


class PatientDeleteView(LoginRequiredMixin, cbv.DeleteView):
    template_name = 'app_patient/delete_patient.html'
    context_object_name = 'patient'

    def get_queryset(self):
        patient = Patient.objects.filter(pk=self.kwargs.get('pk'))
        return patient

    def get_success_url(self):
        messages.success(self.request, 'پرونده با موفقیت حذف شد!')
        return reverse_lazy('app_patient:home')


class PhoneUpdateView(LoginRequiredMixin, cbv.UpdateView):
    template_name = 'app_patient/update_phone.html'
    form_class = PhoneForm
    context_object_name = 'phone'

    def get_queryset(self):
        phone = Phone.objects.filter(patient_id=self.kwargs.get('pk'))
        return phone

    def get_success_url(self):
        messages.success(self.request, 'بروزرسانی با موفقیت انجام شد!')
        return reverse('app_patient:patient_detail', kwargs={'pk': self.get_queryset()[0].pk})

    def form_invalid(self, form):
        messages.error(self.request, "اطلاعات وارد شده صحیح نمیباشد!")
        return redirect('app_patient:update_phone', pk=self.get_queryset()[0].pk)


class VisitListView(LoginRequiredMixin, cbv.ListView):
    template_name = 'app_patient/visit_list.html'
    context_object_name = 'visit_list'

    def get_queryset(self):
        visit_list = Visit.objects.filter(patient_id=self.kwargs.get('pk')).order_by('-datetime')
        return visit_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs.get('pk'))
        return context


class VisitDetailView(LoginRequiredMixin, cbv.DetailView):
    template_name = 'app_patient/visit_detail.html'
    context_object_name = 'visit'

    def get_queryset(self):
        visit = Visit.objects.filter(pk=self.kwargs.get('pk'))
        return visit


class VisitCreateView(LoginRequiredMixin, cbv.CreateView):
    template_name = 'app_patient/create_visit.html'
    form_class = VisitForm

    def get_success_url(self):
        visit = Visit.objects.filter(patient__id=self.request.POST.get('patient')).order_by('-datetime')[0]
        messages.success(self.request, 'ویزیت با موفقیت ایجاد شد!')
        return reverse('app_patient:visit_detail', kwargs={'pk': visit.pk})

    def form_invalid(self, form):
        messages.error(self.request, "اطلاعات وارد شده صحیح نمیباشد!")
        return redirect('app_patient:create_visit', pk=self.get_context_data()['patient'].pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(pk=self.kwargs.get('pk'))
        return context


class VisitUpdateView(LoginRequiredMixin, cbv.UpdateView):
    template_name = 'app_patient/update_visit.html'
    form_class = VisitForm
    context_object_name = 'visit'

    def get_queryset(self):
        visit = Visit.objects.filter(pk=self.kwargs.get('pk'))
        return visit

    def get_success_url(self):
        messages.success(self.request, 'بروزرسانی با موفقیت انجام شد!')
        return reverse('app_patient:visit_detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_invalid(self, form):
        messages.error(self.request, "اطلاعات وارد شده صحیح نمیباشد!")
        return redirect('app_patient:update_visit', pk=self.kwargs.get('pk'))


class VisitDeleteView(LoginRequiredMixin, cbv.DeleteView):
    template_name = 'app_patient/delete_visit.html'
    context_object_name = 'visit'

    def get_queryset(self):
        visit = Visit.objects.filter(pk=self.kwargs.get('pk'))
        return visit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_pk'] = self.get_queryset().get(pk=self.kwargs.get('pk')).patient.pk
        return context

    def get_success_url(self):
        messages.success(self.request, 'ویزیت با موفقیت حذف شد!')
        return reverse_lazy('app_patient:visit_list', kwargs={'pk': self.get_context_data().get('patient_pk')})


class PrescriptionListView(LoginRequiredMixin, cbv.ListView):
    template_name = 'app_patient/prescription_list.html'
    context_object_name = 'prescription_list'

    def get_queryset(self):
        prescription_list = Prescription.objects.filter(patient_id=self.kwargs.get('pk')).order_by('-datetime')
        return prescription_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs.get('pk'))
        return context


class PrescriptionDetailView(LoginRequiredMixin, cbv.DetailView):
    template_name = 'app_patient/prescription_detail.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        prescription = Prescription.objects.filter(pk=self.kwargs.get('pk'))
        return prescription


class PrescriptionCreateView(LoginRequiredMixin, cbv.CreateView):
    template_name = 'app_patient/create_prescription.html'
    form_class = PrescriptionForm

    def get_success_url(self):
        prescription = Prescription.objects.filter(patient__id=self.request.POST.get('patient')).order_by('-datetime')[0]
        messages.success(self.request, 'نسخه با موفقیت ایجاد شد!')
        return reverse('app_patient:prescription_detail', kwargs={'pk': prescription.pk})

    def form_invalid(self, form):
        messages.error(self.request, "اطلاعات وارد شده صحیح نمیباشد!")
        return redirect('app_patient:create_prescription', pk=self.get_context_data()['patient'].pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(pk=self.kwargs.get('pk'))
        return context


class PrescriptionUpdateView(LoginRequiredMixin, cbv.UpdateView):
    template_name = 'app_patient/update_prescription.html'
    form_class = PrescriptionForm
    context_object_name = 'prescription'

    def get_queryset(self):
        prescription = Prescription.objects.filter(pk=self.kwargs.get('pk'))
        return prescription

    def get_success_url(self):
        messages.success(self.request, 'بروزرسانی با موفقیت انجام شد!')
        return reverse('app_patient:prescription_detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_invalid(self, form):
        messages.error(self.request, "اطلاعات وارد شده صحیح نمیباشد!")
        return redirect('app_patient:update_prescription', pk=self.kwargs.get('pk'))


class PrescriptionDeleteView(LoginRequiredMixin, cbv.DeleteView):
    template_name = 'app_patient/delete_prescription.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        prescription = Prescription.objects.filter(pk=self.kwargs.get('pk'))
        return prescription

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_pk'] = self.get_queryset().get(pk=self.kwargs.get('pk')).patient.pk
        return context

    def get_success_url(self):
        messages.success(self.request, 'نسخه با موفقیت حذف شد!')
        return reverse_lazy('app_patient:prescription_list', kwargs={'pk':self.get_context_data().get('patient_pk')})
