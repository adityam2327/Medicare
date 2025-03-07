from django.shortcuts import render, redirect
from django.http import HttpResponse

def dash(request):
    return render(request, 'doctor/dash.html')



def community_updates(request):

    return render(request, 'doctor/community_updates.html')




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DoctorProfileForm
from .models import DoctorProfile

@login_required
def doctor_profile(request):
    profile, created = DoctorProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('doctor:doctor_profile')
    else:
        form = DoctorProfileForm(instance=profile)

    return render(request, 'doctor/doctor_profile.html', {'form': form})












@login_required
def doctor_dashboard(request):
    return render(request, 'doctor/doctor_dashboard.html')

def logout(request):
    return redirect('/loginn')