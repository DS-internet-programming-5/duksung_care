from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Hospital, Review
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HospitalList(ListView):
    model = Hospital
    context_object_name = 'hospital_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hospitals = context['hospital_list']

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
        return context


def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    review_list = Review.objects.filter(hospital=pk)

    review_form = ReviewForm()

    return render(request, 'hospitals/hospital_detail.html',
                  {'hospital': hospital, 'review_list': review_list, 'review_form': review_form})


def get_hospital_list(request):
    # Hospital 모델에서 필요한 데이터를 쿼리하여 JSON으로 직렬화합니다.
    hospital_list = list(Hospital.objects.values('pk', 'x', 'y'))

    # JSON 응답 반환
    return JsonResponse(hospital_list, safe=False)


def new_review(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        filled_form = ReviewForm(request.POST)
        if filled_form.is_valid():
            finished_form = filled_form.save(commit=False)
            finished_form.hospital = get_object_or_404(Hospital, pk=pk)
            finished_form.author = request.user
            finished_form.save()

            # 새로 추가된 리뷰의 내용을 가져와서 JSON 응답
            new_review = {
                'content': finished_form.content,
                'hospital_rating': finished_form.hospital_rating,
                # 필요한 경우 추가 필드도 JSON에 포함
            }
            return JsonResponse(new_review)
        else:
            # 폼이 유효하지 않은 경우 에러 메시지를 JSON으로 반환
            errors = filled_form.errors.as_json()
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
