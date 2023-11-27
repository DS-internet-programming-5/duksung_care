from django.contrib import admin
from .models import Hospital, Category, Review

# Register your models here.
# admin.site.register(Hospital)
admin.site.register(Category)
admin.site.register(Review)

# import, export
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# 클래스 이름 그대로 db에 넣을 자료에 대해 정의
class HospitalResource(resources.ModelResource):
    class Meta:
        model = Hospital
        # 어떤 필드를 넣을지 정의 (전부 다 넣음)
        fields = ('id', 'place_name', 'distance', 'place_url', 'category_name', 'address_name', 'road_address_name',
                  'hospital_id', 'hospital_phone', 'category_group_code', 'category_group_name', 'x', 'y',
                  'operation_time','average_rating','has_female_doctor','has_evening_hours','has_holiday_hours','is_partnership','bookmarks')
        export_order = fields

# admin 페이지에서 어떻게 보일지 정의
class HospitalAdmin(ImportExportModelAdmin):
    # 수정 가능한 필드
    fields = ('place_name', 'distance', 'place_url', 'category_name', 'address_name', 'road_address_name',
              'hospital_id', 'hospital_phone', 'category_group_code', 'category_group_name', 'x', 'y',
              'operation_time', 'average_rating', 'has_female_doctor', 'has_evening_hours', 'has_holiday_hours',
              'is_partnership', 'bookmarks')
    list_display = ('id', 'place_name', 'category_name', 'address_name', 'road_address_name',
              'hospital_phone', 'operation_time')
    resource_class = HospitalResource

admin.site.register(Hospital, HospitalAdmin)
