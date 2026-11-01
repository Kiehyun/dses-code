# 지구과학 데이터 사이언스 1 | III-03. 일출·일몰 시각 계산하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 31.
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderInsufficientPrivileges, GeocoderTimedOut

geolocator = Nominatim(user_agent="ESDS")

place_Suwon = "Suwon"
try:
    location_Suwon = geolocator.geocode(place_Suwon)
    if location_Suwon is None:
        raise ValueError("Location not found. Please check the place name.")
    print("location_Suwon: {}".format(location_Suwon))
except GeocoderInsufficientPrivileges:
    print("Error: Insufficient privileges to access the geocoding service. Please check your usage or try again later.")
except GeocoderTimedOut:
    print("Error: The geocoding service timed out. Please try again later.")
except Exception as e:
    print(f"Unexpected error: {e}")

location_Suwon = geolocator.geocode(place_Suwon)
print("location.raw: {}".format(location_Suwon.raw))
print("location.point: {}".format(location_Suwon.point))  # 위도 · 경도 · 고도

print(f"latitude: {location_Suwon.latitude}")
print(f"longitude: {location_Suwon.longitude}")

# %% code 32.
from astral import LocationInfo

city_London = LocationInfo("London", "England", "Europe/London", 51.5, -0.116)  # 이름, 지역, 시간대, 위도, 경도

print(f"type(city_London): {type(city_London)}")
print(f"city_London: {city_London}")

# %% code 33.
# geopy로 얻은 수원의 위도 · 경도 사용
from astral import LocationInfo

city_Suwon = LocationInfo(place_Suwon, "Korea", "Asia/Seoul", location_Suwon.latitude, location_Suwon.longitude)

print(f"type(city_Suwon): {type(city_Suwon)}")
print(f"city_Suwon: {city_Suwon}")

print(f"city_Suwon.name: {city_Suwon.name}")
print(f"city_Suwon.region: {city_Suwon.region}")
print(f"city_Suwon.timezone: {city_Suwon.timezone}")
print(f"city_Suwon.latitude: {city_Suwon.latitude}")
print(f"city_Suwon.longitude: {city_Suwon.longitude}")

# %% code 34.
from datetime import date
from astral.sun import sun

s = sun(city_Suwon.observer, date = date(2009, 3, 23),
        tzinfo=city_Suwon.timezone)

print(f"type(s): {type(s)}")
print(f"s : {s}")
print(s)

# %% code 35.
print("s['sunrise']: {}".format(s['sunrise']))
print("s['sunset']: {}".format(s['sunset']))

print("s['dawn']: {}".format(s['dawn']))  # 새벽(박명 시작)
print("s['dusk']: {}".format(s['dusk']))  # 황혼(박명 끝)

print("type(s['sunset']-s['sunrise']): {}".format(type(s['sunset']-s['sunrise'])))
print("daytime: {}".format(s['sunset']-s['sunrise']))

# %% code 36.
from datetime import date
from astral import moon
from astral import LocationInfo

city = LocationInfo("Seoul", "South Korea", "Asia/Seoul", 37.5665, 126.9780)

today = date.today()

# 월출 · 월몰 시각
moonrise_time = moon.moonrise(city.observer, date=today)
moonset_time = moon.moonset(city.observer, date=today)

print(f"날짜: {today}")
print(f"달이 뜨는 시각 (Moonrise): {moonrise_time}")
print(f"달이 지는 시각 (Moonset): {moonset_time}")

# %% code 37.
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from suntime import Sun

print("city_Suwon.latitude: {}".format(city_Suwon.latitude))
print("city_Suwon.longitude: {}".format(city_Suwon.longitude))

sun = Sun(city_Suwon.latitude, city_Suwon.longitude)

print("type(sun): {}".format(type(sun)))

def sun_times(sun, day, tz):
    """그날(현지 날짜)의 일출 · 일몰 시각"""
    d = datetime.combine(day, datetime.min.time())
    sunrise = sun.get_sunrise_time(d, tz)
    sunset = sun.get_sunset_time(d, tz)
    # suntime은 일몰 날짜가 하루 어긋날 수 있으므로 일출과 같은 날로 맞춤
    while sunset < sunrise:
        sunset += timedelta(days=1)
    while sunset - sunrise > timedelta(days=1):
        sunset -= timedelta(days=1)
    return sunrise, sunset

