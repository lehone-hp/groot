from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from polls.forms import SignUpForm, EditProfileForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:dashboard'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
def dashboard(request):
    return render(request, 'polls/dashboard.html')


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST)
        if profile_form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name = profile_form.cleaned_data.get('first_name')
            user.last_name = profile_form.cleaned_data.get('last_name')
            user.save()
            return redirect('polls:profile')
    else:
        profile_form = EditProfileForm()
    return render(request, 'polls/profile.html', {'profile_form': profile_form})


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
