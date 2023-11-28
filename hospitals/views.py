from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Hospital, Review, Category
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views import View

class HospitalList(ListView): # 병원 목록
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

# 카테고리
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        hospitals = Hospital.objects.filter(category_name=None)
    else:
        category = get_object_or_404(Category, slug=slug)
        hospitals = Hospital.objects.filter(category_name=category)

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

def hospital_detail(request, pk): # 병원 상세정보
    hospital = get_object_or_404(Hospital, pk=pk)
    review_list = Review.objects.filter(hospital=pk).order_by('-created_at') # 최신리뷰순으로 정렬

    review_form = ReviewForm()

    return render(request, 'hospitals/hospital_detail.html',
                  {'hospital': hospital, 'review_list': review_list, 'review_form': review_form})

def get_hospital_list(request):
    # Hospital 모델에서 필요한 데이터를 쿼리하여 JSON으로 직렬화
    hospital_list = list(Hospital.objects.values('pk', 'x', 'y'))

    # JSON 응답 반환
    return JsonResponse(hospital_list, safe=False)

# 리뷰 작성 (추가)
def new_review(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        filled_form = ReviewForm(request.POST)
        if filled_form.is_valid():
            finished_form = filled_form.save(commit=False)
            finished_form.hospital = get_object_or_404(Hospital, pk=pk)
            finished_form.author = request.user
            finished_form.created_at = timezone.localtime(timezone.now())
            finished_form.save()

            # 새로 추가된 리뷰의 내용을 가져와서 JSON 응답
            new_review = {
                'review_pk': finished_form.pk,
                'content': finished_form.content,
                'hospital_rating': finished_form.hospital_rating,
                'nickname': finished_form.author.nickname,
                'profileImg' : finished_form.author.profileImg.url if finished_form.author.profileImg else None,
                'created_at': finished_form.created_at.strftime('%Y.%m.%d. %H:%M'),
            }
            return JsonResponse(new_review)
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
                'hospital_rating': updated_review.hospital_rating,
                'nickname': updated_review.author.nickname,
                'profileImg': updated_review.author.profileImg.url if updated_review.author.profileImg else None,
                'updated_at': updated_review.updated_at.strftime('%Y.%m.%d. %H:%M'),
            }
            return JsonResponse(updated_data)
        else:
            errors = filled_form.errors.as_json()
            return JsonResponse({'error': 'Form is not valid'}, status=400)

# 리뷰 삭제
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'POST':
        review.delete()
        return JsonResponse({'message': 'Review deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
