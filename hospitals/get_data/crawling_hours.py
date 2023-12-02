import sys
import os

# 현재 작업 디렉토리를 추가
sys.path.append('/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duksung_care.settings')

import django
# Django 초기화
django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# hospital 모델에서 place_url, place_name 가져오기
from hospitals.models import Hospital

hospitals = Hospital.objects.all()

# Chrome WebDriver 경로 설정
webdriver_service = Service('C:/Users/jytp9/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe')
webdriver_service.start()

# Chrome 옵션 설정
chrome_options = Options()

# Chrome WebDriver 실행
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

data = []

for hospital in hospitals:
    url = hospital.place_url + '?openhour=1'
    driver.get(url)

    try:
        # WebDriverWait를 사용하여 해당 요소가 나타날 때까지 대기
        wait = WebDriverWait(driver, 2)  # 최대 2초간 대기
        operation_times = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/ul/li')))

        operation_info = []
        for time in operation_times:
            day = time.text.split()[0]  # 요일 정보 추출
            operation_time = time.find_element(By.CLASS_NAME, 'time_operation').text  # 진료 시간 정보 추출
            operation_info.append(f'{day}: {operation_time}')
    except Exception as e:
        # 요소를 찾을 수 없거나 다른 예외 발생 시, operation_info를 빈 리스트로 추가
        operation_info = []

    data.append({
        'hospital_id': hospital.hospital_id,  # Hospital 모델의 hospital_id 필드
        'place_name': hospital.place_name,
        'operation_time': '\n'.join(operation_info)  # 영업시간을 리스트로 저장하여 문자열로 변환
    })

# WebDriver 종료
driver.quit()

# DataFrame 생성
df = pd.DataFrame(data)
print(df)

# 데이터베이스 업데이트
for index, row in df.iterrows():
    hospital = Hospital.objects.get(hospital_id=row['hospital_id'])  # DataFrame에서 hospital_id 값을 이용해 Hospital 객체 가져오기
    hospital.operation_time = row['operation_time']  # 크롤링한 영업시간 데이터를 operation_time 필드에 업데이트
    hospital.save()  # 변경 사항 저장

print("영업시간 정보를 Hospital 모델의 operation_time 필드에 업데이트했습니다.")

# 데이터프레임을 엑셀 파일로 저장
excel_file_path = 'hospital_hours_data.xlsx'  # 엑셀 파일 경로 지정
df.to_excel(excel_file_path)  # 데이터프레임을 엑셀 파일로 저장

print(f"데이터프레임을 '{excel_file_path}' 파일로 저장했습니다.")