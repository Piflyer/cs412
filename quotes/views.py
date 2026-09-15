from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.

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
    '''shows all the quotes, makes it a zipped dictionary where we split by key/item'''

    zipped_dict = dict(zip(Quotes, Images))

    context = {
        'zipped_dict': zipped_dict,
    }
    
    return render(request, 'quotes/view_all.html', context)

def about(request):
    '''about page on peter thiel'''
    

    return render(request, 'quotes/about.html')
