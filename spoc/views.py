from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm,SpocTableForm
from .models import Spoc
from django.contrib.auth.models import User
import pandas as pd
import os
from django.conf import settings
from django.http import HttpResponse, Http404


def view(request):
    if request.method == "POST":
        file = request.FILES["file"]
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
    luser = User.objects.get(username=request.user)
    if request.method == 'POST':
        # print(request.POST)
        formdata = request.POST.copy()
        formdata['created_by'] = luser.get_full_name()
        formdata['modified_by'] = luser.get_full_name()
        form = SpocTableForm(formdata)
        if form.is_valid():
            form.save()
            return redirect('/view')
        else:
            print("lol")
    context = {
        'form':form,
        'profile' : luser.get_full_name()
    }
    return render(request, 'spoc/newentry.html', context)

def upload(request):
    luser = User.objects.get(username=request.user)
    if request.method == 'POST':
        file = request.FILES['file']
        print(file)
        df = pd.read_csv(file)
        for i in df.index:
            spoc = Spoc(screen_name = df["Screen Name"][i], 
                team_name = df["Team Name"][i], 
                spoc_name = df["Spoc Name"][i],
                created_by = luser.get_full_name(),
                modified_by = luser.get_full_name())
            spoc.save()
        return redirect('spoc-view')
    else:
        return render(request, 'spoc/upload.html')

def download(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'template.csv')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
