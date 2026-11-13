'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Admin management page for dadjokes
'''

from django.contrib import admin

# Register your models here.
from .models import Jokes, Picture
admin.site.register(Jokes)
admin.site.register(Picture)
