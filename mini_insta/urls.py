"""
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : URLs management for mini_insta
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView, ShowFeedView, SearchView, MyProfileView

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
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
]

