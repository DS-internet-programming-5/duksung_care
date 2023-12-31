import sys
import os

# 현재 작업 디렉토리를 추가합니다. Django 프로젝트 루트 디렉토리를 가리키도록 수정해야 합니다.
sys.path.append('/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duksung_care.settings')

import django
# Django 초기화
django.setup()

import requests
from hospitals.models import Hospital, Category


# 요청 헤더에 Kakao API 키 추가
headers = {
    'Authorization': 'KakaoAK 48edddd12b48dd86f25623cd8eb5d7f7'  # 여기에 카카오 REST API 키를 넣어주세요
}

# API 요청을 보낼 URL
url = 'https://dapi.kakao.com/v2/local/search/category.json'

for page in range(1, 4):
    # 요청에 필요한 매개변수 설정
    params = {
        'category_group_code': 'HP8',
        'x': '127.01680486039935',
        'y': '37.64998176552163',
        'radius': '1550',
        'page': page
    }

    # GET 요청 보내기
    response = requests.get(url, headers=headers, params=params)

    # 응답 확인 및 데이터 추출
    if response.status_code == 200:
        data = response.json().get('documents', [])

        # 데이터 확인
        for hospital_data in data:
            print(hospital_data)  # 받아온 데이터 출력 (테스트용)

    else:
        print("API 요청 실패:", response.status_code)

    # 데이터베이스에 저장
    for hospital_data in data:
        # hospital_data['category_name'] 형식 : 의료,건강 > 병원 > 신경외과
        category_name = hospital_data['category_name'].split(' ')[-1] # 제일 마지막 카테고리만 가져옴
        # 카테고리를 가져오거나 없으면 생성
        category, created = Category.objects.get_or_create(
            name=category_name,
            slug=category_name,
        )

        # 기존 병원이 있는지 확인
        hospital = Hospital.objects.filter(hospital_id=hospital_data['id']).first()

        if not hospital:
            # 응답 데이터에 해당하는 항목을 Hospital 모델 인스턴스로 변환
            hospital = Hospital(
                address_name=hospital_data['address_name'],
                category_group_code=hospital_data['category_group_code'],
                category_group_name=hospital_data['category_group_name'],
                category_name=category,
                distance=int(hospital_data['distance']),
                hospital_id=hospital_data['id'],
                hospital_phone=hospital_data['phone'],
                place_name=hospital_data['place_name'],
                place_url=hospital_data['place_url'],
                road_address_name=hospital_data['road_address_name'],
                x=float(hospital_data['x']),
                y=float(hospital_data['y']),
            )
            hospital.save()
        elif not hospital.category_name:
            hospital.category_name = category
            hospital.save()


# '여의사진료' keyword로 검색하고 모델에 여성의사여부 저장
# API 요청을 보낼 URL
url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

# 요청에 필요한 매개변수 설정
params = {
    'category_group_code': 'HP8',
    'x': '127.01680486039935',
    'y': '37.64998176552163',
    'radius': '2000',
    'query' : '여의사진료',
    'page': '1'
}

# GET 요청 보내기
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json().get('documents', [])

    # 데이터 확인
    for hospital_data in data:
        print(hospital_data)  # 받아온 데이터 출력 (테스트용)

else:
    print("API 요청 실패:", response.status_code)

# 데이터베이스에 저장
for hospital_data in data:
    # hospital_data['category_name'] 형식 : 의료,건강 > 병원 > 신경외과
    category_name = hospital_data['category_name'].split(' ')[-1] # 제일 마지막 카테고리만 가져옴
    # 카테고리를 가져오거나 없으면 생성
    category, created = Category.objects.get_or_create(
        name=category_name,
        slug=category_name,
    )

    # 기존 병원이 있는지 확인
    hospital = Hospital.objects.filter(hospital_id=hospital_data['id']).first()

    # 존재하지 않는 경우 새로운 병원 생성
    if not hospital:
        hospital = Hospital(
            hospital_id=hospital_data['id'],
            address_name=hospital_data['address_name'],
            category_group_code=hospital_data['category_group_code'],
            category_group_name=hospital_data['category_group_name'],
            category_name=category,
            distance=hospital_data['distance'],
            hospital_phone=hospital_data['phone'],
            place_name=hospital_data['place_name'],
            place_url=hospital_data['place_url'],
            road_address_name=hospital_data['road_address_name'],
            x=float(hospital_data['x']),
            y=float(hospital_data['y']),
            has_female_doctor=True,
        )
        hospital.save()

    # 이미 존재하는 병원이고, has_female_doctor가 False인 경우만 업데이트
    elif not hospital.has_female_doctor:
        hospital.has_female_doctor = True
        hospital.save()


# '결핵검사' keyword로 검색하고 모델에 결핵검사여부 저장
# API 요청을 보낼 URL
url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

# 요청에 필요한 매개변수 설정
params = {
    'category_group_code': 'HP8',
    'x': '127.01680486039935',
    'y': '37.64998176552163',
    'radius': '2000',
    'query' : '결핵검사',
    'page': '1'
}

# GET 요청 보내기
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json().get('documents', [])

    # 데이터 확인
    for hospital_data in data:
        print(hospital_data)  # 받아온 데이터 출력 (테스트용)

else:
    print("API 요청 실패:", response.status_code)

# 데이터베이스에 저장
for hospital_data in data:
    # hospital_data['category_name'] 형식 : 의료,건강 > 병원 > 신경외과
    category_name = hospital_data['category_name'].split(' ')[-1] # 제일 마지막 카테고리만 가져옴
    # 카테고리를 가져오거나 없으면 생성
    category, created = Category.objects.get_or_create(
        name=category_name,
        slug=category_name,
    )

    # 기존 병원이 있는지 확인
    hospital = Hospital.objects.filter(hospital_id=hospital_data['id']).first()

    # 존재하지 않는 경우 새로운 병원 생성
    if not hospital:
        hospital = Hospital(
            hospital_id=hospital_data['id'],
            address_name=hospital_data['address_name'],
            category_group_code=hospital_data['category_group_code'],
            category_group_name=hospital_data['category_group_name'],
            category_name=category,
            distance=hospital_data['distance'],
            hospital_phone=hospital_data['phone'],
            place_name=hospital_data['place_name'],
            place_url=hospital_data['place_url'],
            road_address_name=hospital_data['road_address_name'],
            x=float(hospital_data['x']),
            y=float(hospital_data['y']),
            tb_test=True,
        )
        hospital.save()

    # 이미 존재하는 병원이고, tb_test가 False인 경우만 업데이트
    elif not hospital.tb_test:
        hospital.tb_test = True
        hospital.save()


# 영업 시간 추가
# import pandas as pd
#
# # 엑셀 파일 경로 지정
# excel_file_path = 'hospital_hours_data.xlsx'
#
# # 엑셀 파일을 데이터프레임으로 읽기
# excel_data = pd.read_excel(excel_file_path)
#
# # 데이터베이스에 데이터 추가
# for index, row in excel_data.iterrows():
#     hospital_id = row['hospital_id']  # hospital 모델의 primary key
#     operation_time = row['operation_time'] # operation_time 필드 데이터
#     if pd.isna(operation_time):
#         operation_time = None
#
#     # Hospital 모델 인스턴스 가져오기
#     hospital = Hospital.objects.get(hospital_id=hospital_id)
#
#     # operation_time 필드 업데이트
#     hospital.operation_time = operation_time
#     hospital.save()