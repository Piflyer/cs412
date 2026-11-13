'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Manager for showing all jokes and picture
'''
from typing import Any

from django.shortcuts import render
from .models import Jokes, Picture
from rest_framework import generics
from .serializers import JokeSerializer, PictureSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView


class SingleJoke(DetailView):
    '''Show a single joke'''
    model = Jokes
    template_name = "dadjokes/joke.html"
    context_object_name = "joke"

class SinglePhoto(DetailView):
    '''Show a single photo'''
    model = Picture
    template_name = "dadjokes/picture.html"
    context_object_name = "picture"

class ManyPhoto(ListView):
    '''Show a list of photos'''
    model = Picture
    template_name = "dadjokes/pictures.html"
    context_object_name = "pictures"

class ManyJokes(ListView):
    '''Show a many jokes'''
    model = Jokes
    template_name = "dadjokes/jokes.html"
    context_object_name = "jokes"

class RandomJokes(TemplateView):
    '''Show random jokes'''
    template_name = "dadjokes/random.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = Jokes.objects.order_by('?').first()
        context['picture'] = Picture.objects.order_by('?').first()
        return context

class JokeListAPIView(generics.ListCreateAPIView):
    '''
    An API view to return a listing of all Jokes (GET)
    and to create a Joke (POST).
    '''
    queryset = Jokes.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    '''An API view to return one Joke by its primary key.'''
    queryset = Jokes.objects.all()
    serializer_class = JokeSerializer


class RandomJokeAPIView(generics.RetrieveAPIView):
    '''An API view to return one Joke selected at random.'''
    serializer_class = JokeSerializer

    def get_object(self):
        '''Return a random Joke instead of looking one up by pk.'''
        return Jokes.objects.order_by('?').first()


class PictureListAPIView(generics.ListAPIView):
    '''An API view to return a listing of all Pictures.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    '''An API view to return one Picture by its primary key.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(generics.RetrieveAPIView):
    '''An API view to return one Picture selected at random.'''
    serializer_class = PictureSerializer

    def get_object(self):
        '''Return a random Picture instead of looking one up by pk.'''
        return Picture.objects.order_by('?').first()