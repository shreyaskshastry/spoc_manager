from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm,SpocTableForm
from .models import Spoc
from django.contrib.auth.models import User

def view(request):
    luser = User.objects.get(username=request.user)
    context = {
        'profile' : luser.get_full_name(),
        'entries' : Spoc.objects.all()
    }
    return render(request, 'spoc/view.html',context)

def edit(request):
    return render(request, 'spoc/edittable.html')

def delete(request):
    return render(request, 'spoc/delete.html')

def signup(request):
    if request.method=='POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('spoc-login')
    else:
        form = UserSignupForm()
    return render(request, 'spoc/signup.html', {'form':form})


def make_entry(request):
    form = SpocTableForm()
    if request.method == 'POST':
        # print(request.POST)
        form = SpocTableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/view')
    context = {'form':form}
    return render(request, 'spoc/test.html', context)