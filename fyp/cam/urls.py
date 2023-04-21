from django.urls import path

from cam import views
from django.conf.urls.static import static
from django.conf import settings

appName = 'cam'

urlpatterns = [
    path('', views.index, name='index'),

    path('signup/', views.signup, name='signup'),

    path('home/', views.home, name='home'),

    path('submit_crime_report/', views.submit_crime_report,
         name='submit_crime_report'),

    path('login/', views.login, name='login'),

    # path('logout/', views.logout_view, name='logout'),

    path ( 'complain/', views.complainForm, name= 'complain_form'),

    path ( 'user/', views.UserPage, name='user_page' )
]
