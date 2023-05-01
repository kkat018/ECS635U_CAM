from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as authlogin, logout
from .models import Location, Notification, Crime
from .forms import SignupForm

# Create your views here.

def index(request) -> HttpResponse:
    """
    Initial index url path will route here
    """
    return redirect('login')


User = get_user_model()

def signup(request):
    if request.user.is_authenticated:
        return redirect('http://localhost/8000/cam/home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')

            password = form.cleaned_data['password1']

            new_user = User.objects.create(name=name)

            new_user.set_password(password)
            new_user.phone_number = phone_number
            new_user.email = email
            new_user.save()
            return redirect('http://localhost:8000/cam/login/')

    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})


@csrf_exempt
def login(request):
    print("he")
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        user_check = User.objects.filter(name=name)
        # print(name, password, email)
        # user = auth.authenticate(username=name, password=password)
        # user = authenticate(request, name=name, password=password)
        user = User.objects.filter(name=name).first()
        print(user, user_check)
        if user is not None:
            auth_user = authenticate(
                request, username=user.username, password=password)
            print("hel0", auth_user)
            if auth_user is not None:
                print("hel")
                check = auth.login(request, user) #login is renamed to authlogin
                # request.session['logged_in'] = True
                
            # authlogin(request, user)
            return redirect('http://localhost:8000/cam/home/')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'auth/login.html')

# @login_required
def home(request):
    request.user = User.objects.filter(name='bella')[0]
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'crime london',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 12,
        'apiKey': '7136729da47947eab1aa1ef4ff411f66'
    }
    print("home page user: ", request.user)
    # Send GET request to API
    response = requests.get(url, params=params)

    unread_notifications, read_notifications = [], []
    # Parse response JSON and extract articles
    articles = response.json().get('articles', [])
    print("noti check:", Notification.objects.filter(user_id=request.user,
                                                     is_read=False).first().complaint.complaint)
    if Notification.objects.filter(user_id=request.user):
        unread_notifications = Notification.objects.filter(user_id=request.user,
                                                           is_read=False)
        read_notifications = Notification.objects.filter(
            user_id=request.user, is_read=True)
    
    context = {'articles': articles ,
               "unread_notifications": unread_notifications,
               "read_notifications": read_notifications}
    # context = {'articles': articles}

    return render(request, 'pages/home.html', context)

def complainForm(request):
    request.user = User.objects.filter(name='User2')[0]
    response = requests.get(
        'https://api.os.uk/search/names/v1/find?key=CQrAclSYxs54aCSAaxybZGxx8wyryjQC&query=london&maxresults=100')
    
    locations = []
    if response.ok:
        # places = response.json()['results']
        data = response.json()
        results = data.get('results', [])
        places = [result['GAZETTEER_ENTRY'] for result in results]
        
        for result in data['results']:
            name = result['GAZETTEER_ENTRY']['DISTRICT_BOROUGH']
            # print(name)
            if name not in locations:
                locations.append(name)

           # create Location objects and save to database
        for location in locations:
        #     Location.objects.create(name=location)
            try:
                location = Location.objects.filter(name=location)

            except Location.DoesNotExist:
                # Create a new location with the given name
                location = Location.objects.create(name=location)
            
    context = {'places': places}
    
    return render(request, 'pages/complain.html', context)
    

@csrf_exempt
def submit_crime_report(request):
    request.user = User.objects.filter(name='User2').first()
    print("location ", request.POST)
    if request.method == 'POST':
        reporter_id = request.user
        datetime = request.POST['date']
        location = Location.objects.filter(name = request.POST['location']).first()
        complaint = request.POST['complaint']

        new_crime = Crime(reporter_id=reporter_id, datetime=datetime,
                        location=location, complaint=complaint)
        new_crime.save()
        print("new crime: ", new_crime)
        # messages.success(request, "Complaint submitted!")
        # user_locations = User.User.objects.filter(name='User2').first().to_dict()
        user_locations = User.objects.all()
        for user in user_locations:
            if user.location.filter(name=location.name):
                print("user check: ", user)
                Notification.objects.create(
                    user_id=user, complaint=new_crime, is_read=False)

        # create a notification for each user

            # unread_count = Notification.objects.filter(is_read=False).count()
        return redirect('http://localhost:8000/cam/home')
    else:
        messages.error(request, "Try again!")
        return redirect('http://localhost/8000/cam/complainForm')
        
    return HttpResponse()


def mark_notification_as_read(request, notification_id):
    # Get the notification object
    notification = Notification.objects.get(id=notification_id)

    # Mark the notification as read
    notification.is_read = True
    notification.save()

    # Redirect the user to the URL they were on before
    return redirect('http://localhost:8000/cam/home')

def UserPage(request):
    request.user = User.objects.filter(name='bella')[0]
    response = requests.get(
        'https://api.os.uk/search/names/v1/find?key=CQrAclSYxs54aCSAaxybZGxx8wyryjQC&query=london&maxresults=100')

    if response.ok:
        # places = response.json()['results']
        data = response.json()
        results = data.get('results', [])
        places = [result['GAZETTEER_ENTRY'] for result in results]
    user_locations = User.objects.all()
    for user in user_locations:
        if user.location.filter(name='Camden'):
            print("user check: ", user)
    # print("user location: ", user_locations.location.filter(name='Camden'))
    locations = request.user.location
    user = request.user.name
    # print("user  ", user)
    # print("Loc \n", Location.objects.all())
    # print("hello ", locations)
    return render(request, 'pages/user.html', {'places': places})


@csrf_exempt
def save_location(request):
    request.user = User.objects.filter(name='bella').first()
    if request.method == 'POST':
        print("what isss: \n", request.POST)
        location_name = request.POST.get('location')
        if location_name:
            # for locat in Location.objects.all():
            #     print("loc\n", locat.name)
            print("just checking, ", location_name)
            location = Location.objects.filter(name=location_name).first()
            print("come in\n " , location)
            # user = request.user
            # check = request.user.is_authenticated
            # print("user  ",user)
            request.user.location.add(location)
            request.user.save()
        else:
            print(f"{location_name} does not exist.")
    else:
        print("Location field is empty.")
        
    return redirect('http://localhost:8000/cam/user')


def logout_view(request):
    logout(request)
    return redirect('login')
