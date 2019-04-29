from django.shortcuts import render

# Create your views here.
from django.views import generic


def dashboard(request):
    return render(request, 'polls/dashboard.html')
