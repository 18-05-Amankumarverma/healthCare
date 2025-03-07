from django.urls import path
from . import views

urlpatterns = [
    path('patientSignIn',views.patientSignIn,name="patientSignIn"),
    path("patientSignUp",views.patientSignUp,name="patientSignUp"),
    path("patientLogOut",views.patientLogOut,name="patientLogOut"),
    path("doctorSignIn",views.doctorSignIn,name="doctorSignIn"),
    path("doctorSignUp",views.doctorSignUp,name="doctorSignUp"),
    path("doctorLogOut",views.doctorLogOut,name="doctorLogOut")
]