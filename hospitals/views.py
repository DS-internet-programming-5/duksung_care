from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Hospital, Review, Category
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views import View
from django.db.models import Q


class HospitalList(ListView):  # 병원 목록
    model = Hospital
    context_object_name = 'hospital_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hospitals = context['hospital_list']
        categories = Category.objects.all()  # 카테고리 데이터 가져오기

        # 페이지네이션
        page = self.request.GET.get('page')
        paginator = Paginator(hospitals, 10)
        page_obj = paginator.page(page)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_obj = paginator.page(page)

        # 현재 페이지를 중심으로 최대 5개의 페이지를 보여줌
        num_pages = paginator.num_pages
        current_page = page_obj.number
        if num_pages <= 5:
            custom_range = range(1, num_pages + 1)
        else:
            if current_page <= 3:
                custom_range = range(1, 6)
            elif current_page + 2 >= num_pages:
                custom_range = range(num_pages - 4, num_pages + 1)
            else:
                custom_range = range(current_page - 2, current_page + 3)

        context['hospital_list'] = hospitals
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['custom_range'] = custom_range
        context['categories'] = categories  # 카테고리 데이터 추가
        return context

    def get_queryset(self):
        order_condition = self.request.GET.get('order', None)
        filter_condition = self.request.GET.get('filter', None)
        bookmark_condition = self.request.GET.get('bookmark', None)
        hospitals = super().get_queryset()

        # 북마크
        if bookmark_condition == 'true':  # 북마크 필터링 추가
            user = self.request.user
            hospitals = hospitals.filter(bookmarks=user)

        # 상세설정
        if filter_condition:
            filters = filter_condition.split(',')
            for condition in filters:
                if condition == 'has_female_doctor':
                    hospitals = hospitals.filter(has_female_doctor=True)
                elif condition == 'has_evening_hours':
                    hospitals = hospitals.filter(has_evening_hours=True)
                elif condition == 'has_holiday_hours':
                    hospitals = hospitals.filter(has_holiday_hours=True)
                elif condition == 'is_partnership':
                    hospitals = hospitals.filter(is_partnership=True)
                elif condition == 'bookmark':  # 북마크 필터링 추가
                    user = self.request.user
                    hospitals = hospitals.filter(bookmarks=user)

        # 정렬
        if order_condition == 'distance':  # 거리 가까운 순
            hospitals = hospitals.order_by('distance')
        elif order_condition == 'rating':  # 별점 많은 순
            hospitals = hospitals.order_by('-average_rating')
        elif order_condition == 'review':  # 리뷰 많은 순
            hospitals = hospitals.annotate(review_count=Count('review')).order_by('-review_count')

        # 검색어
        search_query = self.request.GET.get('search_query', None)
        if search_query:
            # 병원 이름 또는 후기 내용에서 검색
            hospitals = hospitals.filter(
                Q(place_name__icontains=search_query) | Q(review__content__icontains=search_query)
            ).distinct()

        return hospitals


