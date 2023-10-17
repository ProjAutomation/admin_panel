from django.shortcuts import render
from datetime import time


def home(request):
    return render(request, 'index.html')


def slots(request):
    context = {
        'slots': [
            {'start': time(hour=9), 'end': time(hour=13)},
            {'start': time(hour=18), 'end': time(hour=21)},
        ]
    }
    return render(request, 'slots.html', context=context)
