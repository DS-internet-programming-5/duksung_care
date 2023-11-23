from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Hospital

class HospitalList(ListView):
    model = Hospital
    context_object_name = 'hospital_list'

class HospitalDetail(DetailView):
    model = Hospital
    context_object_name = 'hospital'
    template_name = 'hospitals/hospital_detail.html'

def get_hospital_list(request):
    # Hospital 모델에서 필요한 데이터를 쿼리하여 JSON으로 직렬화합니다.
    hospital_list = list(Hospital.objects.values('pk', 'x', 'y'))

    # JSON 응답 반환
    return JsonResponse(hospital_list, safe=False)
