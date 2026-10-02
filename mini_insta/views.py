'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Manager for showing all profiles and individual profiles
'''

from django.shortcuts import render
from .models import Profile, Posts
from django.views.generic import ListView, DetailView


# Create your views here.

class ProfileListView(ListView):
    '''Show all the available Profiles'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profile"

class ProfileDetailView(DetailView):
    '''Show each of the available Profiles'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    '''show each indivual post seperately'''
    model = Posts
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"