from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from polls.forms import SignUpForm, EditProfileForm, CreateElectionForm
from polls.models import Poll, Option


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:dashboard'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
def dashboard(request):
    return render(request, 'polls/dashboard.html')


@login_required
def polls(request):
    total = Poll.objects.all().order_by('-created_at')
    pending = Poll.objects.filter(status=Poll.CREATED).order_by('-created_at')
    active = Poll.objects.filter(status=Poll.ACTIVE).order_by('-created_at')
    finished = Poll.objects.filter(status=Poll.FINISHED).order_by('-created_at')

    return render(request, 'polls/elections.html', {
        'total': total,
        'active': active,
        'pending': pending,
        'finished': finished
    })


@login_required
def create_poll(request):
    if request.method == 'POST':
        form = CreateElectionForm(request.POST)
        if form.is_valid():
            poll = Poll()
            poll.user = request.user
            poll.name = form.cleaned_data.get('name')
            poll.description = form.cleaned_data.get('description')
            poll.max_votes = form.cleaned_data.get('max_votes')
            poll.start = form.cleaned_data.get('start_date')
            poll.expiration = form.cleaned_data.get('end_date')
            poll.save()

            candidates = request.POST.getlist('candidate[]')
            if candidates:
                for candidate in candidates:
                    option = Option()
                    option.name = candidate
                    option.poll = poll
                    option.save()

            return redirect('polls:elections')
    else:
        form = CreateElectionForm()
    return render(request, 'polls/create_election.html', {'form': form})


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
        password_form = PasswordChangeForm(request.user)
    return render(request, 'polls/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('polls:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, 'polls/profile.html', {
            'profile_form': EditProfileForm(),
            'password_form': password_form
        })
    else:
        return redirect('polls:profile')


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
