'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Manager for showing all profiles and individual profiles
'''

from typing import Any

from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from .models import Profile, Post, Photo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse



# Create your views here.

class ProfileListView(ListView):
    '''Show all the available Profiles'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Show each of the available Profiles'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    '''show each indivual post seperately'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    '''Create a new post for a profile'''
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        # get PK from URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        response = super().form_valid(form)
        #Image URL is seperate, create it with the correspodning post
        # image_file = self.request.POST.get('image_file')
        image_file = self.request.FILES.getlist('image_file')
        for image in image_file:
            Photo(post=self.object, image_file=image).save()

        return response

class UpdateProfileView(UpdateView):
    '''
    Handles profile Updates
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Validate our updated profile
        '''
        return super().form_valid(form)

class UpdatePostView(UpdateView):
    '''
    Handles profile Updates
    '''
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    
    def form_valid(self, form):
        '''
        Validate our updated profile
        '''
        response = super().form_valid(form)
        for image in self.request.FILES.getlist('image_file'):
            Photo(post=self.object, image_file=image).save()
        return response


class DeletePostView(DeleteView):
    '''A view to delete a post and remove it from the database.'''
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Provide the post and the profile that made it to the template.'''
        context = super().get_context_data(**kwargs)

        # get the pk for this post
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)

        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        '''Return the URL to redirect to after the delete.'''

        # get the pk for this post
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)

        # find the profile to which this Post is related by FK
        profile = post.profile

        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk': profile.pk})

class ShowFollowersDetailView(DetailView):
    '''Show all the Followers'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    '''Show all the Following'''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class ShowFeedView(DetailView):
    '''show each users personalized feed'''
    model = Profile
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"

class SearchView(ListView):
    '''Shows search results'''
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"
    
    def dispatch(self, request, *args, **kwargs):
        '''show serach form if no query was made'''
        if 'query' not in self.request.GET:
            '''get profile we are saerching'''
            pk = self.kwargs.get("pk")
            profile = Profile.objects.get(pk=pk)
            return render(request, "mini_insta/search.html", {'profile': profile})
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        '''return posts with matching captions'''
        query = self.request.GET.get("query")
        posts = Post.objects.filter(caption__contains=query).order_by("-timestamp")
        return posts
    def get_context_data(self, **kwargs):
        '''Add profile and query to context data'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        profile = Profile.objects.get(pk=pk)
        query = self.request.GET.get("query")
        
        username = Profile.objects.filter(username__contains=query)
        display_name = Profile.objects.filter(display_name__contains=query)
        bio = Profile.objects.filter(bio_text__contains=query)
        
        profiles = []
        for p in list(username) + list(display_name) + list(bio):
            if p not in profiles:
                profiles.append(p)
        context['profile'] = profile
        context['query'] = query
        context['posts'] = self.get_queryset()
        context['profiles'] = profiles
        return context



