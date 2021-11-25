from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model,login,logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from clubs.forms import Log_in_form
from clubs.models import User
from .forms import SignUpForm
from .models import User


# View for the sign up page
def sign_up(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            #For now goes back to sign up
            return redirect('applications')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_home(request):
    return render(request, 'user_home.html')

def log_in(request):
    if request.method == "POST":
        form = Log_in_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if(user.is_officer or user.is_owner):
                    return redirect('applications')
                #needs to go to a homepage for member
                elif(user.is_member):
                    return redirect('user_home')
                else:
                    return redirect('awaiting_application')
            messages.add_message(request, messages.ERROR, 'The credentials provided were invalid')
    form = Log_in_form()
    return render(request, 'log_in.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('home')

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def show_user(request, user_id):
    users = get_user_model().objects.get(id=user_id)
    return render(request, 'show_user.html', {'users': users})

def awaiting_application(request):
    return render(request, 'awaiting_application.html')

def applications(request):
    users = User.objects.filter(is_member=False)
    return render(request, 'applications.html', {'users': users})

def approve_application(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('applications')
    else:
        user.is_member=True
        user.save()
        return render(request, 'approve_application.html', {'user': user})
