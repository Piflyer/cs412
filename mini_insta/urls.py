"""
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : URLs management for mini_insta
"""
from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
]

