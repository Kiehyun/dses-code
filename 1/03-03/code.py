# 지구과학 데이터 사이언스 1 | III-03. 일출·일몰 시각 계산하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 31.
# geopy를 이용하여 도시의 위치 정보(위도, 경도) 얻기
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderInsufficientPrivileges, GeocoderTimedOut

geolocator = Nominatim(user_agent="ESDS") # 위치 정보 검색 객체 생성

place_Suwon = "Suwon" # 검색할 도시 이름
try:
    location_Suwon = geolocator.geocode(place_Suwon) # 도시 위치 정보 검색
    if location_Suwon is None:
        raise ValueError("Location not found. Please check the place name.")
    print("location_Suwon: {}".format(location_Suwon))
except GeocoderInsufficientPrivileges:
    print("Error: Insufficient privileges to access the geocoding service. Please check your usage or try again later.")
except GeocoderTimedOut:
    print("Error: The geocoding service timed out. Please try again later.")
except Exception as e:
    print(f"Unexpected error: {e}")

# 위치 정보의 세부 내용 출력
location_Suwon = geolocator.geocode(place_Suwon)
print("location.raw: {}".format(location_Suwon.raw))  # 원시 데이터
print("location.point: {}".format(location_Suwon.point))  # 위도, 경도, 고도 정보

print(f"latitude: {location_Suwon.latitude}")    # 위도
print(f"longitude: {location_Suwon.longitude}")  # 경도

# %% code 32.
# astral 패키지의 LocationInfo를 이용하여 위치 정보 객체 생성
from astral import LocationInfo

city_London = LocationInfo("London", "England", "Europe/London", 51.5, -0.116)

print(f"type(city_London): {type(city_London)}")
print(f"city_London: {city_London}")

# %% code 33.
# geopy로 얻은 위치 정보를 이용하여 수원 LocationInfo 객체 생성
from astral import LocationInfo

city_Suwon = LocationInfo(place_Suwon, "Korea", "Asia/Seoul", location_Suwon.latitude, location_Suwon.longitude)

print(f"type(city_Suwon): {type(city_Suwon)}")
print(f"city_Suwon: {city_Suwon}")

# LocationInfo 객체의 세부 정보 출력
print(f"city_Suwon.name: {city_Suwon.name}")
print(f"city_Suwon.region: {city_Suwon.region}")
print(f"city_Suwon.timezone: {city_Suwon.timezone}")
print(f"city_Suwon.latitude: {city_Suwon.latitude}")
print(f"city_Suwon.longitude: {city_Suwon.longitude}")

# %% code 34.
# astral.sun 함수를 이용하여 일출, 일몰 등 태양 관련 시각 계산
from datetime import date
from astral.sun import sun

s = sun(city_Suwon.observer, 
        date = date(2009, 3, 23), 
        tzinfo=city_Suwon.timezone)

print(f"type(s): {type(s)}")  # 결과 타입 출력
print(f"s : {s}")             # 전체 딕셔너리 출력
print(s)                      # 전체 딕셔너리 출력

# %% code 35.
# 일출, 일몰, 새벽, 황혼 시각 및 낮의 길이 출력
print("s['sunrise']: {}".format(s['sunrise']))  # 일출 시각
print("s['sunset']: {}".format(s['sunset']))    # 일몰 시각

print("s['dawn']: {}".format(s['dawn']))  # 새벽 시각
print("s['dusk']: {}".format(s['dusk']))  # 황혼 시각

print("type(s['sunset']-s['sunrise']): {}".format(type(s['sunset']-s['sunrise']))) # 낮의 길이 타입
print("daytime: {}".format(s['sunset']-s['sunrise'])) # 낮의 길이

# %% code 36.
# astral의 moon 모듈로 월출/월몰 시각 계산
from datetime import date
from astral import moon
from astral import LocationInfo

# 관측 지역 설정
city = LocationInfo("Seoul", "South Korea", "Asia/Seoul", 37.5665, 126.9780)

# 오늘 날짜 기준
today = date.today()

