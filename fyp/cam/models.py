from django.db import models
from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
 

class User(AbstractUser):
    username = None
    name = models.CharField("Name", max_length=50)
    number = models.IntegerField ("Number", blank = True, null= True)
    email = models.EmailField("Email", max_length=254, unique=True)
    location = models.ManyToManyField( Location, max_length=50, default=None, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.name,
            'email': self.email,
            'locations': self.location
        }


class Crime(models.Model):
    reporter_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reporter', default=None)
    datetime = models.DateTimeField(auto_now_add=False, default=None)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, max_length=50, default=None)
    complaint = models.TextField("Complain", max_length=1000, default=None)

    def to_dict(self):
        return {
            'id': self.id,
            'reporter_id': self.reporter_id,
            'time': self.time,
            'location': self.location,
        }

class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    complaint = models.ForeignKey(Crime, on_delete=models.CASCADE)