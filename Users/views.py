from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SpmRegistrationForm

def register(request):

    if request.method == 'POST':
        form = SpmRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created! Please Login')
            return redirect('login')
    else:
        form = SpmRegistrationForm()

    return render(request, 'Users/register.html', {'form' : form})

def home_page(request):
    return render(request, 'Users/home.html')
