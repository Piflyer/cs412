'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Managing backend connections with a custom Jokes and picture model for user data and attribute for mock joke app
'''
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Jokes(models.Model):
    '''
    Jokes Class for storing all the jokes and its applicable attributes
    '''
    jokes = models.TextField(blank=False)
    contributor  = models.TextField(blank=False)
    timestamp = models.DateTimeField(blank=False)

class Picture(models.Model):
    '''
    Picture Class for storing the pictures
    '''
    image_url = models.URLField(blank=False)
    timestamp = models.DateTimeField(blank=False)
    contributor = models.TextField(blank=False)


    