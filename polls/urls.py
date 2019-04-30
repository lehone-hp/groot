from django.urls import path, include

from . import views

app_name = 'polls'
urlpatterns = [
    path('all/', views.polls, name='elections'),
    path('create/', views.create_poll, name='create_election'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]
