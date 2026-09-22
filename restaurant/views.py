from django.shortcuts import render
import random
from datetime import datetime
# Create your views here.

DAILY_SPECIALS= [
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

CORE_MENU = [
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


def main(request):
    '''Renders the homepage'''
    return render(request, 'restaurant/main.html')

def order(request):
    '''Handles the order page by randomly choosing a daily special and showing the all the core menu items'''
    context = {
        'special' : random.choice(DAILY_SPECIALS),
        'core_menu' : CORE_MENU
    }

    return render(request, 'restaurant/order.html', context=context)

def confirmation(request):
    '''Handles confirmation logic by first coming up with an estimated order time and than handling the requests'''
    total_cost = 0
    context = {}
    items_ordered = []
    ordertime = random.randint(30, 60)
    hour = datetime.now().hour + 1
    minute = datetime.now().minute + ordertime
    if minute > 59:
        hour += 1
        minute -= 60
        hour = hour % 12
    readyTime = f'{hour}:{minute}'
    # checks if POSt request is made and starts filtering it down
    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        card = request.POST['card']
        special_instructions = request.POST['instructions']
        # goes through each of the core menu items request
        for items in request.POST.getlist('core'):
            item = CORE_MENU[int(items)]
            items_ordered.append(item)
            total_cost += item['price']
            option = request.POST.get(f'option_{int(items)}')
            #checks if any options was selected
            if option:
                opt = item['option'][int(option)]
                items_ordered.append({
                    'name': item['option'][int(option)]['name'],
                    'price': item['option'][int(option)]['price'],
                })
                total_cost += item['option'][int(option)]['price']
        #checks for daily specials
        if request.POST['special']:
            for order in DAILY_SPECIALS:
                if request.POST['special'] == order['price']:
                    items_ordered += order
                    total_cost += order['price']
        #wraps up as a context to be sent to the confirmation page
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'total_cost': total_cost,
            'items_ordered': items_ordered,
            'readytime': readyTime,
            'card': card[-4:],
        }
    return render(request, 'restaurant/confirmation.html', context=context)