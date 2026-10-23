'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Manager for showing all profiles and individual profiles
'''

from typing import Any
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from .models import Profile, Post, Photo, Follow, Like
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''Custom Mixin for self.request user and login url'''
    def get_login_url(self) -> str:
        return reverse('login')
    def get_profile(self):
        return Profile.objects.filter(user=self.request.user).first()

class FollowView(CustomLoginRequiredMixin, TemplateView):
    '''Logged in user can follow another profile'''
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        curUser = self.get_profile()
        following = Profile.objects.get(pk=self.kwargs['pk'])
        if curUser != following:
            Follow.objects.get_or_create(profile=following, follower_profile=curUser)
        return redirect('show_profile', pk=following.pk)

class DeleteFollowView(CustomLoginRequiredMixin, TemplateView):
    '''Logged in user can unfollow another profile'''
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        curUser = self.get_profile()
        following = Profile.objects.get(pk=self.kwargs['pk'])
        Follow.objects.filter(profile=following, follower_profile=curUser).delete()
        return redirect('show_profile', pk=following.pk)

class LikeView(CustomLoginRequiredMixin, TemplateView):
    '''Logged in user can like another profile'''
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        curUser = self.get_profile()
        post = Post.objects.get(pk=self.kwargs['pk'])
        Like.objects.get_or_create(post=post, profile=curUser)
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('post', pk=post.pk)


class DeleteLikeView(CustomLoginRequiredMixin, TemplateView):
    '''Logged in user can unlike another profile'''
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        curUser = self.get_profile()
        post = Post.objects.get(pk=self.kwargs['pk'])
        Like.objects.filter(post=post, profile=curUser).delete()
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('post', pk=post.pk)


class CreateProfileView(CreateView):
    '''Create a new account'''
    template_name = 'mini_insta/create_profile_form.html'
    form_class = CreateProfileForm
    def get_context_data(self, **kwargs):
        #get new form input context
        context = super().get_context_data(**kwargs)
        context['form_input'] = UserCreationForm()
        return context
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        #save form
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).first()
            context['is_following'] = Follow.objects.filter(
                profile=self.object, follower_profile=me).exists()
        return context


class PostDetailView(DetailView):
    '''show each indivual post seperately'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs):
        # get like objects
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).first()
            context['has_liked'] = Like.objects.filter(
                post=self.object, profile=me).exists()
        return context

class CreatePostView(CustomLoginRequiredMixin, CreateView):
    '''Create a new post for a profile'''
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get profile data
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

    def form_valid(self, form):
        # get PK from URL
        user = self.get_profile()
        form.instance.profile = user
        response = super().form_valid(form)
        #Image URL is seperate, create it with the correspodning post
        # image_file = self.request.POST.get('image_file')
        image_file = self.request.FILES.getlist('image_file')
        for image in image_file:
            Photo(post=self.object, image_file=image).save()

        return response

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
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
        user = self.request.user
        form.instance.profile = user
        return super().form_valid(form)
    
    def get_object(self):
        return self.get_profile()
class UpdatePostView(CustomLoginRequiredMixin, UpdateView):
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


class DeletePostView(CustomLoginRequiredMixin, DeleteView):
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

class ShowFeedView(CustomLoginRequiredMixin, DetailView):
    '''show each users personalized feed'''
    model = Profile
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"

    def get_object(self):
        '''Get profile'''
        return self.get_profile()

    def get_context_data(self, **kwargs):
        '''Get context data to add in for likes'''
        context = super().get_context_data(**kwargs)
        context['liked_ids'] = Like.objects.filter(
            profile=self.get_profile()).values_list('post_id', flat=True)
        return context


class SearchView(CustomLoginRequiredMixin, ListView):
    '''Shows search results'''
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"
    
    def dispatch(self, request, *args, **kwargs):
        '''show serach form if no query was made'''
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if 'query' not in self.request.GET:
            '''get profile we are saerching'''
            profile = self.get_profile()
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
        profile = self.get_profile()
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

class MyProfileView(CustomLoginRequiredMixin, ProfileDetailView):
    def get_object(self):
        return self.get_profile()


