from django import forms
from .models import UserProfile
from  movies.models import Genre
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
class CustomUserCreationForm(UserCreationForm):
    GENRE_CHOICE = [
        ('Adventure', 'Adventure'),
        ('Fantasy', 'Fantasy'),
          ('Animation', 'Animation'),
          ('Drama', 'Drama'),
          ('Horror', 'Horror'),
          ('Action', 'Action'),
          ('Comedy', 'Comedy'),
          ('History', 'History'),
          ('Western', 'Western'),
          ('Thriller', 'Thriller'),
          ('Crime', 'Crime'),
          ('Documentary', 'Documentary'),
          ('Science Fiction', 'Science Fiction'),
          ('Mystery', 'Mystery'),
          ('Music', 'Music'),
          ('Romance', 'Romance'),
          ('Family', 'Family'),
          ('War', 'War'),
          ('TV Movie', 'TV Movie'),
        ]
    favorite = forms.ChoiceField(
        label="Favorite Movie Genre",
        help_text="Choose your favorite genre. We'll recommend movies based on your choice.",
        choices=GENRE_CHOICE
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'favorite')
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email', 'favorite']
        
class UserProfileForm(forms.ModelForm):   
    class Meta:
        model = UserProfile
        fields = '__all__'

# class UserProfileForm(forms.ModelForm):
#     favorites = forms.ModelMultipleChoiceField(queryset=Genre.objects.all().values_list('name',flat=True ),
#                                                 widget=forms.CheckboxSelectMultiple,
#                                                 label='',)
#     class Meta:
#         model = UserProfile
#         fields = ['favorites']
