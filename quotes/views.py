from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.

Quotes = [
    "I got something I want to talk about - Madonna",
    "Competition is for losers - Peter Thiel",
    "My goal is YC - Every larper out there"
]

Images = [
    "https://pics.freeartbackgrounds.com/midle/Nature_Landscape_Background-223.jpg",
    "https://pics.freeartbackgrounds.com/midle/Azure_Blue_Sea_Background-775.jpg",
    "https://pics.freeartbackgrounds.com/midle/Eiffel_Tower_at_Night_Paris_Background-1289.jpg",
]

def quote(request):
    '''renders the quotes in a random fashion, goes through a list of images and quotes and randomly picks them'''

    
    context = {
        'quote': random.choice(Quotes),
        'image': random.choice(Images),
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    '''shows all the quotes'''

    zipped_dict = dict(zip(Quotes, Images))

    context = {
        'zipped_dict': zipped_dict,
    }
    
    return render(request, 'quotes/view_all.html', context)

def about(request):
    '''about page'''
    
    response_text = '''
    <html>
    <h1>About</h1>
    </html>
    '''
    return HttpResponse(response_text)
