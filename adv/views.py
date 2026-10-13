from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q

# Create your views here.

#------> User Creation
def user_register(request):
    if request.method == "POST":
        form_data = UserForm(request.POST)
        if form_data.is_valid():
            user = form_data.save()
            if user:
                login(request, user)
                messages.success(request, "User loged in successfully")
                return redirect("profile")
            
    form_data = UserForm()
    con = {
        "data" : form_data,
        "title" : "register",
        "btn" : "Register"
    }
    return render(request, 'form.html', con)



def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        form_data = AuthenticationForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request, user)
                messages.success(request, "User loged in")
                return redirect('profile')
            
    form_data = AuthenticationForm()
    con = {
        "data" : form_data,
        "title" : "user login",
        "btn" : "Login",
        "registe_page" : True
    }
    return render(request, 'form.html', con)



@login_required
def user_logout(request):
    logout(request)

    return redirect("login_page")




def dashboard(request):

    con = {
        "title" : "dashboard"
    }
    return render(request, 'dashboard.html', con)



#----->User profile view

@login_required
def profile_view(request):

    return render(request, 'profile.html')


@login_required
def update_profile(request):
    if request.user.user_type == "Recruiter":

        form_data = RecruiterForm()
        if request.method == 'POST':
            form_data = RecruiterForm(request.POST)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.user = request.user
                data.save()
                messages.success(request, "profole updated")
                return redirect('profile')
            
    con = {
        "data" : form_data,
        "title" : "profile update",
        "btn" : "Update"
    }
    return render(request, 'form.html', con)




#------>job View

def job_display(request):
    if request.user.is_authenticated:
        if request.user.user_type == "Recruiter":
            jobs = JobModel.objects.select_related('recruiter__user').filter(recruiter__user = request.user).order_by('-id').prefetch_related('applications')
        else:
            jobs = JobModel.objects.select_related('recruiter__user')
    else:
        jobs = JobModel.objects.select_related('recruiter__user')

    keyword = request.GET.get('q', '').strip()
    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    

    con = {
        "data" : jobs,
        "keyword" : keyword,
        'title' : 'display jobs'
    }
    return render(request, 'jobs.html', con)



#-----------------------------------------------------------------------------------------
"""
How do you check how many SQL queries are being executed?
"""

# from django.db import connection, reset_queries
# from django.conf import settings

# settings.DEBUG = True

# def job_display(request):
#     reset_queries()
#     jobs = JobModel.objects.select_related('recruiter__user')

#     for job in jobs:
#         print(f'{job.title}, {job.recruiter.address}, {job.recruiter.user.username}')

#     print(f"Total Queries:, {len(connection.queries)}")

#     con = {
#         "data" : jobs,
#         'title' : 'display jobs'
#     }
#     return render(request, 'jobs.html', con)


"""
Here:
    - reset_queries() — Clears the record of previous queries.
    - connection.queries — A list of SQL queries recorded in debug mode.
    - len(connection.queries) — Counts the number of recorded queries.
"""
#-----------------------------------------------------------------------------------------



@login_required
def create_job(request):
    recruiter = getattr(request.user, 'recruiter', None)

    if not recruiter or not recruiter.is_profile_complete:
        messages.warning(request, 'Please complete your recruiter profile first.')
        return redirect('profile')

    if request.method == "POST":
        form_data = JobForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.recruiter = request.user.recruiter
            data.save()
            messages.success(request, 'job created')
            return redirect('jobs')

    form_data = JobForm()
    con = {
        "data" : form_data,
        "title" : "create job",
        "btn" : 'Create'
    }
    return render(request, 'form.html', con)




def job_application(request, a_id):
    if not request.user.user_type == 'Seeker':
        messages.success(request, "You can't apply")
        return redirect('jobs')
    
    job = JobModel.objects.get(id = a_id)
    if request.method == "POST":
        form_data = JobApplyForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.job = job
            data.applicant = request.user
            data.save()
            messages.success(request, 'Apply successfully')
            return redirect('jobs')
        
    form_data = JobApplyForm()
    con = {
        'data' : form_data,
        'title' : 'Apply',
        'btn' : 'Apply'
    }
    return render(request, 'form.html', con)




def candidate_view(request, c_id):
    application = get_object_or_404(JobModel, id = c_id)
    candidate = ApplicationModel.objects.filter(job = application).select_related('applicant')

    con = {
        'data' : candidate,
        'title' : 'candidata'
    }
    return render(request, "candidate.html", con)