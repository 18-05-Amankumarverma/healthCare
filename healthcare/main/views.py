from django.shortcuts import render,redirect
from .models import UserQuery
from django.http import JsonResponse,HttpResponse
import os
import google.generativeai as genai
import json
from django.conf import settings
from django.core.files.storage import default_storage
import requests
from django.contrib.auth.decorators import login_required
from .models import Appointment
from mail.views import sendMail
from django.contrib import messages

doctorsList = [
    {
        "doctor_name": "Dr. R.L. Agarwal - General Physician",
        "specialist": "Dermatologist",
        "phone_no": "9006445307",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Brahmananda Narayana Multispeciality Hospital, NH-33, near Pardih Chowk, Tamolia, Jamshedpur, Jharkhand 831012",
        "time": "10:00 AM - 10:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.780, "lng": 86.150 }
    },
    {
        "doctor_name": "Dr. S.K. Sinha - Cardiologist",
        "specialist": "Cardiologist",
        "phone_no": "9876543210",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Tata Main Hospital, Bistupur, Jamshedpur, Jharkhand 831001",
        "time": "9:00 AM - 5:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.790, "lng": 86.180 }
    },
    {
        "doctor_name": "Dr. Arvind Kumar - Orthopedic",
        "specialist": "Orthopedic",
        "phone_no": "9998887776",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Meditrina Hospital, Adityapur, Jamshedpur, Jharkhand 831013",
        "time": "10:30 AM - 7:30 PM",
        "status": "Open",
        "coordinates": { "lat": 22.810, "lng": 86.220 }
    },
    {
        "doctor_name": "Dr. P.K. Gupta - Neurologist",
        "specialist": "Neurologist",
        "phone_no": "9123456789",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Sadar Hospital, Sakchi, Jamshedpur, Jharkhand 831001",
        "time": "8:00 AM - 2:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.825, "lng": 86.250 }
    },
    {
        "doctor_name": "Dr. Manisha Verma - Gynecologist",
        "specialist": "Gynecologist",
        "phone_no": "9345678901",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Lifeline Hospital, Mango, Jamshedpur, Jharkhand 831012",
        "time": "9:30 AM - 6:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.835, "lng": 86.260 }
    },
    {
        "doctor_name": "Dr. Amit Kumar - Pediatrician",
        "specialist": "Pediatrician",
        "phone_no": "9988776655",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Mother & Child Care Clinic, Sonari, Jamshedpur, Jharkhand 831011",
        "time": "10:00 AM - 8:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.775, "lng": 86.140 }
    },
    {
        "doctor_name": "Dr. Ravi Shankar - Dentist",
        "specialist": "Dentist",
        "phone_no": "9876501234",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Smile Dental Clinic, Kadma, Jamshedpur, Jharkhand 831005",
        "time": "9:00 AM - 7:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.805, "lng": 86.170 }
    },
    {
        "doctor_name": "Dr. Piyush Mishra - ENT Specialist",
        "specialist": "ENT Specialist",
        "phone_no": "9123456798",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Jamshedpur ENT Hospital, Sakchi, Jamshedpur, Jharkhand 831001",
        "time": "10:00 AM - 6:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.815, "lng": 86.200 }
    },
    {
        "doctor_name": "Dr. Alok Das - Oncologist",
        "specialist": "Oncologist",
        "phone_no": "9012345678",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Cancer Care Center, Baridih, Jamshedpur, Jharkhand 831017",
        "time": "9:00 AM - 4:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.845, "lng": 86.280 }
    },
    {
        "doctor_name": "Dr. Anjali Kapoor - Psychiatrist",
        "specialist": "Psychiatrist",
        "phone_no": "9112233445",
        "doctorEmail": "akverma2017.jsr@gmail.com",
        "address": "Mind Wellness Clinic, Bistupur, Jamshedpur, Jharkhand 831001",
        "time": "10:00 AM - 5:00 PM",
        "status": "Open",
        "coordinates": { "lat": 22.790, "lng": 86.190 }
    }
]

