from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#user: id, name, number, email, password, address list,
#address: id, postcode, first line, second line, country, city
#crime: reporter id, evidence?, photo?, video?, time, location, 


class Location(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    name = models.CharField("Name", max_length=50, unique=True)
    number = models.IntegerField ("Number", unique= True, blank = True, null= True)
    email = models.EmailField( "Email", max_length=254 )
    location = models.ManyToManyField(
        Location, max_length=50, default=None, null=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.name,
            'email': self.email,
        }


class Crime(models.Model):
    image = models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=100 , default=None)
    reporter_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reporter', default=None)
    datetime = models.DateTimeField(auto_now_add=False, default=None)
    location = models.TextField("location", max_length=50, default=None)
    complaint = models.TextField("Complain", max_length=1000, default=None)

    def to_dict(self):
        return {
            'id': self.id,
            'reporter_id': self.reporter_id,
            'time': self.time,
            'location': self.location,
        }
