from django.shortcuts import render
import random
# Create your views here.

def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    
    
    daily_specials= [
        {
            'name': "Chip Shortage",
            'price': 4.99,
            'desc': "Extra yummy chips that will definitely leave you with shortage when paired with our not-quite-queso-queso dip.",
            'option': [],
        },
        {
            'name': "Stackoverflow Nachos",
            'price': 14.99,
            'desc': "Our take on a nacho tower, paired with our house-made chips and organic ground beef. You'll clear the stack, guaranteed.",
            'option': [],
        },
        {
            'name': "Hash-table Browns",
            'price': 3.99,
            'desc': "Our take on a hash brown, except faster and better",
            'option': [],
        },
    ]

    core_menu = [
        {
            'name': "Spam & Eggs",
            'price': 12.99,
            'desc': "The breakfast you never asked for, yet you see it everywhere.",
            'option': [],
        },
        {
            'name': "Not-a-Bubble Bubble Milkshake",
            'price': 7.99,
            'desc': "We are not in a bubble, but we still made a bubble milkshake.",
            'option': [],
        },
        {
            'name': "Bacon-developer",
            'price': 14.99,
            'desc': "We used some very delicate logic to sizzle and serve this to perfection.",
            'option': [],
        },
        {
            'name': "Localhost Fries",
            'price': 5.99,
            'desc': "No place like 127.0.0.1. And some fries to go with it.",
            'option': [
                {
                    'name': "MegaBite",
                    'price': 0,
                },
                {
                    'name': "GigaBite",
                    'price': 1,
                },
                {
                    'name': "TerraBite",
                    'price': 2,
                },
            ]
        },
        {
            'name': "Bacon-developer",
            'price': 14.99,
            'desc': "We used some very delicate logic to sizzle and serve this to perfection.",
            'option': [],
        },
        {
            'name': "Phish Tacos",
            'price': 12.99,
            'desc': "Looks suspiciously authentic and good, you will get hooked.",
            'option': [],
        },
        {
            'name': "Raspberry Pi",
            'price': 8.99,
            'desc': "Nothing completes a meal like a low cost, bite-sized desert.",
            'option': [],
        },
    ]
    
    context = {
        'special' : random.choice(daily_specials),
        'core_menu' : core_menu
    }

    return render(request, 'restaurant/order.html', context=context)

def submit(request):
    if request.POST:
        name = request.POST['name']
        phone = request.POST

def confirmation(request):
    return render(request, 'restaurant/main.html')