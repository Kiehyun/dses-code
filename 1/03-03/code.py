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
from datetime import datetime
from suntime import Sun

print("city_Suwon.latitude: {}".format(city_Suwon.latitude))
print("city_Suwon.longitude: {}".format(city_Suwon.longitude))

sun = Sun(city_Suwon.latitude, city_Suwon.longitude)

print("type(sun): {}".format(type(sun)))
print("sun: {}".format(sun))

# 이전 날짜 일출, 다음 날짜 일몰 사용(한국 표준시)
from datetime import datetime, date, timedelta
import pytz

tz = pytz.timezone('Asia/Seoul')
today_date = date.today()

yesterday_datetime = datetime.combine(today_date - timedelta(days=1), datetime.min.time())
tomorrow_datetime = datetime.combine(today_date + timedelta(days=1), datetime.min.time())

sunrise = sun.get_sunrise_time(yesterday_datetime).astimezone(tz)
sunset = sun.get_sunset_time(tomorrow_datetime).astimezone(tz)
daytime = sunset - sunrise

print(f"이전 날짜({yesterday_datetime.date()}) 일출 시각(LST): {sunrise}")
print(f"다음 날짜({tomorrow_datetime.date()}) 일몰 시각(LST): {sunset}")
print(f"낮의 길이 (일몰-일출): {daytime}")

# %% code 38.
# 1년 동안 낮의 길이(이전 날짜 일출, 다음 날짜 일몰 기준)
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import pytz

tz = pytz.timezone('Asia/Seoul')
year = 2021
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
    yesterday_datetime = datetime.combine(current_date - timedelta(days=1), datetime.min.time())
    tomorrow_datetime = datetime.combine(current_date + timedelta(days=1), datetime.min.time())
    sunrise = sun.get_sunrise_time(yesterday_datetime).astimezone(tz)
    sunset = sun.get_sunset_time(tomorrow_datetime).astimezone(tz)
    day_length_sec = (sunset - sunrise).total_seconds()
    # 24시간(86400초)을 넘으면 나머지만 사용
    if day_length_sec > 86400:
        day_length_sec %= 86400
    day_length = day_length_sec / 3600  # 초 → 시간
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
# 월별 낮의 총합(이전 날짜 일출, 다음 날짜 일몰 기준)
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import pytz

tz = pytz.timezone('Asia/Seoul')
year = 2021
latitude = 37.2636    # 수원 위도
longitude = 127.0286  # 수원 경도

from suntime import Sun
sun = Sun(latitude, longitude)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_daytime_totals = []

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
        # 24시간(86400초)을 넘으면 나머지만 사용
        if day_length_sec > 86400:
            day_length_sec %= 86400
        total_daytime += day_length_sec
        current_date += timedelta(days=1)
    monthly_daytime_totals.append(total_daytime / 3600)  # 초 → 시간

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
            # 24시간(86400초)을 넘으면 나머지만 사용
            if day_length_sec > 86400:
                day_length_sec %= 86400
            total_daytime += day_length_sec
            current_date += timedelta(days=1)
        monthly_totals.append(total_daytime / 3600)  # 초 → 시간
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
