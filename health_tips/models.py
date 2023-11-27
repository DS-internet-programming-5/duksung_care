from django.db import models
from accounts.models import User

# Create your models here.
class Post(models.Model):
    post_title = models.CharField(max_length=30) # 글 제목
    post_content = models.TextField() # 글 내용
    created_at = models.DateTimeField(auto_now_add=True) # 작성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일
    head_image = models.ImageField(upload_to='health/imgs/%Y/%m/%d/', blank=True) # 필요시 추가
    file_upload = models.FileField(upload_to='health/files/%Y/%m/%d/', blank=True) # 파일
    post_author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # 작성자 : 관리자만 쓸 수 있도록 하기
    likes = models.ManyToManyField(User, related_name='like_post') # 좋아요
    hits = models.PositiveIntegerField(default=0) # 조회수

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/health/{self.pk}/'
