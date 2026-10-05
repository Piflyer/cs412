'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Manager for showing all profiles and individual profiles
'''

from django.shortcuts import render
from .models import Profile, Posts, Photo
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreatePostForm
from django.urls import reverse



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

class CreatePostView(CreateView):
    '''Create a new post for a profile'''
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def form_valid(self, form):
        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")
        # get PK from URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        response = super().form_valid(form)
        #Image URL is seperate, create it with the correspodning post
        image_url = form.cleaned_data.get('image_url')
        if image_url:
            Photo.objects.create(posts=self.object, image_url=image_url)

        return response

    
    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk':pk})