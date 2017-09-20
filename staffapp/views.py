from django.shortcuts import render
from django.utils import timezone
from .models import Job
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    jobs = Job.objects.filter().order_by('created_date')
    return render(request, 'joblist.html', {'jobs': jobs})

def profilePage(request):
    user = request.user
    return render(request, 'profile.html', {})

def joblistPage(request):
    jobs = Job.objects.filter().order_by('created_date')
    return render(request, 'joblist.html', {'jobs': jobs})

@login_required
def jobpostPage(request):
    return render(request, 'jobpost.html', {})

@login_required
def jobNewPost(request):
    if request.method == "POST":
        newjob = Job(writer=request.user)
        newjob.email = request.POST['email']
        newjob.title = request.POST['title']
        newjob.description = request.POST['description']
        newjob.save()

        return HttpResponseRedirect('/job/list')
                    
        
def registerPage(request):
    if request.method == 'GET':
        return render(request, 'registeration/register.html', {})
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            User.objects.create_user(username, email, password)
            user = authenticate(username = username, password = password)
            login(request, user)     
            return HttpResponseRedirect('/profile')
        else:
            return render(request, 'registeration/register.html', {});

        