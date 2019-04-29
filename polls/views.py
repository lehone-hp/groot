from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from polls.forms import SignUpForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:dashboard'))
    else:
        return HttpResponseRedirect(reverse('login'))


def dashboard(request):
    return render(request, 'polls/dashboard.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('polls:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'polls/signup.html', {'form': form})
