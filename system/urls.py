"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('', views.home, name= 'home'),
    path('profile/', views.profile, name='profile'),
    path('password/', views.password, name='password'),
    path('club_home/<club_name>/', views.club_home, name= 'club_home'),
    path('log_in/', views.log_in, name='log_in'),
    path('application_list/<club_name>/', views.application_list, name='application_list'),
    path('approve_application/<club_name>/<int:user_id>', views.approve_application, name='approve_application'),
    path('create_club/', views.create_club, name = 'create_club'),
    path('club_list/', views.club_list, name='club_list'),
    path('my_clubs/', views.my_clubs, name='my_clubs'),
    path('club_profile/<club_name>/', views.club_profile, name ='club_profile'),
    path('club_application/<club_name>/', views.club_application, name ='club_application'),
    path('member_profile/<int:user_id>/', views.member_profile, name ='member_profile'),
    path('view_members/<club_name>/', views.view_members, name ='view_members'),
    path('owner_commands/<club_name>/', views.owner_commands, name ='owner_commands'),
    path('promote_member/<club_name>/<int:user_id>', views.promote_member, name='promote_member'),
    path('demote_officer/<club_name>/<int:user_id>', views.demote_officer, name='demote_officer'),
    path('transfer_ownership/<club_name>/<int:user_id>', views.transfer_ownership, name='transfer_ownership'),
    path('log_out/', views.log_out, name='log_out'),

]
