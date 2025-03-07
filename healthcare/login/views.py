from django.shortcuts import render,redirect
from login.models import Doctor,Patient
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate


def patientSignIn(request):
    if request.method == 'POST':
        patient_name = request.POST.get("patient_name")
        patient_password = request.POST.get("patient_password")
        user = authenticate(username=patient_name,password=patient_password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are now logged in")
            return redirect('patientPage')
        else:
            messages.error(request,"You have entered an invalid username or password")

    return render(request,'signIn.html')



def patientSignUp(request):

    if request.method == 'POST':
        patient_name = request.POST.get("patient_name")
        patient_email = request.POST.get("patient_email")
        patient_phno = request.POST.get("patient_phno")
        patient_password = request.POST.get("patient_password")
        patient = Patient.objects.filter(patientEmail=patient_email)
        
        if patient.exists():
            print("this email exits in db {}".format(patient_email)) 
            messages.warning(request,"This email exits, check your email id")
        else:
            patient = Patient(patientName=patient_name,patientEmail=patient_email,patientPhoneNo=patient_phno,patientPassword=patient_password)
            patient.save()
            user = User(username=patient_name,email=patient_email)
            user.set_password(patient_password)
            user.save()
            messages.success(request,"Account created.” “Thanks for signing up")
            return redirect('patientSignIn')

    return render(request,'signUp.html')




def patientLogOut(request):
    logout(request)
    messages.warning(request,"You have been successfully logged out")
    return render(request,'signIn.html')


# doctors signIn signUp and logout

def doctorSignIn(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.get(email=email)
        user = authenticate(username=user,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"You are now logged in")
            return redirect('doctorPage')
        else:
            messages.error(request,"You have entered an invalid username or password")

        
    return render(request,'doctorSignIn.html')

def doctorSignUp(request):
    if request.method == 'POST':
        doctorName = request.POST.get("doctorName")
        doctorEmail = request.POST.get("doctorEmail")
        doctorPhoneNo = request.POST.get("doctorPhoneNo")
        specializedIn = request.POST.get("specializedIn")
        doctorPassword = request.POST.get("doctorPassword")

        doctor  = Doctor(doctorName=doctorName,doctorEmail=doctorEmail,doctorPhoneNo=doctorPhoneNo,specializedIn=specializedIn,doctorPassword=doctorPassword)
        doctorEmail_db = Doctor.objects.filter(doctorEmail=doctorEmail)
        
        if doctorEmail_db.exists():
            print("this email exits in db {}".format(doctorEmail)) 
            messages.warning(request,"This email exits, check your email id")
        
        else:
            doctor.save()
            user = User(username=doctorName,email=doctorEmail)
            user.set_password(doctorPassword)
            user.save()
            print("data save in doctor model")
            messages.success(request,"Account created.” “Thanks for signing up")
            
            return redirect('doctorSignIn')

    return render(request,'doctorSignUp.html')


def doctorLogOut(request):
    logout(request)
    messages.warning(request,"You have been successfully logged out")
    return render(request,'doctorSignIn.html')
