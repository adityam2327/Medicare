from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Appointment
from .forms import AppointmentForm


import requests
from django.conf import settings

from django.utils import timezone  # Import this

@login_required
def health_calendar(request):
    """Display the health calendar with past and upcoming appointments."""
    today = timezone.now().date()  # Get today's date dynamically

    past_appointments = Appointment.objects.filter(patient=request.user, date__lt=today)
    upcoming_appointments = Appointment.objects.filter(patient=request.user, date__gte=today)

    return render(request, 'patient/health_calendar.html', {
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
        'form': AppointmentForm()
    })

from django.utils.timezone import now
@login_required
def book_appointment(request):
    """Book a new appointment."""
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Ensure patient is set
            appointment.status = "Scheduled"  # Ensure status is set
            appointment.created_at = now()  # Set creation timestamp
            appointment.save()  # Save the appointment in the database

            return JsonResponse({'success': True, 'message': "Appointment booked successfully!", 'reload': True})
    
    return JsonResponse({'success': False, 'error': "Invalid form submission."})

@login_required
def cancel_appointment(request, appointment_id):
    """Cancel an existing appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    appointment.status = "Cancelled"
    appointment.save()
    return JsonResponse({'success': True, 'message': "Appointment cancelled successfully!"})

@login_required
def reschedule_appointment(request, appointment_id):
    """Reschedule an existing appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            appointment.status = "Rescheduled"
            appointment.save()
            return JsonResponse({'success': True, 'message': "Appointment rescheduled successfully!"})
    return JsonResponse({'success': False, 'error': "Invalid form submission."})



def dashboard(request):
    return render(request, 'patient/dashboard.html')

def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('patient:health_calendar')



import requests
from django.shortcuts import render
from django.http import JsonResponse

# Get coordinates from place name using Nominatim API
def get_coordinates(place):
    url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if data:
        return data[0]["lat"], data[0]["lon"]
    return None, None

# Render the combined care finder page
def care_finder(request):
    return render(request, "patient/care_finder.html")

# Fetch nearby hospitals using Overpass API
import requests
from django.http import JsonResponse

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def find_hospitals(request):
    place = request.GET.get("place", "").strip()  # Get the place name from input
    if not place:
        return JsonResponse({"error": "Please enter a location."}, status=400)

    query = f"""
    [out:json];
    area[name="{place}"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      way["amenity"="hospital"](area.searchArea);
      relation["amenity"="hospital"](area.searchArea);
    );
    out center;
    """

    response = requests.get(OVERPASS_URL, params={"data": query})
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch data from Overpass API."}, status=500)

    data = response.json()


    # Debugging: Print response in the server console


    hospitals = []
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name", "Unknown Hospital")
        lat = element.get("lat", element.get("center", {}).get("lat", None))
        lon = element.get("lon", element.get("center", {}).get("lon", None))

        if lat and lon:
            hospitals.append({
                "name": name,
                "latitude": lat,
                "longitude": lon,
            })

    if not hospitals:
        return JsonResponse({"error": "No hospitals found in this location."}, status=404)

    return JsonResponse({"hospitals": hospitals})


import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse

# Configure Gemini API with your API key
genai.configure(api_key=settings.GEMINI_API_KEY)

def chatbot_response(request):
    user_message = request.GET.get("message", "").strip()
    hospital_name = request.GET.get("hospital_name", "the hospital")

    # Create a Gemini AI model
    model = genai.GenerativeModel("gemini-pro")

    # Construct the prompt for Gemini API
    prompt = f"""
    You are a hospital assistant chatbot for {hospital_name}.
    Your task is to provide hospital information, services, book an appointment , staff contacts, and general assistance. you should have all the information of hospital .  
    User message: "{user_message}"
    Provide a helpful response.
    """

    try:
        # Send the prompt to Gemini API
        response = model.generate_content(prompt)
        ai_response = response.text  # Extract the AI-generated text
    except Exception as e:
        ai_response = "I'm sorry, there was an error processing your request."

    return JsonResponse({"response": ai_response})







from .models import CommunityUpdate

def community_updates(request):
    category_filter = request.GET.get('category')
    updates = CommunityUpdate.objects.order_by('-created_at')

    if category_filter:
        updates = updates.filter(category=category_filter)

    categories = CommunityUpdate.CATEGORY_CHOICES
    return render(request, 'patient/community_updates.html', {'updates': updates, 'categories': categories})



from django.shortcuts import render
from .models import HealthcareProfessional

def health_connect(request):
    specialization_filter = request.GET.get('specialization')
    professionals = HealthcareProfessional.objects.filter(availability=True).order_by('name')

    if specialization_filter:
        professionals = professionals.filter(specialization=specialization_filter)

    specializations = HealthcareProfessional.SPECIALIZATION_CHOICES
    return render(request, 'patient/health_connect.html', {
        'professionals': professionals,
        'specializations': specializations,
    })


from django.shortcuts import render
from .models import MedicalInfo

def medinfo(request):
    category_filter = request.GET.get('category')
    medinfo_list = MedicalInfo.objects.all().order_by('-published_at')

    if category_filter:
        medinfo_list = medinfo_list.filter(category=category_filter)

    categories = MedicalInfo.CATEGORY_CHOICES
    return render(request, 'patient/medinfo.html', {
        'medinfo_list': medinfo_list,
        'categories': categories,
    })




def chatbot(request):
    return render(request, 'chatbot.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PatientProfile
from .forms import PatientProfileForm

@login_required
def patient_profile(request):
    patient_profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=patient_profile)
        if form.is_valid():
            form.save()
            return redirect('patient:profile')
    else:
        form = PatientProfileForm(instance=patient_profile)

    return render(request, 'patient/profile.html', {'form': form})


def logout(request):
    return redirect('/loginn')










