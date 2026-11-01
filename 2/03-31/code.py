# 지구과학 데이터 사이언스 2 | III-11. 소행성 관측 계획 수립하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 336.
import pandas as pd

def classify_asteroid(a, e):
    """궤도 긴반지름 a(au)와 이심률 e로 소행성 무리를 대략 판단"""
    q = a * (1 - e)                  # 근일점 거리
    Q = a * (1 + e)                  # 원일점 거리
    if q < 1.3:                      # 근지구소행성
        if Q < 0.983:
            return "근지구 - 아티라"
        if a < 1.0:
            return "근지구 - 아텐"
        if q < 1.017:
            return "근지구 - 아폴로"
        return "근지구 - 아모르"
    if 1.8 <= a < 2.0:
        return "헝가리아족"
    if 2.0 <= a < 3.3:
        return "소행성대"
    if 3.7 <= a < 4.2:
        return "힐다족"
    if 5.05 <= a < 5.35:
        return "목성 트로이군"
    if 5.5 <= a < 30.1:
        return "센타우루스족"
    if a >= 30.1:
        return "해왕성 바깥 천체"
    return "기타"

# 이름, 궤도 긴반지름 a(au), 이심률 e
samples = [
    ("1 Ceres",        2.767, 0.079),
    ("434 Hungaria",   1.944, 0.074),
    ("153 Hilda",      3.972, 0.137),
    ("624 Hektor",     5.263, 0.023),
    ("2060 Chiron",   13.692, 0.379),
    ("433 Eros",       1.458, 0.223),
    ("1862 Apollo",    1.470, 0.560),
    ("2062 Aten",      0.967, 0.183),
    ("99942 Apophis",  0.922, 0.191),
    ("101955 Bennu",   1.126, 0.204),
    ("163693 Atira",   0.741, 0.322),
]

df_orbit = pd.DataFrame(samples, columns=["name", "a(au)", "e"])
df_orbit["q(au)"] = (df_orbit["a(au)"] * (1 - df_orbit["e"])).round(3)
df_orbit["Q(au)"] = (df_orbit["a(au)"] * (1 + df_orbit["e"])).round(3)
df_orbit["group"] = [classify_asteroid(a, e) for a, e in zip(df_orbit["a(au)"], df_orbit["e"])]
df_orbit

# %% code 337.
import numpy as np
import matplotlib.pyplot as plt

a_grid = np.linspace(0.6, 6, 400)

fig, ax = plt.subplots(figsize=(8, 4.4))
ax.plot(a_grid, 1 - 1.3 / a_grid, "r-", label="q = 1.3 au (근지구소행성 경계)")
ax.plot(a_grid, 1 - 1.017 / a_grid, "r--", label="q = 1.017 au (지구 궤도 가로지름)")
ax.axvline(1.0, color="gray", ls=":", label="a = 1.0 au")
ax.axvspan(2.0, 3.3, color="tab:blue", alpha=0.12, label="소행성대")

for _, row in df_orbit[df_orbit["a(au)"] < 6].iterrows():
    ax.plot(row["a(au)"], row["e"], "ko", ms=4)
    ax.annotate(row["name"], (row["a(au)"], row["e"]),
                textcoords="offset points", xytext=(4, 3), fontsize=8)

ax.set_xlim(0.6, 6)
ax.set_ylim(0, 0.7)
ax.set_xlabel("궤도 긴반지름 a (au)")
ax.set_ylabel("이심률 e")
ax.set_title("궤도 요소에 따른 소행성 분류")
ax.legend(fontsize=8, loc="upper right")
plt.show()

# %% code 338.
from datetime import datetime, timedelta, timezone
from astropy.time import Time

KST = timezone(timedelta(hours=9))
dt_kst = datetime(2023, 9, 11, 20, 19, 18, tzinfo=KST)     # 관측 시각(한국 표준시)
dt_utc = dt_kst.astimezone(timezone.utc)
print("한국 표준시:", dt_kst)
print("세계시     :", dt_utc)

