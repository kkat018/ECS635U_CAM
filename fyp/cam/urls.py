from django.urls import path

from cam import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

appName = 'cam'

urlpatterns = [
    path('', views.index, name='index'),

    path('signup/', views.signup, name='signup'),

    path('home/', views.home, name='home'),

    # path('cam/home/', views.home, name='cam_home'),

    path('submit_crime_report/', views.submit_crime_report,
         name='submit_crime_report'),
         
    path('save_location/', views.save_location, name='save_location'),

    path('mark-notification-as-read/<int:notification_id>/',
         views.mark_notification_as_read, name='mark_notification_as_read'),

    path('login/', views.login, name='login'),
    # path('login/', auth_views.LoginView.as_view(
        # template_name='auth/login.html'), name='login'),

    path('logout/', views.logout_view, name='logout'),

    path ( 'complain/', views.complainForm, name= 'complain_form'),

    path ( 'user/', views.UserPage, name='user_page' )
]
