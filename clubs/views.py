from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model,login,logout
from clubs.forms import Log_in_form

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
