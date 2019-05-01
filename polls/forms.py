from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)


class CreateElectionForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(max_length=5000, required=True)
    start_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    end_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    max_votes = forms.IntegerField()


class AddVoterForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    email = forms.CharField(max_length=5000, required=True)
