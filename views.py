from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    user = request.user
    if user.user_type == 'patient':
        return render(request, 'accounts/patient_dashboard.html', {'user': user})
    elif user.user_type == 'doctor':
        return render(request, 'accounts/doctor_dashboard.html', {'user': user})
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')
