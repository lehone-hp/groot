from django.urls import path, include

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