def datetime_range(start_dt, end_dt, delta):
    """start_dt부터 end_dt 앞까지 delta 간격의 datetime을 차례로 내놓음"""
    current = start_dt
    while current < end_dt:
        yield current
        current += delta

print([d.strftime("%m-%d") for d in datetime_range(datetime(2024, 12, 1),
                                                   datetime(2024, 12, 4),
                                                   timedelta(days=1))])

# %% code 339.
t = Time(dt_utc, location=("127d", "37d"))
print("세계시      :", t.utc.iso)
print("줄리안일    :", t.jd)
print("평균 항성시 :", t.sidereal_time("mean"))

# %% code 340.
#############################################
# 변수
mpc_code='P64' # 관측 위치: 경기과학고 천문대, 수원 [코드 P64]

import astropy.units as u
from astropy.coordinates import EarthLocation

site_p64 = EarthLocation(lon=127.0*u.deg, lat=37.3*u.deg)

# 관측 시각 설정(고정 시각: 2024년 12월 2일 21시 KST를 UTC로 바꿈)
t_obs = Time(datetime(2024, 12, 2, 21, 0, 0, tzinfo=KST), location=site_p64)
# 지금 시각의 목록을 받으려면 위 줄 대신 다음 줄을 씀
# t_obs = Time(Time.now(), location=site_p64)
print("type(t_obs) :", type(t_obs))
print("관측 시각(UTC) :", t_obs.iso)
print("관측 시각(KST) :", t_obs.to_datetime(timezone=KST))

obs_datetime = t_obs.strftime('%Y-%m-%dT%H:%M:%S')
print("obs_datetime :", obs_datetime)
obs_date = t_obs.strftime('%Y%m%d')
print("obs_date :", obs_date)

# 변수 설정
elev_min=60
time_min=15
vmag_min=6
vmag_max=13
list_num=100
sort='trans'

# %% code 341.
# API 주소 정의
url = 'https://ssd-api.jpl.nasa.gov/sbwobs.api'

# 이 API 요청에 맞는 주소 만들기
url += f"?sb-kind=a&mpc-code={mpc_code}&obs-time={obs_datetime}&elev-min={elev_min}&time-min={time_min}"
url += f"&vmag-max={vmag_max}&vmag-min={vmag_min}&optical=true&fmt-ra-dec=true&mag-required=true&output-sort={sort}&maxoutput={list_num}"

print("url :", url)

# %% code 342.
import json
import requests

response = requests.get(url, timeout=60)
data = response.json()          # JSON 응답을 파이썬 딕셔너리로

# %% code 343.
print("type(data) :", type(data))
print("data.keys() :", list(data.keys()))

# %% code 344.
print(data['obs_constraints'])
print(data['sb_constraints'])
print(data['fields'])
print(data['data'][0])            # 첫 행(소행성 한 개)만
print(type(data['fields']))
print(len(data['fields']))
print(len(data['data'][0]))
print(len(data['data']))          # 행(소행성) 수

# %% code 345.
import pandas as pd

df = pd.DataFrame.from_dict(data['data'])
df = df.set_axis((data['fields']), axis=1)
df['OBSdate(UT)'] = obs_date
print("len(df) :", len(df))
df.head()                         # 앞의 5행만 표시

# %% code 346.
df.to_csv(str(proj_dir/ f'asteroid_{obs_date}.csv'))

# %% code 347.
url_neo = ("https://ssd-api.jpl.nasa.gov/sbwobs.api"
           f"?sb-kind=a&sb-group=neo&mpc-code={mpc_code}&obs-time={obs_datetime}"
           "&elev-min=30&vmag-max=18&output-sort=vmag&maxoutput=20")
print("url_neo :", url_neo)

