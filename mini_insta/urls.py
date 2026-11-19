"""
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : URLs management for mini_insta
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView, ShowFeedView, SearchView, MyProfileView, CreateProfileView, FollowView, DeleteFollowView, LikeView, DeleteLikeView, ProfileListAPIView, ProfileDetailAPIView, ProfilePostsAPIView, ProfileFeedAPIView, PostListCreateAPIView, PostDetailAPIView, FollowersAPIView, FollowingAPIView, FollowAPIView, LikeAPIView, CommentListCreateAPIView, UserRegistrationView, UserLoginView
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/', MyProfileView.as_view(), name='show_my_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(),name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(),name="show_following"),
    path('profile/feed', ShowFeedView.as_view(), name="show_feed"),
    path('profile/search', SearchView.as_view(), name="search"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html', next_page='show_feed'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_insta/logged_out.html'), name='logout'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/follow', FollowView.as_view(), name='follow'),
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name='delete_follow'),
    path('post/<int:pk>/like', LikeView.as_view(), name='like'),
    path('post/<int:pk>/delete_like', DeleteLikeView.as_view(), name='delete_like'),
    path('api/profiles', ProfileListAPIView.as_view(), name='api_profiles'),
    path('api/profile/<int:pk>', ProfileDetailAPIView.as_view(), name='api_profile'),
    path('api/profile/<int:pk>/posts', ProfilePostsAPIView.as_view(), name='api_profile_posts'),
    path('api/profile/<int:pk>/feed', ProfileFeedAPIView.as_view(), name='api_feed'),
    path('api/posts', PostListCreateAPIView.as_view(), name='api_posts'),
    path('api/post/<int:pk>', PostDetailAPIView.as_view(), name='api_post'),
    path('api/profile/<int:pk>/followers', FollowersAPIView.as_view(), name='api_followers'),
    path('api/profile/<int:pk>/following', FollowingAPIView.as_view(), name='api_following'),
    path('api/profile/<int:pk>/follow', FollowAPIView.as_view(), name='api_follow'),
    path('api/post/<int:pk>/like', LikeAPIView.as_view(), name='api_like'),
    path('api/post/<int:pk>/comments', CommentListCreateAPIView.as_view(), name='api_comments'),
    path('api/register', UserRegistrationView.as_view(), name='register'),
    path('api/login', UserLoginView.as_view(), name='login'),
]

