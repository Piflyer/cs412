'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Managing backend connections with a custom Profile model for user data and attribute for mock Instagram
'''
from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username}, created on {self.join_date}."
