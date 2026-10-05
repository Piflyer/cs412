'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Managing backend connections with a custom Profile model for user data and attribute for mock Instagram
'''
from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    
    def get_Posts(self):
        posts = Posts.objects.filter(profile=self).order_by('-timestamp')
        return posts
    
    def __str__(self):
        return f"{self.username}, created on {self.join_date}."

class Posts(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def get_Photos(self):
        photos = Photo.objects.filter(posts=self)
        return photos
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f"{self.caption}, created on {self.timestamp}."

class Photo(models.Model):
    posts = models.ForeignKey("Posts", on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
            return f"{self.posts}, created on {self.timestamp}."
