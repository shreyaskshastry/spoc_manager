from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm,SpocTableForm
from .models import Spoc, screen_name_choices, team_name_choices
from django.contrib.auth.models import User
import pandas as pd
import os
from django.conf import settings
from django.http import HttpResponse, Http404
import datetime
from django.utils  import timezone


def view(request):
    # if request.method == "POST":
        # file = request.FILES["file"]
    luser = User.objects.get(username=request.user)
    context = {
        'profile' : luser.get_full_name(),
        'entries' : Spoc.objects.filter(is_approve=False)
    }
    if(luser.is_staff):
        return render(request, 'spoc/admin_view.html',context)
    else:
        return render(request, 'spoc/view.html',context)

def edit(request, pk):
    spoc = Spoc.objects.get(id=pk)
    form = SpocTableForm(instance=spoc)
    luser = User.objects.get(username=request.user)
    spoc.modified_date = datetime.date.today()
    if request.method == 'POST':
        # print(request.POST)
        formdata = request.POST.copy()
        formdata['modified_by'] = luser.get_full_name()
        formdata['modified_date'] = timezone.now
        formdata['created_by'] = str(spoc.created_by)
        formdata['is_delete'] = spoc.is_delete
        form = SpocTableForm(formdata,instance=spoc)
        if form.is_valid():
            form.save()
            return redirect('/view')
    context = {
        'form':form,
        'profile' : str(spoc.created_by)
    }
    return render(request, 'spoc/newentry.html', context)

def delete(request, id):
    luser = User.objects.get(username=request.user)
    context = {
        'entry' : Spoc.objects.get(pk=id)
    }
    to_delete = Spoc.objects.get(pk=id)
    to_delete.is_delete = True
    to_delete.save()
    return render(request, 'spoc/delete.html',context)

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
            spoc_entry = Spoc.objects.filter(screen_name=formdata['screen_name']).filter(team_name=formdata['team_name']).filter(spoc_name=formdata['spoc_name']).filter(is_approve=False)
            if(not spoc_entry):
                form.save()
            return redirect('/view')
        else:
            print("lol")
    context = {
        'form':form,
        'profile' : luser.get_full_name()
    }
    return render(request, 'spoc/newentry.html', context)

def validate_entry(i, df):
    screenName = df["Screen Name"][i]
    teamName = df["Team Name"][i]
    spocName = df["Spoc Name"][i]
    spoc_entry = Spoc.objects.filter(screen_name=screenName).filter(team_name=teamName).filter(spoc_name=spocName).filter(is_approve=False)
    
    if pd.isnull(screenName) or pd.isnull(teamName) or pd.isnull(spocName) :
        error = f"Atleast one cell is null in row {i+1} of the uploaded file"
        return (False, error)
    
    elif (not any(screenName in s for s in screen_name_choices)) or (not any(teamName in s for s in team_name_choices)):
        error = f"Invalid screen name or team name provided in row {i+1} of the uploaded file"
        return (False, error)
    else:
        return (True, "")

def unique_entry(i, df):
    screenName = df["Screen Name"][i]
    teamName = df["Team Name"][i]
    spocName = df["Spoc Name"][i]
    spoc_entry = Spoc.objects.filter(screen_name=screenName).filter(team_name=teamName).filter(spoc_name=spocName).filter(is_approve=False)
    if spoc_entry:
        print(f"Non-unique entry, didn't added row {i+1} in the uploaded file")
        return(False)
    return True

def upload(request):
    luser = User.objects.get(username=request.user)
    if request.method == 'POST':
        file = request.FILES['file']
        df = pd.read_csv(file, skipinitialspace = True)
        for i in df.index:
            res, err = validate_entry(i, df)
            if res:
                if unique_entry(i, df):
                    spoc = Spoc(screen_name = df["Screen Name"][i], 
                        team_name = df["Team Name"][i], 
                        spoc_name = df["Spoc Name"][i],
                        created_by = luser.get_full_name(),
                        modified_by = luser.get_full_name())
                    spoc.save()
            else:
                return render(request, 'spoc/upload.html', {'error':err})
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

@login_required
def approve(request):
    if request.user.is_superuser:
        luser = User.objects.get(username=request.user)
        context = {
            'profile' : luser.get_full_name(),
            'entries' : Spoc.objects.filter(is_delete=True,is_approve=False)
        }
        return render(request, 'spoc/admin_view.html',context)
    else:
        return redirect('spoc-view')

def confirm_delete(request,id):
    luser = User.objects.get(username=request.user)
    context = {
        'entry' : Spoc.objects.get(pk=id)
    }
    if request.method == "POST":
        to_approve = Spoc.objects.get(pk=id)
        to_approve.is_approve = True
        to_approve.save()
        return redirect('/adminview')
    return render(request, 'spoc/confirm_delete.html',context)

def confirm_reject(request,id):
    luser = User.objects.get(username=request.user)
    context = {
        'entry' : Spoc.objects.get(pk=id)
    }
    if request.method == "POST":
        to_delete = Spoc.objects.get(pk=id)
        to_delete.is_delete = False
        to_delete.save()
        return redirect('/adminview')
    return render(request, 'spoc/confirm_reject.html',context)

from django.http import HttpResponse, HttpResponseRedirect
@login_required
def login_redirect(request):
    if request.user.is_superuser: return HttpResponseRedirect("/adminview/")
    return HttpResponseRedirect("/view/")