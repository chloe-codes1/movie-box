from django import forms
from .models import UserProfile
from  movies.models import Genre
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email']

class UserProfileForm(forms.ModelForm):
    favorites = forms.ModelMultipleChoiceField(queryset=Genre.objects.all().values_list('name', flat=True),
                                                widget=forms.CheckboxSelectMultiple,
                                                label='',)
    class Meta:
        model = UserProfile
        fields = ['favorites']
