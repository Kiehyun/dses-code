# 지구과학 데이터 사이언스 1 | III-01. 천문학에서의 시간과 좌표계
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
import datetime

dt = datetime.datetime(2023, 4, 15, 12, 30, 0)

print("Specific date and time:", dt)
print("Year:", dt.year)
print("Month:", dt.month)
print("Day:", dt.day)
print("Hour:", dt.hour)
print("Minute:", dt.minute)
print("Second:", dt.second)

# %% code 2.
from datetime import datetime

dt = datetime(2023, 4, 15, 12, 30, 0)

print("Specific date and time:", dt)
print("Year:", dt.year)
print("Month:", dt.month)
print("Day:", dt.day)

# %% code 3.
print("Specific date and time:", dt.strftime("%Y-%m-%d %H:%M:%S"))
dt2 = datetime.strptime("2017-01-02 14:44", "%Y-%m-%d %H:%M")
print("Specific date and time:", dt2.strftime("%Y-%m-%d %H:%M:%S"))

# %% code 4.
# 현재 날짜와 시각
now = datetime.now()
print("type(now)", type(now))
print(f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

import datetime
today = datetime.date.today()
print("Today's date:", today)

# %% code 5.
diff_days = datetime.timedelta(days=5)
print("Difference in days:", diff_days.days)
print("Date after adding 5 days:", today + diff_days)

# %% code 6.
from datetime import datetime, timedelta
import pytz

# 토성의 2023년 충
saturn_conjunction_2023 = datetime(2023, 8, 27, 8, 0, 0, tzinfo=pytz.utc)

# 토성의 회합 주기
saturn_synodic_period = timedelta(days=378.10)

# 2024년 토성의 충 (UTC)
saturn_conjunction_2024_utc = saturn_conjunction_2023 + saturn_synodic_period

# 한국 표준시(KST)로 변환
KST = pytz.timezone('Asia/Seoul')
saturn_conjunction_2024_kst = saturn_conjunction_2024_utc.astimezone(KST)

print("2024년 토성의 충 (KST):", 
      saturn_conjunction_2024_kst.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

# %% code 7.
from datetime import datetime, timedelta  # 날짜와 시간, 시간 간격 처리
from dateutil import relativedelta        # 유연한 시간 간격(상대적 델타) 처리

def create_datetime_list(
        start_time,
        end_time,
        tdelta=relativedelta.relativedelta(minutes=15),  # 기본 간격: 15분
        **kwargs
        ):
    '''
    일정한 시간 간격의 datetime 리스트 생성 함수
    Parameters
    ----------
    start_time : datetime.datetime, 시작 시각
    end_time : datetime.datetime, 끝 시각
    tdelta : 시간 간격 (timedelta 또는 relativedelta)
    Returns : 지정한 간격으로 생성된 datetime 객체 리스트
    '''
    time_list = []
    current_time = start_time
    while current_time <= end_time:
        time_list.append(current_time)  # 리스트에 현재 시각 추가
        current_time += tdelta          # 시간 간격만큼 증가
    return time_list

start_time = datetime(2022, 1, 5, 0, 0)  # 시작 시각: 2022년 1월 5일 0시 0분
end_time = datetime(2022, 1, 5, 23, 59)  # 끝 시각: 2022년 1월 5일 23시 59분
dt_list = create_datetime_list(start_time, end_time, 
                        tdelta=timedelta(minutes=30))  # 30분 간격 리스트 생성

print("dt_list : \n", dt_list)  # 결과 출력

# %% code 8.
import numpy as np
from astropy.time import Time  # astropy의 Time 클래스 임포트

t1 = Time('1999-01-01T00:00:00.123456789')  # 문자열로부터 Time 객체 생성
print("Time in UTC:", t1.utc.iso)           # UTC 기준 ISO 포맷으로 출력

times = ['1999-01-01T00:00:00.123456789', '2010-01-01T00:00:00']  # 여러 시각을 리스트로 준비
t2 = Time(times, scale='utc')      # 리스트로부터 Time 객체 생성 (UTC 스케일 지정)
print("Time in UTC:", t2.utc.iso)  # 각각의 시각을 UTC 기준 ISO 포맷으로 출력

# %% code 9.
t3_string = '1999-01-01T00:00:00.123456789'
t3 = Time(t3_string, format='isot')  # ISO 형식 문자열로부터 Time 객체 생성
print("t3 :", t3)                    # Time 객체 출력
print("t3.format: ", t3.format)      # 현재 포맷 확인

t3_jd = t3.jd  # 줄리안 데이(Julian Date)로 변환
print("t3_jd :", t3_jd)
print("type(t3_jd): ", type(t3_jd))  # 타입 확인

t3_mjd = t3.mjd  # 수정 줄리안 데이(Modified Julian Date)로 변환
print("t3_mjd :", t3_mjd)
print("type(t3_mjd): ", type(t3_mjd))  # 타입 확인

t3.format = 'fits'  # 출력 포맷을 FITS 형식으로 변경
print("t3 :", t3)   # 변경된 포맷으로 출력

# %% code 10.
from astropy import units as u
from astropy.timeseries import TimeSeries

# 2016-03-22T12:30:31부터 시작하여 3초 간격으로 5개의 시각 생성
ts1 = TimeSeries(
    time_start='2016-03-22T12:30:31',  # 시작 시각
    time_delta=3 * u.s,                # 시간 간격: 3초
    n_samples=5                        # 샘플 개수: 5개
)

print("type(ts1): ", type(ts1))  # TimeSeries 객체의 타입 출력
print("ts1: \n", ts1)            # 생성된 TimeSeries 객체 출력

# %% code 11.
ts2 = TimeSeries(time=['2016-03-22T12:30:31',
                        '2016-03-22T12:30:38',
                        '2016-03-22T12:34:40'])
print("type(ts2): ", type(ts2))  # TimeSeries 객체의 타입 출력
print("ts2: \n", ts2)            # 생성된 TimeSeries 객체 출력
print("ts2.time: \n", ts2.time)  # TimeSeries 객체의 시간 정보 출력

ts3 = TimeSeries(time_start="2011-01-01T00:00:00",
            time_delta=[0.1, 0.2, 0.1, 0.3, 0.2]*u.s)
print("type(ts3.time): ", type(ts3.time))  # ts3.time의 타입 출력
print("ts3.time.jd: \n", ts3.time.jd)      # 줄리안 데이(Julian Date)로 변환된 시간 정보 출력   
ts3.time.jd = ts3.time.mjd                 # 수정 줄리안 데이(Modified Julian Date)로 변환
print("ts3.time.mjd: \n", ts3.time.mjd)    # 수정 줄리안 데이로 변환된 시간 정보 출력
print("ts3.time.isot: \n", ts3.time.isot)  # ISO 형식으로 변환된 시간 정보 출력 

# %% code 12.
from astropy.time import Time
import astropy.units as u

def create_time_list(
        start_time,
        end_time,
        time_delta=30*u.min,
        **kwargs
        ):
    '''
    일정한 시간 간격의 astropy Time 객체 리스트 생성 함수
    Parameters
    ----------
    start_time : astropy.time.Time, 시작 시각
    end_time : astropy.time.Time, 끝 시각
    time_delta : 시간 간격 (기본값 30분, astropy.units 사용)
    Returns : 지정한 간격으로 생성된 astropy Time 객체 리스트
    '''
    t_list = []
    current_time = start_time
    while current_time <= end_time:
        t_list.append(current_time)  # 리스트에 현재 시각 추가
        current_time += time_delta   # 시간 간격만큼 증가
    return t_list

start_time = Time('2022-01-05T00:00:00', scale='utc')  # 시작 시각: 2022년 1월 5일 0시 0분(UTC)
end_time = Time('2022-01-05T23:59:00', scale='utc')  # 끝 시각: 2022년 1월 5일 23시 59분(UTC)
t_list = create_time_list(start_time, end_time, time_delta=30*u.min)  # 30분 간격 리스트 생성

print("len(t_list) : \n", len(t_list))  # 리스트 길이(시각 개수) 출력
print("t_list : \n", t_list)            # 생성된 시각 리스트 출력

# %% code 13.
from astropy.coordinates import SkyCoord

# 문자열로 적경(RA), 적위(Dec)를 입력하여 SkyCoord 객체 생성
c = SkyCoord(ra='20h41m25.9s', dec='+45d16m49s')
print("type(c):", type(c))  # SkyCoord 객체의 타입 출력
print("c :", c)             # SkyCoord 객체 정보 출력

# 시, 분, 초/도, 분, 초 형식의 문자열을 분리하여 새로운 형식으로 변환
ra_str = '20:41:25.9'
dec_str = '45:16:49'

ra_h, ra_m, ra_s = ra_str.split(':')      # RA 문자열 분리
dec_d, dec_m, dec_s = dec_str.split(':')  # Dec 문자열 분리

# SkyCoord에서 사용하는 형식으로 변환
ra_new = f"{ra_h}h{ra_m}m{ra_s}s"
dec_new = f"+{dec_d}d{dec_m}m{dec_s}s"

print(f"ra='{ra_new}', dec='{dec_new}'")  # 변환된 문자열 출력

from astropy import units as u
# 도 단위로 적경(RA), 적위(Dec)를 입력하여 SkyCoord 객체 생성 (ICRS 프레임)
c = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')

# %% code 14.
print("c :", c)                  # SkyCoord 객체 전체 정보 출력
print("c.ra :", c.ra)            # 적경(Right Ascension, RA) 값 (단위 포함)
print("c.dec :", c.dec)          # 적위(Declination, Dec) 값 (단위 포함)
print("c.ra.deg :", c.ra.deg)    # 적경(RA)을 도(degree) 단위로 출력
print("c.dec.deg :", c.dec.deg)  # 적위(Dec)를 도(degree) 단위로 출력
print("c.icrs :", c.icrs)        # ICRS(국제 천체 기준 좌표계)로 변환된 좌표 출력
print("c.fk5 :", c.fk5)          # FK5(J2000.0 기준) 좌표계로 변환된 좌표 출력
print("c.fk4 :", c.fk4)          # FK4(B1950.0 기준) 좌표계로 변환된 좌표 출력

# %% code 15.
from astropy.coordinates import get_constellation
print("get_constellation(c) :", get_constellation(c))

# %% code 16.
print("c.galactic :", c.galactic)      # 은하 좌표계(Galactic)로 변환된 전체 좌표 출력
print("c.galactic.l :", c.galactic.l)  # 은하 경도(Galactic Longitude, l) 값 출력
print("c.galactic.b :", c.galactic.b)  # 은하 위도(Galactic Latitude, b) 값 출력

# %% code 17.
c_ecl = c.transform_to('geocentricmeanecliptic')  # 적도좌표계에서 지심 황도좌표계로 변환
print("c_ecl :", c_ecl)                           # 변환된 황도좌표계 전체 정보 출력
print("c_ecl.lon :", c_ecl.lon)                   # 황도 경도(Longitude) 값 출력
print("c_ecl.lat :", c_ecl.lat)                   # 황도 위도(Latitude) 값 출력

# %% code 18.
from astropy import units as u
from astropy.coordinates import SkyCoord

# 기존 SkyCoord 객체
c = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')

# 거리를 추가하여 새로운 SkyCoord 객체 생성
c_with_distance = SkyCoord(ra=c.ra, dec=c.dec, distance=1*u.pc, frame='icrs')

# 일심 황도 좌표계로 변환
c_hcl = c_with_distance.transform_to('heliocentricmeanecliptic')

# 결과 출력
print("c_hcl :", c_hcl)
print("c_hcl.lon :", c_hcl.lon)
print("c_hcl.lat :", c_hcl.lat)

# %% code 19.
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u

# 관측 위치와 시간 설정
P64 = EarthLocation(lat=37.308889*u.deg, lon=127.005*u.deg, height=101*u.m)
time = Time('2024-08-26 14:00:00')

# AltAz 프레임 생성
altaz_frame = AltAz(obstime=time, location=P64)

print("type(altaz_frame) :", type(altaz_frame))
print("altaz_frame :", altaz_frame)

# %% code 20.
# 관측 위치와 시각 정보를 함께 출력
print("관측 위치 (위도, 경도, 고도):", P64.lat, P64.lon, P64.height)
print("관측 시각:", time.iso)
print("AltAz 프레임:", altaz_frame)

# 천체의 좌표를 AltAz(지평 좌표계)로 변환
print("c:", c)                         # 변환 전 SkyCoord 객체 정보 출력
c_altaz = c.transform_to(altaz_frame)  # AltAz 프레임으로 좌표 변환

# 변환된 좌표에서 고도(alt)와 방위각(az) 값을 소수점 2자리까지 출력
print(f"고도: {c_altaz.alt:.2f}, 방위각: {c_altaz.az:.2f}")

# %% code 21.
from datetime import datetime                      # 날짜와 시간 처리
import matplotlib.pyplot as plt                    # 그래프 및 이미지 시각화
from pytz import timezone                          # 타임존(시간대) 처리
from starplot import MapPlot, Projection, Star, _  # starplot의 주요 클래스 및 헬퍼
from starplot.styles import PlotStyle, extensions  # 스타일 및 확장 테마

plt.rcParams.update({'figure.max_open_warning': 0})  # matplotlib 경고 메시지 억제

tz = timezone("Asia/Seoul")  # 한국 표준시(KST) 타임존 객체 생성

print(f"timezone : {tz}")  # 현재 타임존 출력

dt = datetime(2023, 7, 13, 22, 0, tzinfo=tz)  # 2023년 7월 13일 22시(한국시간) datetime 객체 생성

# MapPlot 객체 생성: 성도(별자리 지도) 설정
p = MapPlot(
    projection=Projection.ZENITH,  # 천정(Zenith) 투영법 사용
    lat=37.363484,                 # 위도(관측 위치)
    lon=127.836394,                # 경도(관측 위치)
    dt=dt,                         # 관측 시각
    style=PlotStyle().extend(
        extensions.BLUE_MEDIUM,  # 파란색 계열 스타일 적용
    ),
    resolution=3600,  # 해상도(픽셀)
    autoscale=True,   # 자동 스케일링
)
p.horizon()               # 지평선 표시
p.constellations()        # 별자리 선 표시
p.stars(where=[_.magnitude < 4.6], where_labels=[_.magnitude < 2.4])  # 밝은 별과 라벨 표시
p.constellation_labels()  # 별자리 이름 라벨 표시

# 성도 이미지를 파일로 저장
# p.export(f"star_chart_basic.png", transparent=True, padding=0.1)

# %% code 22.
p = MapPlot(
    projection=Projection.ZENITH,  # 천정(Zenith) 투영법 사용
    lat=33.363484,                 # 위도(관측 위치)
    lon=-116.836394,               # 경도(관측 위치)
    dt=dt,                         # 관측 시각
    style=PlotStyle().extend(
        extensions.BLUE_GOLD,      # 파란색-금색 계열 스타일 적용
    ),
    resolution=3600,  # 해상도(픽셀)
    autoscale=True,   # 자동 스케일링
)
p.horizon()         # 지평선 표시
p.constellations()  # 별자리 선 표시
p.stars(where=[_.magnitude < 4.6], where_labels=[_.magnitude < 2.1])  # 밝은 별과 라벨 표시

p.galaxies(where=[_.magnitude < 9], true_size=False, labels=None)  # 밝은 은하 표시
p.open_clusters(where=[_.magnitude < 9], true_size=False, labels=None)  # 밝은 산개성단 표시

p.constellation_borders()  # 별자리 경계선 표시
p.ecliptic()               # 황도(태양의 경로) 표시
p.celestial_equator()      # 천구 적도 표시
p.milky_way()              # 은하수 표시

# 특정 위치(예: Mel 111)에 마커와 라벨 추가
p.marker(
    ra=12.36 * 15,  # 적경(RA, 시간→도 단위 변환)
    dec=25.85,      # 적위(Dec)
    style={
        "marker": {
            "size": 60,
            "symbol": "circle",
            "fill": "none",
            "color": None,
            "edge_color": "hsl(44, 70%, 73%)",
            "edge_width": 2,
            "line_style": [1, [2, 3]],
            "alpha": 1,
            "zorder": 100,
        },
        "label": {
            "zorder": 200,
            "font_size": 22,
            "font_weight": "bold",
            "font_color": "hsl(44, 70%, 64%)",
            "font_alpha": 1,
            "offset_x": "auto",
            "offset_y": "auto",
            "anchor_point": "top right",
        },
    },
    label="Mel 111",  # 라벨 텍스트
)
p.constellation_labels()  # 별자리 이름 라벨 표시

# 성도 이미지를 파일로 저장
# p.export(f"star_chart_detail.png", transparent=True, padding=0.1)
