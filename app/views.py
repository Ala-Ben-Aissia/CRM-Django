from django.shortcuts import render, redirect
from .forms import RegistrationForm,  RecordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
# Create your views here.

# HOMEPAGE:
def home (request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('home')
            messages.success(request, 'Logged-In Successfully...')
        else:
            messages.error(request, 'An Error Occured! Please Try Again...') 
    context = {'records': records}
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged-Out Successfully...')
    return redirect('home')

def register_user(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username, password)
            login(request, user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'registration.html', context)

def add_record(request):
    form = RecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Added Successfully...')
                return redirect('home')
        context = {'form': form}
        return render(request, 'add_record.html', context)
    messages.error(request, 'You Must Login to add record')
    return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        try:
            record = Record.objects.get(id=pk)
        except:
            messages.error(request, 'This Record Does Not Exist!')
            return redirect('home')
        form = RecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully...')
            return redirect('home')
        context = {'record': record, 'form': form}
        return render(request, 'update_record.html', context)
    messages.error(request, 'You Must Login!')
    return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        try:
            record = Record.objects.get(id=pk)
        except:
            messages.error(request, 'This Record Does Not Exist!')
            return redirect('home')
        record.delete()
        messages.success(request, 'Record deleted successfully..')
        return redirect('home')
    messages.error(request, 'You Must Login!')
    return redirect('home')

def record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
    else:
        messages.error(request, 'You must Login to get access to this record')    
        return redirect('home')
    context = {'record': record}
    return render(request, 'record.html', context)