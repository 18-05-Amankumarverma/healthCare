from django.shortcuts import render
from django.http import HttpResponse
from .models import Mails
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage


# Create your views here.
def sendMail(request,patientName,doctorName,doctorEmail,appointmentDate,appointmentTime,patientEmail,patientPhoneNo,appointmentFor):
    if request.method == 'POST':
        mail = Mails(senderEmail=patientEmail,senderName=patientName,recevierEmail=doctorEmail,recevierName=doctorName,mailBody=appointmentFor)
        mail.save()
        send_mail(
            "Appoinment for Check Up "+patientName,
            appointmentFor + "\nphno: "+ patientPhoneNo + "\ndate time: " + appointmentDate + " " +appointmentTime,#message
            patientEmail,#to
            [doctorEmail]#from
        )
        
        # messages.succes(request,"Mail send successfully")
    return HttpResponse("<h2>mail service</h2>")


def sendMailToPatient(request, patientName, doctorEmail, doctorName, appointmentDateTime, patientEmail, patientPhoneNo, appointmentGrantDateTime, treatmentFor, messageFromDoctor):
    if request.method == 'POST':
        # mail model to store mails record 
        mail = Mails(senderEmail=doctorEmail,
                     senderName=doctorName,
                     recevierEmail=patientEmail,
                     recevierName=patientName,
                     mailBody=treatmentFor)
        
        mail.save()

        try:
            email_subject = "Appointment Confirmation"
            email_body = f"""
            <h4>Hi {patientName}, we have received your appointment request</h4>
            <h5>Your appointment is scheduled for:</h5>
            <h6>Appointment Id: 19817</h6>
            <h6>Patient Name: {patientName}</h6>
            <h6>For: {treatmentFor}</h6>
            <h6>Doctor Name: {doctorName}</h6>
            <h6>Appointment Date: {appointmentDateTime}</h6>
            <h5>{messageFromDoctor}</h5>
            <p>Note: This is a System Generated email, so please don't reply.</p>
            """

            email = EmailMessage(
                email_subject, 
                email_body, 
                doctorEmail,  # From email
                [patientEmail]  # To email
            )
            email.content_subtype = "html"  
            email.send()

            messages.success(request, "Mail sent successfully to the patient.")

        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")

        return HttpResponse("<h2>Mail service executed successfully.</h2>")
    
    # If the request is not a POST request, return an error
    return HttpResponse("<h2>Invalid request method.</h2>", status=400)
