from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = "app_patient"

urlpatterns = [
    path('404/', views.NotFoundView.as_view(), name="404"),

    # home
    path('', views.HomeView.as_view(), name="home"),

    # patient
    path('patient/create/', views.PatientCreateView.as_view(), name="create_patient"),
    path('patient/list/', views.PatientListView.as_view(), name="patient_list"),
    path('patient/<str:pk>/', views.PatientDetailView.as_view(), name="patient_detail"),
    path('patient/<str:pk>/update/', views.PatientUpdateView.as_view(), name="update_patient"),
    path('patient/<str:pk>/delete/', views.PatientDeleteView.as_view(), name="delete_patient"),

    # phone
    path('patient/<str:pk>/phone/', views.PhoneUpdateView.as_view(), name="update_phone"),

    # visit
    path('patient/<str:pk>/visit/list/', views.VisitListView.as_view(), name="visit_list"),
    path('patient/<str:pk>/visit/create/', views.VisitCreateView.as_view(), name="create_visit"),
    path('visit/<str:pk>/', views.VisitDetailView.as_view(), name="visit_detail"),
    path('visit/<str:pk>/update/', views.VisitUpdateView.as_view(), name="update_visit"),
    path('visit/<str:pk>/delete/', views.VisitDeleteView.as_view(), name="delete_visit"),

    # prescription
    path('patient/<str:pk>/prescription/list/', views.PrescriptionListView.as_view(), name="prescription_list"),
    path('patient/<str:pk>/prescription/create/', views.PrescriptionCreateView.as_view(), name="create_prescription"),
    path('prescription/<str:pk>/', views.PrescriptionDetailView.as_view(), name="prescription_detail"),
    path('prescription/<str:pk>/update/', views.PrescriptionUpdateView.as_view(), name="update_prescription"),
    path('prescription/<str:pk>/delete/', views.PrescriptionDeleteView.as_view(), name="delete_prescription"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
