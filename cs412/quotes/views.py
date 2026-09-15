from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def quote(request):
    '''renders the quotes in a random fashion'''
    
    response_text = '''
    <html>
    <h1>Quote!</h1>
    </html>
    '''
    return HttpResponse(response_text)

def show_all(request):
    '''shows all the quotes'''
    
    response_text = '''
    <html>
    <h1>All Quotes</h1>
    </html>
    '''
    return HttpResponse(response_text)

def about(request):
    '''about page'''
    
    response_text = '''
    <html>
    <h1>About</h1>
    </html>
    '''
    return HttpResponse(response_text)
