from django.shortcuts import render
from django.core.management.utils import get_random_secret_key
from django.http import HttpResponse


print(get_random_secret_key())


def index(request):
    return render(request, 'index.html')


def about(request):
    return HttpResponse('Hello, World!')