# 카테고리
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        hospitals = Hospital.objects.filter(category_name=None)
    else:
        category = get_object_or_404(Category, slug=slug)
        hospitals = Hospital.objects.filter(category_name=category)

    # 북마크
    bookmark_condition = request.GET.get('bookmark', None)
    if bookmark_condition == 'true':  # 북마크 필터링 추가
        user = request.user
        hospitals = hospitals.filter(bookmarks=user)

    # 상세설정
    filter_condition = request.GET.get('filter', None)
    if filter_condition:
        filters = filter_condition.split(',')
        for condition in filters:
            if condition == 'has_female_doctor':
                hospitals = hospitals.filter(has_female_doctor=True)
            elif condition == 'has_evening_hours':
                hospitals = hospitals.filter(has_evening_hours=True)
            elif condition == 'has_holiday_hours':
                hospitals = hospitals.filter(has_holiday_hours=True)
            elif condition == 'is_partnership':
                hospitals = hospitals.filter(is_partnership=True)

    # 정렬
    order_condition = request.GET.get('order', None)
    if order_condition == 'distance':  # 거리 가까운 순
        hospitals = hospitals.order_by('distance')
    elif order_condition == 'rating':  # 별점 많은 순
        hospitals = hospitals.order_by('-average_rating')
    elif order_condition == 'review':  # 리뷰 많은 순
        hospitals = hospitals.annotate(review_count=Count('review')).order_by('-review_count')

    paginator = Paginator(hospitals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    custom_range = get_custom_range(page_obj, paginator)

    return render(
        request,
        'hospitals/hospital_list.html',
        {
            'page_obj': page_obj,
            'categories': Category.objects.all(),
            'no_categories_hospital_count': Hospital.objects.filter(category_name=None).count(),
            'category': category,
            'paginator': paginator,
            'custom_range': custom_range,
        }
    )


def get_custom_range(page_obj, paginator):
    num_pages = paginator.num_pages
    current_page = page_obj.number

    if num_pages <= 5:
        return range(1, num_pages + 1)
    else:
        if current_page <= 3:
            return range(1, 6)
        elif current_page + 2 >= num_pages:
            return range(num_pages - 4, num_pages + 1)
        else:
            return range(current_page - 2, current_page + 3)


def hospital_detail(request, pk):  # 병원 상세정보
    hospital = get_object_or_404(Hospital, pk=pk)
    review_list = Review.objects.filter(hospital=pk).order_by('-created_at')  # 최신리뷰순으로 정렬

    review_form = ReviewForm()

    return render(request, 'hospitals/hospital_detail.html',
                  {'hospital': hospital, 'review_list': review_list, 'review_form': review_form})


def get_hospital_list(request):
    # Hospital 모델에서 필요한 데이터를 쿼리하여 JSON으로 직렬화
    hospital_list = list(Hospital.objects.values('pk', 'x', 'y','place_name'))

    # JSON 응답 반환
    return JsonResponse(hospital_list, safe=False)


# 리뷰 작성 (추가)
@login_required
def new_review(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        filled_form = ReviewForm(request.POST)
        if filled_form.is_valid():
            # 로그인된 사용자인지 확인
            if request.user.is_authenticated:
                finished_form = filled_form.save(commit=False)
                finished_form.hospital = get_object_or_404(Hospital, pk=pk)
                finished_form.author = request.user  # 인증된 사용자로 리뷰 작성자 설정
                finished_form.created_at = timezone.localtime(timezone.now())
                finished_form.save()

                # 새로 추가된 리뷰의 내용을 가져와서 JSON 응답
                new_review = {
                    'review_pk': finished_form.pk,
                    'content': finished_form.content,
                    'hospital_pk': finished_form.hospital.pk,
                    'hospital_rating': finished_form.hospital_rating,
                    'average_rating': finished_form.hospital.average_rating,
                    'nickname': finished_form.author.nickname,
                    'profileImg': finished_form.author.profileImg.url if finished_form.author.profileImg else None,
                    'created_at': finished_form.created_at.strftime('%Y.%m.%d. %H:%M'),
                    'likes': list(finished_form.likes.values()),
                    'num_likes': finished_form.num_likes,
                    'num_reviews': finished_form.hospital.num_reviews,
                    'author_pk': finished_form.author.pk,
                    'is_superuser': request.user.is_superuser,
                    'user_pk': request.user.pk if request.user.is_authenticated else None,
                }
                return JsonResponse(new_review)
            else:
                # 사용자가 인증되지 않은 경우 에러 메시지를 JSON으로 반환
                return JsonResponse({'error': 'User is not authenticated'}, status=403)
        else:
            # 폼이 유효하지 않은 경우 에러 메시지를 JSON으로 반환
            errors = filled_form.errors.as_json()
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# 리뷰 수정
class UpdateReview(View):
    def post(self, request, review_pk):  # review_pk로 변경
        review_instance = get_object_or_404(Review, pk=review_pk)
        filled_form = ReviewForm(request.POST, instance=review_instance)

        if filled_form.is_valid():
            updated_review = filled_form.save(commit=False)
            updated_review.updated_at = timezone.localtime(timezone.now())
            updated_review.save()

            updated_data = {
                'review_pk': updated_review.pk,
                'content': updated_review.content,
                'hospital_pk': updated_review.hospital.pk,
                'hospital_rating': updated_review.hospital_rating,
                'average_rating': updated_review.hospital.average_rating,
                'num_reviews': updated_review.hospital.num_reviews,
                'nickname': updated_review.author.nickname,
                'profileImg': updated_review.author.profileImg.url if updated_review.author.profileImg else None,
                'updated_at': updated_review.updated_at.strftime('%Y.%m.%d. %H:%M'),
            }
            return JsonResponse(updated_data)
        else:
            errors = filled_form.errors.as_json()
            return JsonResponse({'error': 'Form is not valid'}, status=400)


# 리뷰 삭제
@login_required
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    hospital = review.hospital

    if request.method == 'POST':
        review.delete()
        # 해당 병원의 평균 별점 다시 계산
        average_rating = hospital.average_rating
        num_reviews = hospital.num_reviews
        hospital_pk = hospital.pk

        return JsonResponse(
            {'message': 'Review deleted successfully', 'average_rating': average_rating, 'num_reviews': num_reviews, 'hospital_pk': hospital_pk},
            status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# 리뷰 좋아요
def likes_review(request, review_pk):
    if request.method == 'POST' and request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if user in review.likes.all():
            review.likes.remove(user)
            liked = False
        else:
            review.likes.add(user)
            liked = True

        # 좋아요를 추가 또는 제거할 때마다 해당 리뷰의 좋아요 수를 업데이트
        review.num_likes = review.likes.count()
        review.save()

        return JsonResponse({'liked': liked, 'likes': review.num_likes})

    return JsonResponse({}, status=400)


# 북마크
def hospital_bookmark(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        hospital = get_object_or_404(Hospital, pk=pk)
        user = request.user

        if user in hospital.bookmarks.all():
            hospital.bookmarks.remove(user)
            bookmarked = False
        else:
            hospital.bookmarks.add(user)
            bookmarked = True

        return JsonResponse({'bookmarked': bookmarked})

    return JsonResponse({}, status=400)

# 제휴 병원 상세 정보
def partnership_detail(request, hospital_id):
    hospital = get_object_or_404(Hospital, hospital_id=hospital_id, is_partnership=True)
    return render(request, 'hospitals/partnership_detail.html', {'hospital': hospital})