from django.shortcuts import render
from django.utils import timezone
from .models import Job, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    jobs = Job.objects.filter().order_by('created_date')
    return render(request, 'joblist.html', {'jobs': jobs})

@login_required
def about(request):
    return render(request, 'about.html', {})

@login_required
def profilePage(request):
    profile = Profile.objects.filter(user=request.user)
    if not profile:
        profile = Profile(user=request.user)
        profile.age = 0
        profile.save()
    else:
        profile = profile[0]

    return render(request, 'profile.html', {'profile':profile})

@login_required
def profileEdit(request):
    if request.method == "POST":
        profile = Profile.objects.filter(user=request.user)[0]
        # profile = Profile(user=request.user)
        profile.age = int(request.POST['age'])
        #newprofile.role = request.POST['role']
        profile.contact = request.POST['contact']
        profile.location = request.POST['location']
        profile.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/job/list')

@login_required
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
            return render(request, 'registeration/register.html', {})

        