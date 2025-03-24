# MediCure

**MediCure** is an AI-driven healthcare assistance platform that helps users with health-related concerns.  
Simply upload an image of the affected area, and the AI will analyze it and suggest possible treatments.

> **Example:** Upload an image of acne on your face, and the AI will recommend suitable treatments.

## Features
✔️ User authentication for both doctors and patients  
✔️ Patient dashboard  
✔️ Doctor dashboard  
✔️ AI-based image analysis for health issues  
✔️ Appointment booking system  
✔️ OpenStreetMap integration for real-time patient and doctor location tracking  
✔️ Image upload functionality  

## Technologies Used
1. **Django** – Backend framework  
2. **HTML/CSS** – Frontend styling  
3. **JavaScript** – Frontend interactivity  
4. **OpenStreetMap** – Location tracking  
5. **Google PaLM AI Model** – For AI-powered analysis  

## How It Works
1. A **patient** creates an account and logs in.  
2. The patient uploads an image of their health concern along with a description.  
3. The AI model analyzes the image and provides treatment suggestions.  
4. On the right panel, doctors' details (including location) are displayed.  
5. The patient can:  
   - Click on a doctor’s location to see the route and distance.  
   - Book an appointment with a doctor.  
6. When an appointment is booked, an **email notification** is sent to the doctor.  
7. On the **doctor dashboard**, all patient appointments are listed.  
8. The doctor can accept the appointment and send an **acknowledgment email** to the patient confirming the appointment.  

## Installation Guide
> **Note:** Ensure you have the latest version of Python installed.

### 1. Set up a virtual environment:
```sh
python -m venv env
```

### 2. Activate the virtual environment:
#### Windows:

```sh
env\Scripts\activate
```
#### Mac or Linux:

```sh
Mac/Linux:
```

```sh
source env/bin/activate
```

### 3. Install dependencies:
```sh
pip install -r requirements.txt
```

### 4. Navigate to the project folder:
```sh
cd healthcare
```

### 5. Run the development server:
```sh
python manage.py runserver
```
Now, open your browser and go to http://127.0.0.1:8000/ to access MediCure.
