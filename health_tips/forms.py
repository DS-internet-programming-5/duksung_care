# forms.py
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_content',)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_title', 'post_content', 'head_image','is_banner']

        widgets = {
            'post_title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '제목을 입력하세요.'}
            ),
            'post_content': forms.CharField(widget=CKEditorUploadingWidget()),
        }



