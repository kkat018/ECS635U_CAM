from django.contrib import admin
from .models import User, Notification, Location, Crime

# Register your models here.
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Crime)
admin.site.register(Notification)
