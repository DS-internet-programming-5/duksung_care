# forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        if 'content' in self.fields:
            self.fields['content'].label = False

    class Meta:
        model = Comment
        fields = ('text',)
