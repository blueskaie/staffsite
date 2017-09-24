from django.shortcuts import render
from django.utils import timezone
from .models import Job, Profile, Requestjob
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
import smtplib

from django.conf import settings
from django.core.files.storage import FileSystemStorage
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
        uploaded_file_url = ''
        if 'photo' in request.FILES:
            myfile = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name,myfile)
            uploaded_file_url = fs.url(filename)
        profile = Profile.objects.filter(user=request.user)[0]
        # profile = Profile(user=request.user)
        profile.age = int(request.POST['age'])
        #newprofile.role = request.POST['role']
        profile.contact = request.POST['contact']
        profile.location = request.POST['location']
        if uploaded_file_url != '':
            profile.path = uploaded_file_url
        profile.save()
        return render(request, 'profile.html', {'profile': profile})
    else:
        return HttpResponseRedirect('/job/list')

@login_required
def joblistPage(request):
    jobs = Job.objects.filter().order_by('created_date')
    return render(request, 'joblist.html', {'jobs': jobs})

@login_required
def jobpostPage(request):
    if 'job_id' in request.GET:
        jobid = int(request.GET['job_id'])
        job = Job.objects.filter(id=jobid)[0]
        return render(request, 'jobpost.html', {'job': job})
    return render(request, 'jobpost.html', {})

@login_required
def jobNewPost(request):
    if request.method == "POST":
        if request.POST['jobid']:
            jobid = int(request.POST['jobid'])
            newjob = Job.objects.filter(id=jobid)[0]
            newjob.title = request.POST['title']
            newjob.location = request.POST['location']
            newjob.description = request.POST['description']
            if request.POST['start_time']:
                newjob.start_time = request.POST['start_time']
            if request.POST['end_time']:
                newjob.end_time = request.POST['end_time']
            newjob.save()
        else: 
            newjob = Job(writer=request.user)
            newjob.title = request.POST['title']
            newjob.location = request.POST['location']
            newjob.description = request.POST['description']
            if request.POST['start_time']:
                newjob.start_time = request.POST['start_time']
            if request.POST['end_time']:
                newjob.end_time = request.POST['end_time']
            newjob.save()
        return HttpResponseRedirect('/job/list')

@login_required                   
def jobDeletePost(request):
    if request.method == "POST":
        jobid = request.POST['job_id']
        job = Job.objects.get(id=jobid)
        job.delete()
        return JsonResponse({'result': 'true'})

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

@login_required
def requestJob(request):
    if request.method == 'POST':
        jobid = int(request.POST['job_id'])
        job = Job.objects.filter(id=jobid)
        if (not job):
            return JsonResponse({'result': false})
        newReqjob = Requestjob(user=request.user, job=job[0])
        newReqjob.save()
        return JsonResponse({'result': newReqjob.id})
    else:
        requestjobs = Requestjob.objects.filter(user=request.user)
        return render(request, 'requestjoblist.html', {'requestjobs': requestjobs})

@login_required
def requestJobProcess(request):
    if request.method == 'POST':
        request_id = int(request.POST['request_id'])
        mode = request.POST['mode']
        requestjob = Requestjob.objects.filter(id=request_id)[0]
        to_email = requestjob.user.email
        if mode == 'true':
            requestjob.status = 'AC'
        else:
            requestjob.status = 'DE'
        # gmail_user = 'sabrinallbani83@gmail.com'
        # server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
        # server.login(gmail_user, 'victory1983')
        # server.sendmail(gmail_user, gmail_user, 'thanks')
        
        content = 'Your Request ' + str(requestjob.id) + ' is processed!'

        to_email = requestjob.user.email
        try:
            send_mail(
                'Wild Fork Team',
                content,
                'sabrinallbani83@gmail.com',
                [to_email],
                fail_silently=False,
            )
        except:
            return JsonResponse({'result': 'false'})

        requestjob.save()
        return JsonResponse({'result': requestjob.id})      
    else:
        will_requests = Requestjob.objects.filter(status='WT')
        did_requests = Requestjob.objects.filter(~Q(status='WT'))
        return render(request, 'requestprocess.html', {'will_requests': will_requests, 'did_requests': did_requests})


def adminJobList(request):
    jobs = Job.objects.filter().order_by('created_date')
    return render(request, 'adminjoblist.html', {'jobs': jobs})