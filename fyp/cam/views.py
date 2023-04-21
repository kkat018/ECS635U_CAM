from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as authlogin

from .models import Crime
from .forms import SignupForm

# Create your views here.


def index(request) -> HttpResponse:
    """
    Initial index url path will route here
    """
    # Change on deployment
    return redirect('signup')


User = get_user_model()
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            authlogin(request, user)
            return redirect('home')
    return render(request, 'auth/login.html')

@login_required
def home(request):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'crime london',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 12,
        'apiKey': '7136729da47947eab1aa1ef4ff411f66'  # 7136729da47947eab1aa1ef4ff411f66
    }

    # Send GET request to API
    response = requests.get(url, params=params)

    # Parse response JSON and extract articles
    articles = response.json().get('articles', [])
    return render(request, 'pages/home.html', {'articles': articles})

def complainForm(request):
    response = requests.get(
        'https://api.os.uk/search/names/v1/find?key=CQrAclSYxs54aCSAaxybZGxx8wyryjQC&query=london&maxresults=100')
    
    if response.ok:
        # places = response.json()['results']
        data = response.json()
        results = data.get('results', [])
        places = [result['GAZETTEER_ENTRY'] for result in results]

    else:
        places = "Error"
    context = {'places': places}
    
    return render(request, 'pages/complain.html', context)
    

@csrf_exempt
def submit_crime_report(request):
    print("location ", request.POST)
    if request.method == 'POST':
        reporter_id = request.user
        # reporter_id = 1234
        datetime = request.POST['date']
        location = request.POST['location']
        complaint = request.POST['complaint']

        new_crime = Crime(reporter_id=reporter_id, datetime=datetime,
                        location=location, complaint=complaint)
        new_crime.save()
        messages.success(request, "Complaint submitted!")
        return redirect('home')
    else:
        messages.error(request, "Try again!")
        return redirect('complainForm')
        
    return HttpResponse()
    
def UserPage(request):
    return render(request, 'pages/user.html')