data_neo = requests.get(url_neo, timeout=60).json()
if data_neo.get("data"):
    df_neo = pd.DataFrame(data_neo["data"], columns=data_neo["fields"])
    print(f"관측 가능한 근지구소행성 {len(df_neo)}개 (밝은 순)")
    display(df_neo[["Full name", "Transit time", "Vmag", "Topo.range (au)"]])
else:
    print("조건에 맞는 근지구소행성이 없습니다:", data_neo.get("message", ""))

# %% code 348.
# 여러 날의 관측 후보 목록을 하루 간격으로 받아 CSV로 저장
#############################################
# 변수
mpc_code='P64' # 관측 위치: 경기과학고 천문대, 수원 [코드 P64]

elev_min=60
time_min=15
vmag_min=6
vmag_max=15
list_num=500
sort='trans'
#############################################

# 관측하는 밤의 현지 21시(KST) = UTC 12시로 요청해야 그날 밤 목록을 받음
start_dt    = datetime(2024, 12, 1, 12)
end_dt      = datetime(2024, 12, 3, 12)
dt = 1

dts = [dt for dt in datetime_range(start_dt, end_dt, timedelta(days=dt))]

print("len(dts):", len(dts))
print("dts", dts)

df_all = pd.DataFrame()

for dt in dts :
    obs_datetime = dt.strftime('%Y-%m-%dT%H:%M:%S')  # 날짜와 시간 사이에 구분자 T를 넣는 것 잊지 말 것
    obs_date = dt.strftime('%Y%m%d')

    # API 주소 정의
    url = 'https://ssd-api.jpl.nasa.gov/sbwobs.api'

    # 이 API 요청에 맞는 주소 만들기
    url += f"?sb-kind=a&mpc-code={mpc_code}&obs-time={str(obs_datetime)}&elev-min={elev_min}&time-min={time_min}"
    url += f"&vmag-max={vmag_max}&vmag-min={vmag_min}&optical=true&fmt-ra-dec=true&mag-required=true&output-sort={sort}&maxoutput={list_num}"

    # API 요청을 보내고 JSON 응답 해석
    response = requests.get(url, timeout=60)
    try:
        data = json.loads(response.text)
    except ValueError:
        print("Unable to decode JSON results")

    df = pd.DataFrame.from_dict(data['data'])
    df = df.set_axis((data['fields']), axis=1)
    df['OBSdate(UT)'] = obs_date
    print(f"obs_datetime : {obs_datetime} -> {len(df)}개")

    df.to_csv(str(proj_dir/f"asteroid_{dt.strftime('%Y%m%d')}.csv"))

    df_all = pd.concat([df_all, df], axis = 0)

df_all.reset_index(inplace=True)
print("len(df_all) :", len(df_all))

df_all.to_csv(str(proj_dir/f"asteroid_{dts[0].strftime('%Y%m%d')}-{dts[-1].strftime('%Y%m%d')}.csv"))
df_all.head()

# %% code 349.
#print("df :", df)
#print("df['Full name'] :", df['Full name'])
print("df['Full name'][0] :", df['Full name'][0])

#import re
#asteroid_names = re.findall('\(([^)]+)', df['Full name'][0]) #extracts string in bracket()
#print (asteroid_names[0])

asteroid_id = df['Full name'][0].split(" ")[0]   # 이름 앞의 번호만 잘라 내기
print("asteroid_id :", asteroid_id)
obs_date = df['OBSdate(UT)'][0]

# %% code 350.
from astroquery.mpc import MPC

# %% code 351.
t_start = Time(f"{obs_date[:4]}-{obs_date[4:6]}-{obs_date[6:]} 09:00:00")   # KST 18시 = UTC 09시
eph = MPC.get_ephemeris(asteroid_id, location='P64', start=t_start, number=15,
                        ra_format={'sep': ':', 'unit': 'hourangle',
                                   'precision': 1},
                        dec_format={'sep': ':', 'precision': 0}, step='1h')
print("type(eph): ", type(eph))
print("eph: ", eph)

# %% code 352.
print(f"Proper motion: {eph['Proper motion'].quantity.to('arcmin/h').max():.03f}")