# 달의 일출(월출)과 일몰(월몰) 시각 계산
moonrise_time = moon.moonrise(city.observer, date=today)
moonset_time = moon.moonset(city.observer, date=today)

# 결과 출력
print(f"날짜: {today}")
print(f"달이 뜨는 시각 (Moonrise): {moonrise_time}")
print(f"달이 지는 시각 (Moonset): {moonset_time}")

# %% code 37.
# suntime 패키지로 태양 객체 생성 및 정보 출력
from datetime import datetime
from suntime import Sun

print("city_Suwon.latitude: {}".format(city_Suwon.latitude)) # 위도
print("city_Suwon.longitude: {}".format(city_Suwon.longitude)) # 경도

sun = Sun(city_Suwon.latitude, city_Suwon.longitude) # 태양 객체 생성

print("type(sun): {}".format(type(sun)))  # 객체 타입 출력
print("sun: {}".format(sun))              # 객체 정보 출력

# 일출/일몰 시각을 한국 표준시(LST)로 변환하여 출력 (이전 날짜 일출, 다음 날짜 일몰 사용)
from datetime import datetime, date, timedelta
import pytz

tz = pytz.timezone('Asia/Seoul')
today_date = date.today()

# 이전 날짜와 다음 날짜의 0시 datetime 객체 생성
yesterday_datetime = datetime.combine(today_date - timedelta(days=1), datetime.min.time())
tomorrow_datetime = datetime.combine(today_date + timedelta(days=1), datetime.min.time())

# 일출/일몰 시각 계산 및 변환
sunrise = sun.get_sunrise_time(yesterday_datetime).astimezone(tz)
sunset = sun.get_sunset_time(tomorrow_datetime).astimezone(tz)
daytime = sunset - sunrise

print(f"이전 날짜({yesterday_datetime.date()}) 일출 시각(LST): {sunrise}")
print(f"다음 날짜({tomorrow_datetime.date()}) 일몰 시각(LST): {sunset}")
print(f"낮의 길이 (일몰-일출): {daytime}")

# %% code 38.
# 1년 동안 (이전 날짜 일출, 다음 날짜 일몰 기준) 낮의 길이 변화 시각화 (24시간 이상 방지)
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import pytz

tz = pytz.timezone('Asia/Seoul')
year = 2021           # 원하는 연도
latitude = 37.2636    # 수원 위도
longitude = 127.0286  # 수원 경도

from suntime import Sun
sun = Sun(latitude, longitude)

dates = []
day_lengths = []

start_date = date(year, 1, 1)
end_date = date(year, 12, 31)
delta = timedelta(days=1)
current_date = start_date

while current_date <= end_date:
 # 이전 날짜와 다음 날짜의 0시 datetime 객체
    yesterday_datetime = datetime.combine(current_date - timedelta(days=1), datetime.min.time())
    tomorrow_datetime = datetime.combine(current_date + timedelta(days=1), datetime.min.time())
 # 일출/일몰 시각 계산 및 변환
    sunrise = sun.get_sunrise_time(yesterday_datetime).astimezone(tz)
    sunset = sun.get_sunset_time(tomorrow_datetime).astimezone(tz)
    day_length_sec = (sunset - sunrise).total_seconds()
 # 0보다 작거나 24시간(86400초)보다 크면 나머지 값으로 처리
    if day_length_sec > 86400:
        day_length_sec %= 86400
    day_length = day_length_sec / 3600  # 시간 단위
    dates.append(current_date)
    day_lengths.append(day_length)
    current_date += delta

# 그래프 그리기
plt.figure(figsize=(12.0, 4.3))
plt.plot(dates, day_lengths, color='blue')
plt.title(f'{year}년 수원에서의 낮의 길이 변화 (이전 날짜 일출, 다음 날짜 일몰 기준)')
plt.xlabel('날짜')
plt.ylabel('낮의 길이 (시간)')
plt.grid(True)
plt.tight_layout()
plt.show()

