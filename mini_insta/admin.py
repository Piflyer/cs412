'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Admin management page for mini_insta
'''

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)