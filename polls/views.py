import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django import forms
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from polls.forms import SignUpForm, EditProfileForm, CreateElectionForm, AddVoterForm
from polls.models import Poll, Option, Voter, Vote


def index(request):
    return render(request, 'polls/index.html')


@login_required
def dashboard(request):
    total = Poll.objects.all().order_by('-created_at').count()
    pending = Poll.objects.filter(status=Poll.CREATED).order_by('-created_at').count()
    active = Poll.objects.filter(status=Poll.ACTIVE).order_by('-created_at').count()
    finished = Poll.objects.filter(status=Poll.FINISHED).order_by('-created_at').count()

    return render(request, 'polls/dashboard.html', {
        'total': total,
        'active': active,
        'pending': pending,
        'finished': finished
    })


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
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/election_detail.html', {
        'poll': poll
    })


@login_required
def add_voter(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if request.method == 'POST':
        form = AddVoterForm(request.POST)
        if form.is_valid():
            old_voter = poll.voter_set.filter(email=form.cleaned_data.get('email')).count()
            if old_voter <= 0:
                voter = Voter()
                voter.name = form.cleaned_data.get('name')
                voter.email = form.cleaned_data.get('email')
                voter.access_token = uuid.uuid4()
                voter.poll = poll
                voter.save()

                link = request.build_absolute_uri('/')[:-1]
                link = link + reverse('polls:vote', kwargs={'access_token': voter.access_token})

                send_mail('Voter Invitation',
                          'Hello, '+str(voter.name)+"\n\n"
                          'You have been invited to take part in the following election by voting:\n\n'
                                +poll.name+'\n\n'
                          'To do so, please follow the link provided: '+link+' \n\n'
                          'regards, Groot Team.',
                          'Groot Vote <noreply@groot.com>',
                          ['lehone4hope@gmail.com'])

            return redirect('/polls/'+str(poll_id)+'/?voter=true')
    else:
        return redirect('polls:detail', poll_id)


@login_required
def remove_voter(request, voter_id):
    voter = Voter.objects.get(pk=voter_id)
    poll = voter.poll
    if voter:
        for vote in voter.vote_set.all():
            option = vote.option
            option.votes = option.votes - 1
            option.save()
            vote.delete()
        voter.delete()

    return redirect('/polls/' + str(poll.id) + '/?voter=true')


def vote(request, access_token):
    try:
        voter = Voter.objects.get(access_token=access_token)
        poll = voter.poll
        if voter.vote_set.count() > 0 and poll.status == 'Active':
            return redirect('polls:vote_thanks', voter.id)

        return render(request, 'polls/vote.html', {
            'voter': voter,
            'poll': poll
        })
    except ObjectDoesNotExist:
        raise Http404


def cast_vote(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
    except ObjectDoesNotExist:
        return Http404

    if request.method == 'POST':
        poll = voter.poll

        candidate_ids = request.POST.getlist('candidate[]')
        if candidate_ids:
            for c_id in candidate_ids:
                try:
                    candidate = Option.objects.get(pk=c_id)
                    vote1 = Vote()
                    vote1.voter = voter
                    vote1.poll = poll
                    vote1.option_id = candidate.id
                    vote1.save()

                    candidate.votes = candidate.votes + 1
                    candidate.save()
                except ObjectDoesNotExist:
                    print('An error occurred')
        return redirect('polls:vote_thanks', voter_id)
    else:
        return Http404


def vote_thanks(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
    except ObjectDoesNotExist:
        voter = None

    return render(request, 'polls/vote_thanks.html', {
        'voter': voter
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
            candidates_bio = request.POST.getlist('candidate_bio[]')
            if candidates:
                for i in range(len(candidates)):
                    option = Option()
                    option.name = candidates[i]
                    option.description = candidates_bio[i] if candidates_bio[i] else ''
                    option.poll = poll
                    option.save()

            return redirect('polls:detail', poll.id)
    else:
        form = CreateElectionForm()
    return render(request, 'polls/create_election.html', {'form': form})


@login_required
def edit_poll(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except ObjectDoesNotExist:
        return Http404

    if request.method == 'POST':
        form = CreateElectionForm(request.POST)
        if form.is_valid():
            poll.name = form.cleaned_data.get('name')
            poll.description = form.cleaned_data.get('description')
            poll.max_votes = form.cleaned_data.get('max_votes')
            poll.start = form.cleaned_data.get('start_date')
            poll.expiration = form.cleaned_data.get('end_date')
            poll.save()

            for candidate in poll.option_set.all():
                candidate.delete()

            candidates = request.POST.getlist('candidate[]')
            if candidates:
                for candidate in candidates:
                    option = Option()
                    option.name = candidate
                    option.poll = poll
                    option.save()

            return redirect('polls:detail', poll.id)
    else:
        form = CreateElectionForm()
    return render(request, 'polls/edit_election.html', {
        'form': form,
        'poll': poll
    })


@login_required
def open_poll(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except ObjectDoesNotExist:
        return Http404

    poll.status = 'Active'
    poll.save()
    return redirect('polls:detail', poll_id)


@login_required
def close_poll(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except ObjectDoesNotExist:
        return Http404

    poll.status = 'Finished'
    poll.save()
    return redirect('polls:detail', poll_id)


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
