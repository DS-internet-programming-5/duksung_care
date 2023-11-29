from django.db import models
from django.conf import settings
from django.urls import reverse

class Post(models.Model):
    post_title = models.CharField(max_length=30)
    post_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='health/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='health/files/%Y/%m/%d/', blank=True)
    post_author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post', blank=True)
    hits = models.PositiveIntegerField(default=0)

    def increase_hits(self):
        if not hasattr(self, '_likes_increase'):
            self.hits += 1
            self._likes_increase = True
            self.save()

    def __str__(self):
        return f'[{self.pk}] {self.post_title} :: {self.post_author}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}::{self.text}'