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
url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

hospitals = Hospital.objects.all()

for hospital in hospitals:
    # 요청에 필요한 매개변수 설정
    params = {
        'category_group_code': 'HP8',
        'x': '127.01680486039935',
        'y': '37.64998176552163',
        'query' : hospital.place_name,
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
        if hospital_data['id'] == hospital.hospital_id:
            category_name = hospital_data['category_name'].split(' ')[-1] # 제일 마지막 카테고리만 가져옴
            # 카테고리를 가져오거나 없으면 생성
            category, created = Category.objects.get_or_create(
                name=category_name,
                slug=category_name,
            )

            hospital.category_name = category
            hospital.distance = hospital_data['distance']
            hospital.save()
            break