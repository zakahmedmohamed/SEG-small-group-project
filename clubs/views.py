from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model,login,logout
from django.contrib import messages
from django.http import HttpResponse
from clubs.forms import Log_in_form
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
        form = Log_in_form()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
            messages.add_message(request, messages.ERROR, 'The credentials provided were invalid')

    form = Log_in_form()
    return render(request, 'log_in.html', {'form':form})

def user_list(request):
    model = get_user_model()
    users = get_user_model().objects.all()
    return render(request, 'user_list.html', {'users': users})

def show_user(request, user_id):
    users = get_user_model().objects.get(id=user_id)
    return render(request, 'show_user.html', {'users': users})