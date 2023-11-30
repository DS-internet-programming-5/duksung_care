from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # SlugField : 숫자인 pk 대신, 읽을 수 있는 텍스트로 URL을 만들고 싶을 때 주로 사용
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'


class Hospital(models.Model):
    # 카카오맵 REST API response
    place_name = models.CharField(max_length=200)  # 장소이름
    distance = models.IntegerField(blank=True, null=True)  # 중심좌표와의 거리
    place_url = models.URLField(max_length=200)  # 상세 정보 링크 (카카오맵)
    category_name = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    address_name = models.CharField(max_length=200)  # 지번 주소
    road_address_name = models.CharField(max_length=200)  # 도로명 주소
    hospital_id = models.CharField(max_length=50)  # 카카오맵에서의 id
    hospital_phone = models.CharField(max_length=20, null=True)  # 전화번호
    category_group_code = models.CharField(max_length=50)  # HP8 : 병원
    category_group_name = models.CharField(max_length=50)  # 카테고리 이름 (병원, 약국, 음식점 등)
    x = models.DecimalField(max_digits=50, decimal_places=45)  # x좌표, 경도
    y = models.DecimalField(max_digits=50, decimal_places=45)  # y좌표, 위도

    # opening_time = models.TimeField(blank=True, null=True)  # 영업 시작 시간
    # closing_time = models.TimeField(blank=True, null=True)  # 영업 종료 시간
    operation_time = models.TextField(blank=True, null=True)  # 영업 시간 정보
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0,
                                         validators=[MinValueValidator(0), MaxValueValidator(5)])  # 평균별점(0~5)
    num_reviews = models.IntegerField(default=0)  # 리뷰 개수

    has_female_doctor = models.BooleanField(default=False)  # 여성 의사 여부
    has_evening_hours = models.BooleanField(default=False)  # 야간 진료 여부
    has_holiday_hours = models.BooleanField(default=False)  # 휴일 진료 여부
    is_partnership = models.BooleanField(default=False)  # 학교 제휴 여부
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_hospitals', blank=True, null=True)  # 북마크한 유저들

    def __str__(self):
        return f'[{self.pk}] {self.place_name}'

    def get_absolute_url(self):
        return f'/hospital/{self.pk}/'


class Review(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    content = models.TextField()  # 리뷰 내용
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # 리뷰 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일
    likes = models.ManyToManyField(User, related_name='like_reviews', null=True)  # 리뷰 좋아요
    num_likes = models.IntegerField(default=0)  # 리뷰 좋아요 개수
    hospital_rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])  # 별점(0~5)
