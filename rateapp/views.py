from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404
from .models import Project,Profile, Review
from django.contrib.auth.decorators import login_required
from .forms import NewProjectForm, ProfileForm, ReviewForm
from django.contrib.auth.models import User
from django.db.models import Avg

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
  projects = Project.get_projects()
  return render(request,'index.html',{"projects":projects})

def search_results(request):

  if 'project' in request.GET and request.GET["project"]:
    search_term = request.GET.get("project")
    searched_projects = Project.search_by_title(search_term)
    message = f"{search_term}"

    return render(request, 'search.html',{"message":message,"projects": searched_projects})

  else:
    message = "You haven't searched for any term"
    return render(request, 'search.html',{"message":message})

def project(request, id):
  if request.user.is_authenticated:
    user = User.objects.get(username = request.user)
  project = Project.objects.get(id = id)
  reviews = Review.objects.filter(project = project)
  design = reviews.aggregate(Avg('design'))['design__avg']
  usability = reviews.aggregate(Avg('usability'))['usability__avg']
  content = reviews.aggregate(Avg('content'))['content__avg']
  average = reviews.aggregate(Avg('average'))['average__avg']
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
      review = form.save(commit=False)
      review.average = (review.design + review.usability + review.content) / 3
      review.project = project
      review.user = user
      review.save()
      return redirect('project', id)
  else:
    form = ReviewForm()
  return render(request, 'profile.html', {'project': project, 'reviews': reviews, 'form': form, 'design': design, 'usability': usability, 'content': content, 'average': average})

@login_required(login_url='/accounts/login/')
def new_project(request):
  current_user = request.user
  if request.method == 'POST':
    form = NewProjectForm(request.POST, request.FILES)
    if form.is_valid():
       project = form.save(commit=False)
       project.profile = current_user
       project.save()
    return redirect('index')

  else:
    form = NewProjectForm()
  return render(request, 'new_project.html', {"form": form})

@login_required(login_url='/accounts/login/')
def profile(request, username):
  title = "Profile"
  profile = User.objects.get(username=username)
  users = User.objects.get(username=username)

  try :
    profile_details = Profile.get_by_id(profile.id)
  except:
    profile_details = Profile.filter_by_id(profile.id)

  projects = Project.get_profile_projects(profile.id)
  return render(request, 'profile.html', {'title':title,'profile':profile, 'profile_details':profile_details, 'projects':projects})

@login_required(login_url='/accounts/login/')
def edit_profile(request):
  title = 'Edit Profile'
  profile = User.objects.get(username=request.user)
  try:
    profile_details = Profile.get_by_id(profile.id)
  except:
    profile_details = Profile.filter_by_id(profile.id)
    
  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES)
    if form.is_valid():
      edit = form.save(commit=False)
      edit.user = request.user
      edit.save()
    return redirect('profile', username=request.user)
  else:
    form = ProfileForm()
    
  return render(request, 'editprofile.html', {'form':form, 'profile_details':profile_details})