# %% code 353.
from astropy.coordinates import SkyCoord, AltAz, get_sun, get_body
import matplotlib.dates as mdates

site = EarthLocation(lon=127.0*u.deg, lat=37.3*u.deg, height=50*u.m)   # P64 관측지
t_eph = Time(eph['Date'])
c_ast = SkyCoord(eph['RA'], eph['Dec'], unit=(u.hourangle, u.deg))
aa_ast = c_ast.transform_to(AltAz(obstime=t_eph, location=site))

# 태양과 달은 10분 간격으로 계산
t_fine = t_eph[0] + np.linspace(0, (t_eph[-1] - t_eph[0]).to_value(u.h), 85)*u.h
frame_fine = AltAz(obstime=t_fine, location=site)
alt_sun = get_sun(t_fine).transform_to(frame_fine).alt
alt_moon = get_body("moon", t_fine, site).transform_to(frame_fine).alt

kst = lambda t: [d.replace(tzinfo=None) for d in t.to_datetime(timezone=KST)]   # 가로축은 KST
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.plot(kst(t_eph), aa_ast.alt.deg, "o-", color="tab:blue", label=f"{asteroid_id} (소행성)")
ax.plot(kst(t_fine), alt_sun.deg, color="tab:orange", label="태양")
ax.plot(kst(t_fine), alt_moon.deg, "--", color="gray", label="달")
ax.fill_between(kst(t_fine), -90, 90, where=alt_sun.deg < -18, color="k", alpha=0.08,
                label="천문박명 이후(태양 고도 < −18°)")
ax.axhline(30, color="tab:red", ls=":", label="고도 30°")
ax.set_ylim(-30, 90)
ax.set_xlabel(f"한국 표준시 (관측일 {obs_date})")
ax.set_ylabel("고도 (°)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H시"))
ax.legend(fontsize=8, loc="upper right")
ax.grid(alpha=0.3)
ax.set_title("관측지(P64)에서 본 고도 변화")
plt.tight_layout()
plt.show()

i_max = int(np.argmax(aa_ast.alt.deg))
print(f"가장 높을 때: {kst(t_eph)[i_max]:%m-%d %H:%M} KST, 고도 {aa_ast.alt.deg[i_max]:.1f}°, "
      f"방위 {aa_ast.az.deg[i_max]:.1f}°")

# %% code 354.
df_eph = eph.to_pandas()
df_eph['Asteroid ID'] = asteroid_id

df_eph['Asteroid name'] = df['Full name'][0]
df_eph.to_csv(str(proj_dir/ f'asteroid_{asteroid_id}.csv'))
df_eph

# %% code 355.
import re

n_eph = 5                        # 책에서는 앞의 5개만(전체는 len(df))
saved = []
for i, row in df.head(n_eph).iterrows():
    # 정규식으로 소행성 이름 추출
    match = re.match(r"^\d+\s+([^(]+)", row["Full name"])
    if match:
        asteroid_id = match.group(1).strip()
    else:
        asteroid_id = row["Full name"].split(" ")[0]  # 정규식이 실패했을 때의 대비책

    # 위치 예보(ephemeris) 질의
    eph = MPC.get_ephemeris(
        asteroid_id,
        location='P64',
        start=t_start,        # 관측일 저녁 18시(KST)부터
        number=15,
        ra_format={'sep': ':', 'unit': 'hourangle', 'precision': 1},
        dec_format={'sep': ':', 'precision': 0},
        step='1h'
    )

    # 위치 예보 데이터 저장
    df_eph = eph.to_pandas()
    df_eph['Asteroid ID'] = asteroid_id
    df_eph['Asteroid name'] = row["Full name"]
    df_eph.to_csv(str(proj_dir / f"eph_asteroid_{asteroid_id}.csv"))
    saved.append(asteroid_id)

print(f"위치 예보 {len(saved)}개 저장(목록 {len(df)}개 중):", ", ".join(saved))