KST = ZoneInfo('Asia/Seoul')  # 한국 표준시
today_date = date.today()

sunrise, sunset = sun_times(sun, today_date, KST)
daytime = sunset - sunrise

print(f"{today_date} 일출 시각(KST): {sunrise}")
print(f"{today_date} 일몰 시각(KST): {sunset}")
print(f"낮의 길이 (일몰-일출): {daytime}")

# %% code 38.
# 1년 동안 수원의 낮의 길이
import matplotlib.pyplot as plt

def day_length_hours(sun, day, tz):
    """그날 낮의 길이(시간) — 앞에서 만든 sun_times() 사용"""
    sunrise, sunset = sun_times(sun, day, tz)
    return (sunset - sunrise).total_seconds() / 3600  # 초 → 시간

year = 2021
latitude = 37.2636    # 수원 위도
longitude = 127.0286  # 수원 경도
sun = Sun(latitude, longitude)

dates = []
day_lengths = []

current_date = date(year, 1, 1)
while current_date <= date(year, 12, 31):
    dates.append(current_date)
    day_lengths.append(day_length_hours(sun, current_date, KST))
    current_date += timedelta(days=1)

# 그래프 그리기
plt.figure(figsize=(12.0, 4.3))
plt.plot(dates, day_lengths, color='blue')
plt.title(f'{year}년 수원에서의 낮의 길이 변화')
plt.xlabel('날짜')
plt.ylabel('낮의 길이 (시간)')
plt.grid(True)
plt.tight_layout()
plt.show()

# %% code 39.
# 월별 낮의 총합
import matplotlib.pyplot as plt
from zoneinfo import ZoneInfo

def get_monthly_daytime_totals(year, latitude, longitude, tz_str):
    """월별 낮의 길이 합(시간) 12개를 돌려줌"""
    tz = ZoneInfo(tz_str)
    sun = Sun(latitude, longitude)
    monthly_totals = []
    for month in range(1, 13):
        total_daytime = 0
        current_date = date(year, month, 1)
        while current_date.month == month:  # 그달의 마지막 날까지
            total_daytime += day_length_hours(sun, current_date, tz)
            current_date += timedelta(days=1)
        monthly_totals.append(total_daytime)
    return monthly_totals

year = 2021
months = [f'{m}월' for m in range(1, 13)]
suwon_lat, suwon_lon, suwon_tz = 37.2636, 127.0286, 'Asia/Seoul'
suwon_totals = get_monthly_daytime_totals(year, suwon_lat, suwon_lon, suwon_tz)

# 그래프 그리기
plt.figure(figsize=(10, 5))
plt.bar(months, suwon_totals, color='skyblue')
plt.title(f'{year}년 수원 월별 낮의 총합')
plt.xlabel('월')
plt.ylabel('월별 낮의 총합 (시간)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# %% code 40.
import numpy as np
import matplotlib.pyplot as plt

# 수원(suwon_totals)은 앞에서 구함, 모스크바도 같은 함수로
moscow_lat, moscow_lon, moscow_tz = 55.751244, 37.618423, 'Europe/Moscow'
moscow_totals = get_monthly_daytime_totals(year, moscow_lat, moscow_lon, moscow_tz)

# 그래프 그리기
x = np.arange(len(months))
bar_width = 0.35

plt.figure(figsize=(10, 5))
plt.bar(x - bar_width/2, suwon_totals, width=bar_width, color='skyblue', alpha=0.8, label='수원')
plt.bar(x + bar_width/2, moscow_totals, width=bar_width, color='salmon', alpha=0.8, label='모스크바')
plt.xticks(x, months, rotation=45)
plt.title(f'{year}년 수원과 모스크바 월별 낮의 총합 비교')
plt.xlabel('월')
plt.ylabel('월별 낮의 총합 (시간)')
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.show()
