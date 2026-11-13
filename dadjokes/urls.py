"""
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : URLs management for mini_insta
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', RandomJokes.as_view(), name="index"),
    path('random', RandomJokes.as_view(), name="random"),
    path('jokes', ManyJokes.as_view(), name="jokes"),
    path('joke/<int:pk>', SingleJoke.as_view(), name="joke"),
    path('pictures', ManyPhoto.as_view(), name="pictures"),
    path('picture/<int:pk>', SinglePhoto.as_view(), name="picture"),
    path('api/', RandomJokeAPIView.as_view(), name="api_index"),
    path('api/random', RandomJokeAPIView.as_view(), name="api_random"),
    path('api/jokes', JokeListAPIView.as_view(), name="api_jokes"),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name="api_joke"),
    path('api/pictures', PictureListAPIView.as_view(), name="api_pictures"),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name="api_picture"),
    path('api/random_picture', RandomPictureAPIView.as_view(), name="api_random_picture"),
]