# %% code 39.
# 1년 동안 (이전 날짜 일출, 다음 날짜 일몰 기준) 월별 낮의 총합(시간) 그래프
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import pytz

tz = pytz.timezone('Asia/Seoul')
year = 2021           # 원하는 연도
latitude = 37.2636    # 수원 위도
longitude = 127.0286  # 수원 경도

from suntime import Sun
sun = Sun(latitude, longitude)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_daytime_totals = []

for month in range(1, 13):
    total_daytime = 0
 # 월의 시작일과 종료일 계산
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year, 12, 31)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        yesterday_datetime = datetime.combine(current_date - timedelta(days=1), datetime.min.time())
        tomorrow_datetime = datetime.combine(current_date + timedelta(days=1), datetime.min.time())
        sunrise = sun.get_sunrise_time(yesterday_datetime).astimezone(tz)
        sunset = sun.get_sunset_time(tomorrow_datetime).astimezone(tz)
        day_length_sec = (sunset - sunrise).total_seconds()
 # 0보다 작거나 24시간(86400초)보다 크면 나머지 값으로 처리
        if day_length_sec > 86400:
            day_length_sec %= 86400
        total_daytime += day_length_sec
        current_date += timedelta(days=1)
    monthly_daytime_totals.append(total_daytime / 3600)  # 시간 단위

# 그래프 그리기
plt.figure(figsize=(10, 5))
plt.bar(months, monthly_daytime_totals, color='skyblue')
plt.title(f'{year}년 수원 월별 낮의 총합 (이전 날짜 일출, 다음 날짜 일몰 기준)')
plt.xlabel('월')
plt.ylabel('월별 낮의 총합 (시간)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# %% code 40.
# 수원과 모스코바의 월별 낮의 총합(시간) 비교 그래프
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import pytz
from suntime import Sun

def get_monthly_daytime_totals(year, latitude, longitude, tz_str):
    tz = pytz.timezone(tz_str)
    sun = Sun(latitude, longitude)
    monthly_totals = []
    for month in range(1, 13):
        total_daytime = 0
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        current_date = start_date
        while current_date <= end_date:
            yesterday_datetime = datetime.combine(current_date - timedelta(days=1), datetime.min.time())
            tomorrow_datetime = datetime.combine(current_date + timedelta(days=1), datetime.min.time())
            sunrise = sun.get_sunrise_time(yesterday_datetime).astimezone(tz)
            sunset = sun.get_sunset_time(tomorrow_datetime).astimezone(tz)
            day_length_sec = (sunset - sunrise).total_seconds()
 # 0보다 작거나 24시간(86400초)보다 크면 나머지 값으로 처리
            if day_length_sec > 86400:
                day_length_sec %= 86400
            total_daytime += day_length_sec
            current_date += timedelta(days=1)
        monthly_totals.append(total_daytime / 3600)  # 시간 단위
    return monthly_totals

year = 2021
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# 수원
suwon_lat, suwon_lon, suwon_tz = 37.2636, 127.0286, 'Asia/Seoul'
suwon_totals = get_monthly_daytime_totals(year, suwon_lat, suwon_lon, suwon_tz)

# 모스코바
moscow_lat, moscow_lon, moscow_tz = 55.751244, 37.618423, 'Europe/Moscow'
moscow_totals = get_monthly_daytime_totals(year, moscow_lat, moscow_lon, moscow_tz)

# 그래프 그리기
import numpy as np
x = np.arange(len(months))
bar_width = 0.35

plt.figure(figsize=(10, 5))
plt.bar(x - bar_width/2, suwon_totals, width=bar_width, color='skyblue', alpha=0.8, label='Suwon')
plt.bar(x + bar_width/2, moscow_totals, width=bar_width, color='salmon', alpha=0.8, label='Moscow')
plt.xticks(x, months, rotation=45)
plt.title(f'{year}년 수원과 모스코바 월별 낮의 총합 비교')
plt.xlabel('월')
plt.ylabel('월별 낮의 총합 (시간)')
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.show()
