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
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Profile, Post, Photo, Follow, Like, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import ProfileSerializer, PostSerializer, CommentSerializer, UserSerializer




# Create your views here.
class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''Custom Mixin for self.request user and login url'''
    def get_login_url(self) -> str:
        # move to login url
        return reverse('login')
    def get_profile(self):
        # get the user
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
        if post.profile != curUser:
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
        # get context behind who is following add return that
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
    def get_queryset(self):
        '''Only allow the logged-in user's own posts'''
        return Post.objects.filter(profile=self.get_profile())

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
    
    def get_queryset(self):
        '''Only allow the logged-in user's own posts'''
        return Post.objects.filter(profile=self.get_profile())

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
    '''Return profile view'''
    def get_object(self):
        return self.get_profile()

def get_viewer_profile(request):
    '''Return the Profile named by ?viewer=<id>, or 404.'''
    return get_object_or_404(Profile, pk=request.query_params.get('viewer'))


class ProfileListAPIView(generics.ListAPIView):
    '''
    API view to return a listing of all Profiles.
    Optional ?search=<text> matches username, display name, or bio.
    '''
    serializer_class = ProfileSerializer

    def get_queryset(self):
        '''Return all profiles, filtered by ?search= if given.'''
        profiles = Profile.objects.all().order_by('username')
        query = self.request.query_params.get('search')
        if query:
            profiles = profiles.filter(
                Q(username__icontains=query) |
                Q(display_name__icontains=query) |
                Q(bio_text__icontains=query))
        return profiles


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    '''API view to return (GET) or update (PATCH) one Profile by pk.'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfilePostsAPIView(generics.ListAPIView):
    '''API view to return all Posts (with photos) for one Profile.'''
    serializer_class = PostSerializer

    def get_queryset(self):
        '''Return posts for the profile in the URL.'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.get_all_posts()


class ProfileFeedAPIView(generics.ListAPIView):
    '''API view to return the feed for one Profile.'''
    serializer_class = PostSerializer

    def get_queryset(self):
        '''Return posts from the profiles this profile follows.'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.get_post_feed()


class FollowersAPIView(generics.ListAPIView):
    '''API view to return the profiles that follow one Profile.'''
    serializer_class = ProfileSerializer
    pagination_class = None

    def get_queryset(self):
        '''Return the followers of the profile in the URL.'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.get_followers()


class FollowingAPIView(generics.ListAPIView):
    '''API view to return the profiles one Profile follows.'''
    serializer_class = ProfileSerializer
    pagination_class = None

    def get_queryset(self):
        '''Return the profiles followed by the profile in the URL.'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.get_following()


class FollowAPIView(APIView):
    '''POST to follow, DELETE to unfollow, the Profile in the URL as ?viewer=.'''

    def post(self, request, pk):
        '''The viewer follows this profile (not themselves).'''
        profile = get_object_or_404(Profile, pk=pk)
        viewer = get_viewer_profile(request)
        if viewer == profile:
            return Response({'detail': "You can't follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.get_or_create(profile=profile, follower_profile=viewer)
        return Response(ProfileSerializer(profile, context={'request': request}).data)

    def delete(self, request, pk):
        '''The viewer unfollows this profile.'''
        profile = get_object_or_404(Profile, pk=pk)
        viewer = get_viewer_profile(request)
        Follow.objects.filter(profile=profile, follower_profile=viewer).delete()
        return Response(ProfileSerializer(profile, context={'request': request}).data)


class PostListCreateAPIView(generics.ListCreateAPIView):
    '''
    API view to list all Posts (GET) and create a Post (POST).
    Optional ?search=<text> matches the caption.
    '''
    serializer_class = PostSerializer

    def get_queryset(self):
        '''Return all posts, filtered by ?search= if given.'''
        posts = Post.objects.all().order_by('-timestamp')
        query = self.request.query_params.get('search')
        if query:
            posts = posts.filter(caption__icontains=query)
        return posts


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view to return (GET), edit the caption (PATCH), or delete (DELETE) one Post.'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeAPIView(APIView):
    '''POST to like, DELETE to unlike, the Post in the URL as ?viewer=.'''

    def post(self, request, pk):
        '''The viewer likes this post (not their own, same as the web version).'''
        post = get_object_or_404(Post, pk=pk)
        viewer = get_viewer_profile(request)
        if post.profile == viewer:
            return Response({'detail': "You can't like your own post."},
                            status=status.HTTP_400_BAD_REQUEST)
        Like.objects.get_or_create(post=post, profile=viewer)
        return Response(PostSerializer(post, context={'request': request}).data)

    def delete(self, request, pk):
        '''The viewer unlikes this post.'''
        post = get_object_or_404(Post, pk=pk)
        viewer = get_viewer_profile(request)
        Like.objects.filter(post=post, profile=viewer).delete()
        return Response(PostSerializer(post, context={'request': request}).data)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    '''API view to list (GET) or add (POST) Comments on the Post in the URL.'''
    serializer_class = CommentSerializer
    pagination_class = None

    def get_queryset(self):
        '''Return the comments on this post, oldest first.'''
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post).order_by('timestamp')

    def perform_create(self, serializer):
        '''Attach the new comment to the post in the URL.'''
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(post=post)

class UserRegistrationView(generics.CreateAPIView):
    ''' Register a User'''
    serializer_class = UserSerializer

class UserLoginView(APIView):
    '''User Login view sign in process'''
    def post(self, request):
        '''Validate user View'''
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)  # Authenticate the user
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)  # Create or retrieve a token for the user
            profile = Profile.objects.filter(user=user).first()
            return Response({
                            'token': token.key,
                            'user_id': user.id,
                            'username': user.username,
                            'profile_id': profile.id if profile else None,
                        }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

