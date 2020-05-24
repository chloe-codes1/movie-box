# movies/forms.py
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=100,
        label='Comment Create',
        help_text='Your comment must be no more than 100 characters in length',
        widget=forms.TextInput(
            attrs={
                'class':'input-sm',
                'placeholder': "What do you think about this movie?"
            }
        )
    )
    class Meta:
        model = Comment
        fields = ['content']