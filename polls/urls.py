from django.urls import path, include

from . import views

app_name = 'polls'
urlpatterns = [
    path('all/', views.polls, name='elections'),
    path('create/', views.create_poll, name='create_election'),
    path('edit/<int:poll_id>/', views.edit_poll, name='edit_election'),
    path('open/<int:poll_id>/', views.open_poll, name='open_election'),
    path('close/<int:poll_id>/', views.close_poll, name='close_election'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),

    path('<int:poll_id>/add-voter', views.add_voter, name='add_voter'),
    path('<int:voter_id>/remove-voter', views.remove_voter, name='remove_voter'),
    path('vote/thanks/<int:voter_id>', views.vote_thanks, name='vote_thanks'),
    path('vote/<str:access_token>', views.vote, name='vote'),
    path('cast-vote/<int:voter_id>', views.cast_vote, name='cast_vote'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]
