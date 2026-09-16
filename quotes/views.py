# Author: Tim Nguyen (tim7@bu.edu), 9/16/2026
# Description: view functions for the quotes app, which displays quotes and images of Peter Thiel.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random


Quotes = [
    "Moving first is a tactic, not a goal - Peter Thiel",
    "Competition is for losers - Peter Thiel",
    "There's absolutely no bubble in technology - Peter Thiel"
]

Images = [
    "https://www.thenation.com/wp-content/uploads/2026/06/AP26064375929256.jpg",
    "https://fortune.com/img-assets/wp-content/uploads/2024/12/GettyImages-2152107576-e1733614218964.jpg",
    "https://img-cdn.inc.com/image/upload/f_webp,q_auto,c_fit/vip/2024/12/peter-thiel-inc.jpg",
]

def quote(request):
    '''renders the quotes in a random fashion, goes through a list of images and quotes and randomly picks them'''

    
    context = {
        'quote': random.choice(Quotes),
        'image': random.choice(Images),
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    '''shows all the quotes, makes it return two lists and then pulled for the HTML page render'''

    context = {
        'images': Images,
        'quotes': Quotes,
    }
    
    return render(request, 'quotes/show_all.html', context)

def about(request):
    '''about page on peter thiel and tim'''
    

    return render(request, 'quotes/about.html')
