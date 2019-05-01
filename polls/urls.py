from django.urls import path, include

from . import views

app_name = 'polls'
urlpatterns = [
    path('all/', views.polls, name='elections'),
    path('create/', views.create_poll, name='create_election'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/add-voter', views.add_voter, name='add_voter'),
    path('<int:voter_id>/remove-voter', views.remove_voter, name='remove_voter'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]
