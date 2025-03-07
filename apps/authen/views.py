from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        role = request.POST.get('role')  # Get the selected role (doctor/patient)
        
        print(fnm, emailid, pwd, role)

        # Create a new user and store the role in the first_name field
        my_user = User.objects.create_user(username=fnm, email=emailid, password=pwd)
        my_user.first_name = role  # Store role in first_name (default User model doesn't have a role field)
        my_user.save()
        
        return redirect('/loginn')  # Redirect to login page after successful signup
    
    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        
        print(fnm, pwd)
        
        # Authenticate the user
        userr = authenticate(request, username=fnm, password=pwd)
        
        if userr is not None:
            login(request, userr)
            
            # Redirect based on role (stored in first_name)
            if userr.first_name == 'doctor':
                return redirect('/doctor')
            else:
                return redirect('/patient')  # Default to patient if role is missing
            
        else:
            return redirect('/loginn')  # Stay on the login page if credentials are incorrect

    return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def index(request):
    return render(request, 'index.html')

def signout(request):
    logout(request)
    return redirect('/loginn')
