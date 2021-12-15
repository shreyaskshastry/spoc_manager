from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm

def view(request):
    return render(request, 'spoc/view.html')

def signup(request):
    if request.method=='POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('spoc-login')
    else:
        form = UserSignupForm()
    return render(request, 'spoc/signup.html', {'form':form})
