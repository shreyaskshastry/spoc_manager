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
    if request.method == 'POST':
        # print(request.POST)
        formdata = request.POST.copy()
        formdata['modified_by'] = luser.get_full_name()
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

def approve(request):
    luser = User.objects.get(username=request.user)
    context = {
        'profile' : luser.get_full_name(),
        'entries' : Spoc.objects.filter(is_delete=True,is_approve=False)
    }
    return render(request, 'spoc/admin_view.html',context)

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