# view for handling AI request

# Helper function to find file in the folder
def find_file_in_folder(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return file_path
    else:
        return None


# Configure Gemini AI securely
genai.configure(api_key=settings.GIMINI_APIKEY)  # Move this outside the function

# AI Model Configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Initialize Model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)


# View to handle patient data and file upload
@login_required(login_url='patientSignIn')
def patientPage(request):
    if request.method == 'POST':
        
        # Get uploaded file and user query
        file = request.FILES['user_uploadedFile']
        query = request.POST['user_query']
        username = "Ravi Sharma"

        # Save the user message (including file and query)
        user_message = UserQuery(username=username, user_uploadedFile=file, user_query=query)
        user_message.save()

        uploadedFileName = file.name

        # Get file path in 'media/disease' directory
        folder_path = 'media/disease'
        file_name = uploadedFileName

        # Find the file in the folder
        file_path = find_file_in_folder(folder_path, file_name)

        print(file_path)
        
        if file_path:
            print(f"File found: {file_path}")

            try:
                # Generate content from the AI model
                response = model.generate_content([
                        "Analyze the image and suggest the medical treatment and medicine for the detected disease.",
                        "Provide a structured response in the form of JSON  with the following fields:",
                        "- Disease Name",
                        "- Symptoms",
                        "- Recommended Treatment",
                        "- Medicines (if applicable)",
                        "- Any precautions",
                        "Ensure the response is formatted properly json , not a paragraph.",
                        file_path,  # Directly passing file path
                    ])

                    # Process the response
                data = response.text.strip()  # Remove leading/trailing whitespace

                   # In your view function
                try:
                        # Try parsing the response as JSON
                        parsed_data = json.loads(data)
                        formatted_response = json.dumps(parsed_data, indent=4)  # Make it readable
                except json.JSONDecodeError:
                        # Fallback: Convert text into list format manually
                        formatted_response = data.replace("*", "\n")  # Convert newline to bullet points
                print("\n--- Suggested Treatment ---\n", formatted_response)

                request.session['doctorsList'] = doctorsList
                
                return render(request, 'patient.html', {'AIresponse': formatted_response, 'userQuestions': query,'doctorsList':doctorsList})

            except Exception as e:
                    print(f"Error generating response: {e}")

        else:
            print("File not found.")
        
    return render(request,'patient.html')





@login_required(login_url='patientSignIn')
def patientMap(request):
    doctorsList = request.session['doctorsList']

    return render(request, 'map.html',{'doctorsList':doctorsList})



@login_required(login_url='doctorSignIn')
def appointmentList(request):
    lst_of_appointment = []
    appointments = Appointment.objects.all()
    for appointment in appointments.values():
        lst_of_appointment.append(appointment)
    return JsonResponse(lst_of_appointment,status=200,safe=False)



@login_required(login_url='doctorSignIn')
def doctorPage(request):
    lst_of_appointment = []
    appointments = Appointment.objects.all()
    for appointment in appointments.values():
        lst_of_appointment.append(appointment)
    return render(request,'doctor.html',{'lst_of_appointment':lst_of_appointment})

# def appointmentForm(request):
#     if request.method == 'POST':
#         if request.method == "POST":
#             appointementFor = request.POST.get("appointementFor")
#             doctorName = request.POST.get("doctorName")
#             patientName = request.POST.get("patientName")
#             appointmentDate = request.POST.get("appointmentDate")
#             appointmentTime = request.POST.get("appointmentTime")
#             appointementStatus = request.POST.get("appointementStatus") == "on"

#              # Save appointment in database
#             appointment = Appointment.objects.create(
#                 appointementFor=appointementFor,
#                 doctorName=doctorName,
#                 patientName=patientName,
#                 appointmentDate=appointmentDate,
#                 appointmentTime=appointmentTime,
#             )
#     return render(request,'appointment.html')

def dataSanitizer(field):
    field = field.strip()
    if type(field) == 'str' and len(field) >=0 :
        return field
    else:
        return False



@login_required(login_url='doctorSignIn')
def appointment(request):
    if request.method == 'POST':
        appointmentFor = request.POST.get("appointmentFor")  # body for mail
        doctorName = request.POST.get("doctorName")
        patientName = request.POST.get("patientName")
        patientEmail = request.POST.get("patientEmail")
        patientPhoneNo = request.POST.get("patientPhoneNo")
        doctorEmail = request.POST.get("doctorEmail")
        appointmentDate = request.POST.get("appointmentDate")
        appointmentTime = request.POST.get("appointmentTime")
        

        if appointmentFor == 'blank' and doctorName == 'blank' and patientName == 'blank' and patientEmail == 'blank' and patientPhoneNo == 'blank' and doctorEmail == 'blank' and  appointmentDate == 'blank' and appointmentTime == 'blank':
                messages.error(request,'check all fields')
        else:
            appointment = Appointment(appointmentFor=appointmentFor,doctorName=doctorName,doctorEmail=doctorEmail,patientName=patientName,patientEmail=patientEmail,patientPhoneNo=patientPhoneNo,appointmentDate=appointmentDate,appointmentTime=appointmentTime)
            if appointment:
                appointment.save()

                # send mail to doctor
                sendMail(request,patientName,doctorName,doctorEmail,appointmentDate,appointmentTime,patientEmail,patientPhoneNo,appointmentFor)
                messages.success(request,"mail sent succesfully")
                return redirect('appointment')
        
            else:
                messages.error(request,"mail not sent")
                return redirect('appointment')
        


    return render(request,'appointment.html')


from django.shortcuts import get_object_or_404
from .models import Appointment,AppointmentGrant
from mail.views import sendMailToPatient


@login_required(login_url='doctorSignIn')
def acceptAppointmentMail(request):
    if request.method == 'POST':
        patientName = request.POST.get('patientName')
        appointmentDateTime = request.POST.get('appointmentDateTime')
        appointementStatus = request.POST.get('appointmentStatus')
        patientEmail = request.POST.get('patientEmail')
        patientPhoneNo = request.POST.get('patientPhoneNo')
        appointmentGrantDateTime = request.POST.get('appointmentGrantDateTime')
        treatmentFor = request.POST.get('treatmentFor')
        messageFromDoctor = request.POST.get('messageFromDoctor')

        appointmentGrant =  AppointmentGrant(
            treatmentFor=treatmentFor,
            patientName=patientName,
            patientEmail=patientEmail,
            patientPhoneNo=patientPhoneNo,
            appointmentDateTime=appointmentDateTime,
            appointmentGrantDateTime=appointmentGrantDateTime,
            appointementStatus=appointementStatus,
            messageFromDoctor=messageFromDoctor
        )
        if appointmentGrant:
            appointmentGrant.save()

            # appointment = get_object_or_404(Appointment, pk=request.POST.get('appointmentId'))  # Pass 'appointmentId' in the form
            # appointment.appointmentStatus = True  # Fixed the field name typo
            # appointment.save()

            # send mail to doctor
            sendMailToPatient(request,patientName,request.user.email,request.user.username,appointmentDateTime,patientEmail,patientPhoneNo,appointmentGrantDateTime,treatmentFor,messageFromDoctor)
            return redirect('doctorPage')
        
        else:
            messages.error(request,"mail not sent")
            return redirect('doctorPage')

    return render(request,'acceptAppointment.html')




@login_required(login_url='doctorSignIn')
def acceptAppointment(request,id):
    appointment = get_object_or_404(Appointment,pk=id)
    return render(request,'acceptAppointment.html',{'appointment':appointment})



def patientProfile(request):
    return render(request,'patientProfile.html')




def patientHelpPage(request):
    return render(request,'patientHelpPage.html')


def patientAppointmentList(request):
    return render(request,'patientAppointmentList.html')