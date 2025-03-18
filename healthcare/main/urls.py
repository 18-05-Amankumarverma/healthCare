from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    
    path('patientPage',views.patientPage,name='patientPage'), 
    path('patientMap',views.patientMap,name='patientMap') , 
    path('doctorPage',views.doctorPage,name='doctorPage'),
    path('appointment',views.appointment,name='appointment'),
    path('appointmentList',views.appointmentList,name='appointmentList'),
    path('acceptAppointment/<id>',views.acceptAppointment,name='acceptAppointment'),
    path('acceptAppointmentMail',views.acceptAppointmentMail,name='acceptAppointmentMail'),
    path('patientProfile',views.patientProfile,name='patientProfile'),
    path('patientHelpPage',views.patientHelpPage,name='patientHelpPage'),
    path('patientAppointmentList',views.patientAppointmentList,name='patientAppointmentList'),
]