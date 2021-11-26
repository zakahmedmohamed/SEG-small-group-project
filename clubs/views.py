from os import name
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model,login,logout
from django.contrib import messages
from django.http import HttpResponse
from clubs.forms import Log_in_form
from clubs.models import Club
from .forms import SignUpForm


# View for the sign up page
def sign_up(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            #For now goes back to sign up
            return redirect('sign_up')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


# Create your views here.
def home(request):
    return render(request, 'home.html')

def log_in(request):
    if request.method == "POST":
        form = Log_in_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('club_list')
            messages.add_message(request, messages.ERROR, 'The credentials provided were invalid')

    form = Log_in_form()
    return render(request, 'log_in.html', {'form':form})


def club_list(request):
    model = Club
    clubs = Club.objects.filter().order_by()
    return render(request, 'club_list.html', {'clubs':clubs})

def club_profile(request,club_name):
    club = Club.objects.get(name = club_name)
    print(club)
    return (render(request, 'club_profile.html', {'club':club}))

def log_out(request):
    logout(request)
    return(redirect('home'))
