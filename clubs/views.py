from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q
from clubs.forms import Log_in_form
from clubs.models import User
from .forms import SignUpForm, Create_A_Club_Form, Log_in_form, UserForm, PasswordForm
from clubs.models import Club, UserClubs
from .models import User

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect('my_clubs')
        else:
            return view_function(request)
    return modified_view_function

def owner_required(view_function):
    def modified_view_function(request, club_name, **kwargs):
        selected_club = Club.objects.get(name = club_name)
        owner_user = UserClubs.objects.get(user=request.user, club = selected_club)
        if not owner_user.is_owner:
            return redirect('club_list')
        else:
            return view_function(request, club_name, **kwargs)
    return modified_view_function

def officer_required(view_function):
    def modified_view_function(request, club_name, **kwargs):
        selected_club = Club.objects.get(name = club_name)
        owner_user = UserClubs.objects.get(user=request.user, club = selected_club)
        if not owner_user.is_officer:
            return redirect('club_list')
        else:
            return view_function(request, club_name, **kwargs)
    return modified_view_function

def member_required(view_function):
    def modified_view_function(request, club_name, **kwargs):
        selected_club = Club.objects.get(name = club_name)
        member_user = UserClubs.objects.filter(user=request.user, club = selected_club)
        if not member_user.exists() or not member_user.get().is_member:
            return redirect('my_clubs')
        else:
            return view_function(request, club_name, **kwargs)
    return modified_view_function

# View for the sign up page
def sign_up(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            #For now goes back to sign up
            return redirect('my_clubs')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('my_clubs')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})

@login_required
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('my_clubs')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})

@login_required
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
@login_prohibited
def home(request):
    return render(request, 'home.html')


@login_required
@member_required
def club_home(request, club_name):
    club = Club.objects.get(name = club_name)
    club_user = UserClubs.objects.all().get(user = request.user, club = club)
    #form = Club_Navigation_Form(request.POST)
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True)
    clubIDs = joined_clubs.values_list('club')
    clubs = Club.objects.filter(id__in = clubIDs)
    #form.fields['clubs'] = clubs
    return render(request, 'club_home.html', {'club': club_name, 'clubUser': club_user})

@login_prohibited
def log_in(request):
    if request.method == "POST":
        form = Log_in_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = request.POST.get('next') or 'my_clubs'
                return redirect(redirect_url)
            messages.add_message(request, messages.ERROR, 'The credentials provided were invalid')
    form = Log_in_form()
    next = request.GET.get('next') or ''
    return render(request, 'log_in.html', {'form':form, 'next':next})

@login_required
def club_list(request):
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True) # All the clubs the user is in
    clubIDs = joined_clubs.values_list('club')
    clubs = Club.objects.exclude(id__in = clubIDs)   #All the clubs 
    return render(request, 'club_list.html', {'clubs':clubs, 'joined_clubs':joined_clubs})

@login_required
def my_clubs(request):
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True)
    clubIDs = joined_clubs.values_list('club')
    clubs = Club.objects.filter(id__in = clubIDs)
    #clubs = Club.objects.filter().order_by()
    user = request.user
    owner_dict = {}
    for c in clubs:
        owner_dict[c] = UserClubs.objects.all().get(club = c, is_owner = True)
    return render(request, 'my_clubs.html', {'clubs':clubs, 'user':user, 'owners':owner_dict})

@login_required
@member_required
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

@login_required
def club_profile(request,club_name):
    currentClub = Club.objects.get(name = club_name)
    memberSize = UserClubs.objects.all().filter(club = currentClub, is_member = True).count()
    owner = UserClubs.objects.all().get(club = currentClub, is_owner = True)
    return (render(request, 'club_profile.html', {'club':currentClub, 'memberSize': memberSize, 'owner': owner}))

@login_required
def club_application(request, club_name):
    new_user = request.user
    apply_club = Club.objects.get(id = club_name)
    if(not(UserClubs.objects.filter(user = new_user, club = apply_club).exists())):
        club_user = UserClubs(user = new_user, club = apply_club)
        club_user.save()
    return redirect('club_list')

@login_required
@officer_required
def application_list(request, club_name):
    apply_club = Club.objects.get(name = club_name)
    users = UserClubs.objects.filter(club = apply_club, is_member = False)
    return render(request, 'application_list.html', {'users': users, 'club_name':club_name})

@login_required
@officer_required
def approve_application(request, club_name, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
        #club_name = user.club.name
    except ObjectDoesNotExist:
        return redirect('my_clubs')
    else:
        user.is_member=True
        user.save()
        return redirect('application_list', club_name=club_name)

@login_required
@owner_required
def owner_commands(request, club_name):
    selected_club = Club.objects.get(name = club_name)
    members = UserClubs.objects.all().filter(club = selected_club).filter(is_member=True).exclude(user = request.user)
    return (render(request, 'owner_commands.html',{'members':members, 'selected_club': selected_club} ))

@login_required
@owner_required
def promote_member(request, club_name, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('owner_commands', club_name = club_name)
    else:
        user.is_officer=True
        user.save()
        return redirect('owner_commands', club_name = club_name)

@login_required
@owner_required
def demote_officer(request, club_name, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('owner_commands', club_name = club_name)
    else:
        user.is_officer=False
        user.save()
        return redirect('owner_commands', club_name = club_name)

@login_required
@owner_required
def transfer_ownership(request, club_name, user_id):
    try:
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('club_home', club_name = club_name)
    else:
        selected_club = Club.objects.get(name = club_name)
        owner_user = UserClubs.objects.get(user=request.user, club = selected_club)
        owner_user.is_owner = False
        owner_user.save()
        user.is_officer=True
        user.is_owner=True
        user.save()
        return redirect('club_home', club_name = club_name)

def log_out(request):
    logout(request)
    return redirect('home')

"""
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def show_user(request, user_id):
    users = get_user_model().objects.get(id=user_id)
    return render(request, 'show_user.html', {'users': users})
"""
