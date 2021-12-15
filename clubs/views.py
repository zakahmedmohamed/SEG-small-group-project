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

"""Redirect URL if you are logged in"""
def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect('my_clubs')
        else:
            return view_function(request)
    return modified_view_function

"""Redirect URL if you are not an owner"""
def owner_required(view_function):
    def modified_view_function(request, club_name, **kwargs):
        selected_club = Club.objects.get(name = club_name)
        owner_user = UserClubs.objects.get(user=request.user, club = selected_club)
        if not owner_user.is_owner:
            return redirect('club_list')
        else:
            return view_function(request, club_name, **kwargs)
    return modified_view_function

"""Redirect URL if you are not an officer"""
def officer_required(view_function):
    def modified_view_function(request, club_name, **kwargs):
        selected_club = Club.objects.get(name = club_name)
        owner_user = UserClubs.objects.get(user=request.user, club = selected_club)
        if not owner_user.is_officer:
            return redirect('club_list')
        else:
            return view_function(request, club_name, **kwargs)
    return modified_view_function

"""Redirect URL if you are not a member"""
def member_required(view_function):
    def modified_view_function(request, club_name, **kwargs):
        selected_club = Club.objects.get(name = club_name)
        member_user = UserClubs.objects.filter(user=request.user, club = selected_club)
        if not member_user.exists() or not member_user.get().is_member:
            return redirect('my_clubs')
        else:
            return view_function(request, club_name, **kwargs)
    return modified_view_function

"""View for the sign up page"""
def sign_up(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('my_clubs')

        messages.add_message(request, messages.ERROR, "Details provided are incorrect")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

"""View to change profile"""
@login_required
def change_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('my_clubs')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'change_profile.html', {'form': form})

"""View tp change password"""
@login_required
def change_password(request):
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
    return render(request, 'change_password.html', {'form': form})

"""View to create a club"""
@login_required
def create_club(request):
    if request.method =='POST':
        form = Create_A_Club_Form(request.POST)
        if form.is_valid():
            newClub = form.save()
            request.user.make_club_owner(newClub)
            return redirect('my_clubs')
    else:
        form = Create_A_Club_Form()
    return render(request, 'create_club.html', {'form': form})

"""View to see home page"""
@login_prohibited
def home(request):
    return render(request, 'home.html')

"""View to see a club home page"""
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
    return render(request, 'club_home.html', {'clubs': clubs, 'club': club_name, 'clubUser': club_user})

"""View to log in"""
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

"""View for the club list page"""
@login_required
def club_list(request):
    all_clubs = Club.objects.filter().order_by()
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True)
    clubIDs = joined_clubs.values_list('club')
    my_clubs = Club.objects.filter(id__in = clubIDs)
    owner_dict = {}
    for c in all_clubs:
        owner_dict[c] = UserClubs.objects.all().get(club = c, is_owner = True)
    return render(request, 'club_list.html', {'all_clubs':all_clubs, 'owners':owner_dict, 'clubs':my_clubs})

"""View for the my clubs page"""
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

"""View for the members list"""
@login_required
@member_required
def view_members(request,club_name):

    selected_club = Club.objects.get(name = club_name)
    members = UserClubs.objects.all().filter(club = selected_club).filter(is_member=True).exclude(user = request.user)
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True)
    clubIDs = joined_clubs.values_list('club')
    clubs = Club.objects.filter(id__in = clubIDs)
    current_user = UserClubs.objects.all().get(user = request.user,club = selected_club)
    return (render(request, 'view_members.html',{'members':members, 'selected_club': selected_club, 'clubs':clubs, 'current_user': current_user} ))

"""View for the club profile page"""
@login_required
def club_profile(request,club_name):
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True)
    clubIDs = joined_clubs.values_list('club')
    clubs = Club.objects.filter(id__in = clubIDs)
    try:
        currentClub = Club.objects.get(name = club_name)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        memberSize = UserClubs.objects.all().filter(club = currentClub, is_member = True).count()
        owner = UserClubs.objects.all().get(club = currentClub, is_owner = True)
        have_applied = UserClubs.objects.all().filter(club = currentClub, user = request.user).exists()
        return (render(request, 'club_profile.html', {'club':currentClub, 'memberSize': memberSize, 'owner': owner, 'have_applied': have_applied, 'clubs':clubs}))

"""View to apply for a club"""
@login_required
def club_application(request, club_name):
    try:
        new_user = request.user
        apply_club = Club.objects.get(name = club_name)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        if(not(UserClubs.objects.filter(user = new_user, club = apply_club).exists())):
            new_user.apply_club(apply_club)
            #club_user = UserClubs(user = new_user, club = apply_club)
            #club_user.save()
        return redirect('club_list')

"""View for list of club applications"""
@login_required
@officer_required
def application_list(request, club_name):
    apply_club = Club.objects.get(name = club_name)
    users = UserClubs.objects.filter(club = apply_club, is_member = False)
    joined_clubs = UserClubs.objects.all().filter(user = request.user, is_member = True)
    clubIDs = joined_clubs.values_list('club')
    clubs = Club.objects.filter(id__in = clubIDs)
    return render(request, 'application_list.html', {'users': users, 'club_name':club_name, 'clubs':clubs})

"""View to approve a application"""
@login_required
@officer_required
def approve_application(request, club_name, user_id):
    try:
        club = Club.objects.get(name = club_name)
        officer = UserClubs.objects.get(user = request.user, club = club)
        user = UserClubs.objects.get(id=user_id)
        #club_name = user.club.name
    except ObjectDoesNotExist:
        return redirect('my_clubs')
    else:
        officer.approve_application(user)
        return redirect('application_list', club_name=club_name)

"""View to remove a application"""
@login_required
@officer_required
def reject_application(request, club_name, user_id):
    try:
        club = Club.objects.get(name = club_name)
        officer = UserClubs.objects.get(user = request.user, club = club)
        user = UserClubs.objects.get(id=user_id)
        #club_name = user.club.name
    except ObjectDoesNotExist:
        return redirect('my_clubs')
    else:
        officer.reject_application(user)
        return redirect('application_list', club_name=club_name)


"""View to promote a member"""
@login_required
@owner_required
def promote_member(request, club_name, user_id):
    try:
        club = Club.objects.get(name = club_name)
        owner = UserClubs.objects.get(user = request.user, club = club)
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('view_members', club_name = club_name)
    else:
        owner.promote_member(user)
        return redirect('view_members', club_name = club_name)

"""View to demote an officer"""
@login_required
@owner_required
def demote_officer(request, club_name, user_id):
    try:
        club = Club.objects.get(name = club_name)
        owner = UserClubs.objects.get(user = request.user, club = club)
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('view_members', club_name = club_name)
    else:
        owner.demote_officer(user)
        return redirect('view_members', club_name = club_name)

"""View to transfer ownership to another member"""
@login_required
@owner_required
def transfer_ownership(request, club_name, user_id):
    try:
        club = Club.objects.get(name = club_name)
        owner = UserClubs.objects.get(user=request.user, club = club)
        user = UserClubs.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('club_home', club_name = club_name)
    else:
        owner.transfer_ownership(user)
        return redirect('club_home', club_name = club_name)

"""View to log out"""
def log_out(request):
    logout(request)
    return redirect('home')