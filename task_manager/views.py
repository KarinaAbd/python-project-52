from django.shortcuts import render
from django.core.management.utils import get_random_secret_key


print(get_random_secret_key())


def index(request):
    return render(request, 'index.html')
