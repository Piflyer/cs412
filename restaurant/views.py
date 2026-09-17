from django.shortcuts import render
import random
# Create your views here.

def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    
    daily_specials = {"Chip Shortage - $4.99" : "Extra yummy chips that will definitely leave you with shortage when paired with our not-quite-queso-queso dip.",
                      "Stackoverflow Nachos - $14.99" : "Our take on a nacho tower, paired with our house-made chips and organic ground beef. You'll clear the stack, guaranteed.",
                      "Hash-table Browns - $3.99": "Our take on a hash brown, except faster and better."}
    
    core_menu = {
        "Spam & Eggs - $12.99" : "The breakfast you never asked for, yet you see it everywhere.",
        "Not-a-Bubble Bubble Milkshake - $7.99" : "We are not in a bubble, but we still made a bubble milkshake.",
        "Bacon-developer - $14.99" : "We used some very delicate logic to sizzle and serve this to perfection.",
        "Localhost Fries - $5.99" : "No place like 127.0.0.1. And some fries to go with it.",
        "Phish Tacos - $12.99" : "Looks suspiciously authentic and good, you will get hooked.",
        "Raspberry Pi - $8.99" : "Nothing completes a meal like a low cost, bite-sized desert."
    }
    
    
    
    return render(request, 'restaurant/main.html')

def confirmation(request):
    return render(request, 'restaurant/main.html')