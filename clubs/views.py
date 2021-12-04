from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model,login,logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from clubs.forms import Log_in_form
from clubs.models import User
from .forms import SignUpForm, Create_A_Club_Form, Log_in_form
from clubs.models import Club, UserClubs
from .models import User


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

def create_club(request):
    if request.method =='POST':
        form = Create_A_Club_Form(request.POST)
        if form.is_valid():
            newClub = form.save()
            #clubName = form.cleaned_data['name']
            club_user = UserClubs(user = request.user, club = newClub)
            club_user.is_member = True
            club_user.is_officer = True
            club_user.is_owner = True
            club_user.save()
            return redirect('club_list')
    else:
        form = Create_A_Club_Form()
    return render(request, 'create_club.html', {'form': form})

# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_home(request):
    return render(request, 'user_home.html')

def club_home(request, club_name):
    club = Club.objects.get(name = club_name)
    club_user = UserClubs.objects.all().get(user = request.user, club = club)
    return render(request, 'club_home.html', {'club': club_name, 'user': club_user})

def log_in(request):
    if request.method == "POST":
        form = Log_in_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_home')
            messages.add_message(request, messages.ERROR, 'The credentials provided were invalid')
    form = Log_in_form()
    return render(request, 'log_in.html', {'form':form})

def club_list(request):
    joined_clubs = UserClubs.objects.all().filter(user = request.user)
    clubs = Club.objects.filter().order_by()
    return render(request, 'club_list.html', {'clubs':clubs})

def my_clubs(request):
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True)
    clubIDs = joined_clubs.values_list('club')
    clubs = Club.objects.filter(id__in = clubIDs)
    #clubs = Club.objects.filter().order_by()
    user = request.user
    return render(request, 'my_clubs.html', {'clubs':clubs, 'user':user })

def view_members(request,club_name):
    """
    currentUser = request.user
    currentClub = UserClubs.objects.get(user = currentUser.id).objects.filter(club = club_name)
    if currentClub.is_officer:
        {'currentClub',currentClub}
    """

    #currentUser = request.user
    #currentClub = UserClubs.objects.get(user = currentUser.id, club = club_name)
    clubObject = Club.objects.get(name = club_name)
    currentClub = UserClubs.objects.all().get(club = clubObject, user = request.user)
    members = UserClubs.objects.all().filter(club = clubObject).filter(is_member=True)
    return (render(request, 'view_members.html',{'users':members, 'currentClub': currentClub} ))
    

def club_profile(request,club_name):
    currentClub = Club.objects.get(name = club_name)
    memberSize = UserClubs.objects.all().filter(club = currentClub).count()
    owner = UserClubs.objects.all().get(club = currentClub, is_owner = True)
    return (render(request, 'club_profile.html', {'club':currentClub, 'memberSize': memberSize, 'owner': owner}))

def club_application(request, club_name):
    new_user = request.user
    apply_club = Club.objects.get(id = club_name)
    if(not(UserClubs.objects.filter(user = new_user, club = apply_club).exists())):
        club_user = UserClubs(user = new_user, club = apply_club)
        club_user.save()
    return redirect('club_list')
    
def application_list(request, club_name):
    apply_club = Club.objects.get(name = club_name)
    users = UserClubs.objects.filter(club = apply_club, is_member = False)
    return render(request, 'application_list.html', {'users': users})

def approve_application(request, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('my_clubs')
    else:
        user.is_member=True
        user.save()
        return redirect('my_clubs')

def owner_commands(request, club_name):
    selected_club = Club.objects.get(name = club_name)
    members = UserClubs.objects.all().filter(club = selected_club).filter(is_member=True).exclude(user = request.user)
    return (render(request, 'owner_commands.html',{'members':members, 'selected_club': selected_club} ))

def promote_member(request, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('my_clubs')
    else:
        user.is_officer=True
        user.save()
        return redirect('my_clubs')

def demote_officer(request, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('my_clubs')
    else:
        user.is_officer=False
        user.save()
        return redirect('my_clubs')

def transfer_ownership(request, club_name, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('my_clubs')
    else:
        selected_club = Club.objects.get(name = club_name)
        owner_user = UserClubs.objects.get(user=request.user, club = selected_club)
        owner_user.is_owner = False
        owner_user.save()
        user.is_officer=True
        user.is_owner=True
        user.save()
        return redirect('my_clubs')

def log_out(request):
    logout(request)
    return redirect('home')

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def show_user(request, user_id):
    users = get_user_model().objects.get(id=user_id)
    return render(request, 'show_user.html', {'users': users})
