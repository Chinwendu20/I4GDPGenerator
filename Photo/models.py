from django.db import models
from django.db import models
from django.conf import settings
from authentication.models import User
from cloudinary.models import CloudinaryField
import uuid
from django.contrib.sessions.models import Session


# Create your models here.
# class authUser(models.Model):
# 	username=models.CharField( max_length=200)
# 	password=models.CharField( max_length=128)
# 	email=models.EmailField( blank=False)
# 	first_name=models.CharField( max_length=200)
# 	last_name=models.CharField( max_length=200)

class Post(models.Model):
	user=models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	Banner=CloudinaryField('Banner')
	Link = models.SlugField(max_length = 250, null = False, blank = False)
	Height=models.IntegerField()
	Width=models.IntegerField()
	Position_x=models.IntegerField()
	Position_y=models.IntegerField()
	Border_radius=models.IntegerField(blank=True, null=True)
	Name=models.CharField( max_length=200)
	Description=models.CharField( max_length=200)
	session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
	


