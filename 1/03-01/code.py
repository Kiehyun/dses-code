# 지구과학 데이터 사이언스 1 | III-01. 천문학에서의 시간과 좌표계
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-1.
import datetime

dt = datetime.datetime(2023, 4, 15, 12, 30, 0)

print("날짜와 시각:", dt)
print("연:", dt.year)
print("월:", dt.month)
print("일:", dt.day)
print("시:", dt.hour)
print("분:", dt.minute)
print("초:", dt.second)

# %% code Ⅲ-2.
from datetime import datetime

dt = datetime(2023, 4, 15, 12, 30, 0)

print("날짜와 시각:", dt)
print("연:", dt.year)
print("월:", dt.month)
print("일:", dt.day)

# %% code Ⅲ-3.
print("날짜와 시각:", dt.strftime("%Y-%m-%d %H:%M:%S"))
dt2 = datetime.strptime("2017-01-02 14:44", "%Y-%m-%d %H:%M")
print("날짜와 시각:", dt2.strftime("%Y-%m-%d %H:%M:%S"))

# %% code Ⅲ-4.
now = datetime.now()
print("type(now)", type(now))
print(f"현재 날짜와 시각: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 날짜만 다루는 date, 시간 간격을 다루는 timedelta 클래스
# (import datetime 으로 모듈을 다시 들여오면 앞의 datetime 클래스 이름이 가려짐)
from datetime import date, timedelta
today = date.today()
print("오늘 날짜:", today)

# %% code Ⅲ-5.
diff_days = timedelta(days=5)
print("시간 간격(일):", diff_days.days)
print("5일 뒤 날짜:", today + diff_days)

# %% code Ⅲ-6.
from datetime import datetime, timedelta
import pytz

# 토성의 2023년 충(UTC)
saturn_opposition_2023 = datetime(2023, 8, 27, 8, 0, 0, tzinfo=pytz.utc)

# 토성의 평균 회합 주기(일)
saturn_synodic_period = timedelta(days=378.10)

saturn_opposition_2024_utc = saturn_opposition_2023 + saturn_synodic_period

KST = pytz.timezone('Asia/Seoul')
saturn_opposition_2024_kst = saturn_opposition_2024_utc.astimezone(KST)

print("2024년 토성의 충 (KST, 근삿값):", 
      saturn_opposition_2024_kst.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

# %% code Ⅲ-7.
from datetime import datetime, timedelta
from dateutil import relativedelta        # 월 · 연 단위도 되는 시간 간격

def create_datetime_list(
        start_time,
        end_time,
        tdelta=relativedelta.relativedelta(minutes=15),
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
        time_list.append(current_time)
        current_time += tdelta
    return time_list

start_time = datetime(2022, 1, 5, 0, 0)
end_time = datetime(2022, 1, 5, 23, 59)
dt_list = create_datetime_list(start_time, end_time, 
                        tdelta=timedelta(minutes=30))

print("dt_list : \n", dt_list)

# %% code Ⅲ-8.
import numpy as np
from astropy.time import Time

t1 = Time('1999-01-01T00:00:00.123456789')
print("Time in UTC:", t1.utc.iso)

times = ['1999-01-01T00:00:00.123456789', '2010-01-01T00:00:00']
t2 = Time(times, scale='utc')
print("Time in UTC:", t2.utc.iso)

# %% code Ⅲ-9.
t3_string = '1999-01-01T00:00:00.123456789'
t3 = Time(t3_string, format='isot')
print("t3 :", t3)
print("t3.format: ", t3.format)

t3_jd = t3.jd  # 줄리안 데이
print("t3_jd :", t3_jd)
print("type(t3_jd): ", type(t3_jd))

t3_mjd = t3.mjd  # 수정 줄리안 데이
print("t3_mjd :", t3_mjd)
print("type(t3_mjd): ", type(t3_mjd))

t3.format = 'fits'
print("t3 :", t3)

# %% code Ⅲ-10.
from astropy import units as u
from astropy.timeseries import TimeSeries

ts1 = TimeSeries(
    time_start='2016-03-22T12:30:31', time_delta=3 * u.s, n_samples=5
)

print("type(ts1): ", type(ts1))
print("ts1: \n", ts1)

# %% code Ⅲ-11.
ts2 = TimeSeries(time=['2016-03-22T12:30:31',
                        '2016-03-22T12:30:38',
                        '2016-03-22T12:34:40'])
print("type(ts2): ", type(ts2))
print("ts2: \n", ts2)
print("ts2.time: \n", ts2.time)

ts3 = TimeSeries(time_start="2011-01-01T00:00:00",
            time_delta=[0.1, 0.2, 0.1, 0.3, 0.2]*u.s)
print("type(ts3.time): ", type(ts3.time))
print("ts3.time.jd: \n", ts3.time.jd)
print("ts3.time.mjd: \n", ts3.time.mjd)
print("ts3.time.isot: \n", ts3.time.isot)

# %% code Ⅲ-12.
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
        t_list.append(current_time)
        current_time += time_delta
    return t_list

start_time = Time('2022-01-05T00:00:00', scale='utc')
end_time = Time('2022-01-05T23:59:00', scale='utc')
t_list = create_time_list(start_time, end_time, time_delta=30*u.min)

print("len(t_list) : \n", len(t_list))
print("t_list : \n", t_list)

# %% code Ⅲ-13.
from astropy.coordinates import SkyCoord

# 문자열로 적경 · 적위 입력
c = SkyCoord(ra='20h41m25.9s', dec='+45d16m49s')
print("type(c):", type(c))
print("c :", c)

# 「시:분:초」 꼴 문자열을 SkyCoord 형식으로 바꾸기
ra_str = '20:41:25.9'
dec_str = '45:16:49'

ra_h, ra_m, ra_s = ra_str.split(':')
dec_d, dec_m, dec_s = dec_str.split(':')

ra_new = f"{ra_h}h{ra_m}m{ra_s}s"
dec_new = f"+{dec_d}d{dec_m}m{dec_s}s"

print(f"ra='{ra_new}', dec='{dec_new}'")

from astropy import units as u
# 도 단위로 적경 · 적위 입력(ICRS)
c = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')

# %% code Ⅲ-14.
print("c :", c)
print("c.ra :", c.ra)
print("c.dec :", c.dec)
print("c.ra.deg :", c.ra.deg)
print("c.dec.deg :", c.dec.deg)
print("c.icrs :", c.icrs)  # 국제 천구 기준 좌표계
print("c.fk5 :", c.fk5)    # J2000.0 기준
print("c.fk4 :", c.fk4)    # B1950.0 기준

# %% code Ⅲ-15.
from astropy.coordinates import get_constellation
print("get_constellation(c) :", get_constellation(c))

# %% code Ⅲ-16.
print("c.galactic :", c.galactic)
print("c.galactic.l :", c.galactic.l)  # 은하 경도
print("c.galactic.b :", c.galactic.b)  # 은하 위도

# %% code Ⅲ-17.
c_ecl = c.transform_to('geocentricmeanecliptic')  # 적도 좌표 → 지심 황도 좌표
print("c_ecl :", c_ecl)
print("c_ecl.lon :", c_ecl.lon)
print("c_ecl.lat :", c_ecl.lat)

# %% code Ⅲ-18.
from astropy import units as u
from astropy.coordinates import SkyCoord

c = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')

# 거리 추가(일심 좌표 변환에 필요)
c_with_distance = SkyCoord(ra=c.ra, dec=c.dec, distance=1*u.pc, frame='icrs')

# 일심 황도 좌표계로 변환
c_hcl = c_with_distance.transform_to('heliocentricmeanecliptic')

print("c_hcl :", c_hcl)
print("c_hcl.lon :", c_hcl.lon)
print("c_hcl.lat :", c_hcl.lat)

# %% code Ⅲ-19.
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u

# 관측 위치와 시각
P64 = EarthLocation(lat=37.308889*u.deg, lon=127.005*u.deg, height=101*u.m)
time = Time('2024-08-26 14:00:00')

# 지평 좌표계(AltAz) 프레임
altaz_frame = AltAz(obstime=time, location=P64)

print("type(altaz_frame) :", type(altaz_frame))
print("altaz_frame :", altaz_frame)

# %% code Ⅲ-20.
print("관측 위치 (위도, 경도, 고도):", P64.lat, P64.lon, P64.height)
print("관측 시각:", time.iso)
print("AltAz 프레임:", altaz_frame)

# 지평 좌표계로 변환
print("c:", c)
c_altaz = c.transform_to(altaz_frame)

print(f"고도: {c_altaz.alt:.2f}, 방위각: {c_altaz.az:.2f}")

# %% code Ⅲ-21.
from datetime import datetime
import matplotlib.pyplot as plt
from zoneinfo import ZoneInfo
from starplot import MapPlot, Projection, Star, _
from starplot.styles import PlotStyle, extensions

plt.rcParams.update({'figure.max_open_warning': 0})  # 그림 여러 장을 열 때의 경고 끄기

tz = ZoneInfo("Asia/Seoul")  # pytz의 timezone을 tzinfo=에 넣으면 LMT(+08:28)가 붙음

print(f"timezone : {tz}")

dt = datetime(2023, 7, 13, 22, 0, tzinfo=tz)
print(f"관측 시각 : {dt.isoformat()}")  # +09:00 확인

# 성도 설정
p = MapPlot(
    projection=Projection.ZENITH,  # 천정 투영
    lat=37.363484,                 # 관측 위치
    lon=127.836394,
    dt=dt,
    style=PlotStyle().extend(
        extensions.BLUE_MEDIUM,
    ),
    resolution=3600,  # 해상도(픽셀)
    autoscale=True,
)
p.horizon()
p.constellations()
p.stars(where=[_.magnitude < 4.6], where_labels=[_.magnitude < 2.4])  # 밝은 별과 이름
p.constellation_labels()

# 성도를 파일로 저장
# p.export(f"star_chart_basic.png", transparent=True, padding=0.1)

# %% code Ⅲ-22.
p = MapPlot(
    projection=Projection.ZENITH,
    lat=33.363484,                 # 관측 위치
    lon=-116.836394,
    dt=dt,
    style=PlotStyle().extend(
        extensions.BLUE_GOLD,
    ),
    resolution=3600,
    autoscale=True,
)
p.horizon()
p.constellations()
p.stars(where=[_.magnitude < 4.6], where_labels=[_.magnitude < 2.1])

p.galaxies(where=[_.magnitude < 9], true_size=False, labels=None)
p.open_clusters(where=[_.magnitude < 9], true_size=False, labels=None)

p.constellation_borders()
p.ecliptic()               # 황도(태양이 지나는 길)
p.celestial_equator()
p.milky_way()

# Mel 111(머리털자리 성단) 표시
p.marker(
    ra=12.36 * 15,  # 적경: 시 → 도
    dec=25.85,
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
    label="Mel 111",
)
p.constellation_labels()

# 성도를 파일로 저장
# p.export(f"star_chart_detail.png", transparent=True, padding=0.1)
