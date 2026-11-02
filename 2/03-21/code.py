# 지구과학 데이터 사이언스 2 | III-01. 은하의 분류와 특이 은하
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-1.
import time
from io import StringIO, BytesIO
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from PIL import Image

SKY = "https://skyserver.sdss.org/dr18/SkyServerWS"

def get(url, params=None, tries=3):
    for k in range(tries):
        try:
            r = requests.get(url, params=params, timeout=180)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if k == tries - 1:
                raise
            time.sleep(5)

def sql(query, name):
    """SDSS SkyServer에 SQL을 보내 결과를 DataFrame으로 받기(name.csv로 저장)."""
    f = Path(proj_dir) / f"{name}.csv"
    if not f.exists():
        text = get(f"{SKY}/SearchTools/SqlSearch",
                   {"cmd": query, "format": "csv"}).text
        f.write_text(text, encoding="utf-8")
    return pd.read_csv(f, skiprows=1)

def cutout(ra, dec, scale, name, size=400):
    """SDSS 컬러 사진(gri 합성) 받기. scale은 화소당 각초."""
    f = Path(proj_dir) / f"img_{name}.jpg"
    if not f.exists():
        r = get(f"{SKY}/ImgCutout/getjpeg",
                {"ra": ra, "dec": dec, "scale": scale, "width": size, "height": size})
        f.write_bytes(r.content)
    return Image.open(f)

# %% code Ⅲ-2.
galaxies = pd.DataFrame([
    ("M87", 187.7059, 12.3911, 2.0, "E0", "타원"),
    ("M49", 187.4446, 8.0004, 2.0, "E2", "타원"),
    ("NGC 5866", 226.6229, 55.7633, 1.2, "S0", "렌즈형"),
    ("M65", 169.7330, 13.0923, 1.8, "Sa", "나선"),
    ("NGC 4565", 189.0866, 25.9877, 2.6, "Sb(옆모습)", "나선"),
    ("M51", 202.4696, 47.1952, 2.4, "Sbc", "나선"),
    ("M101", 210.8023, 54.3489, 3.6, "Scd", "나선"),
    ("M95", 160.9906, 11.7037, 1.6, "SBb", "막대 나선"),
    ("M109", 179.3998, 53.3745, 1.8, "SBbc", "막대 나선"),
    ("NGC 4449", 187.0463, 44.0936, 1.4, "IBm", "불규칙"),
    ("M82", 148.9685, 69.6797, 2.2, "I0", "불규칙"),
], columns=["name", "ra", "dec", "scale", "hubble", "kind"])

order = np.random.default_rng(7).permutation(len(galaxies))   # 순서 섞기
fig, axes = plt.subplots(3, 4, figsize=(7.5, 5.8))
for ax, k in zip(axes.ravel(), order):
    g = galaxies.iloc[k]
    ax.imshow(cutout(g.ra, g.dec, g.scale, g["name"].replace(" ", "")))
    ax.set_title(f"은하 {list(order).index(k) + 1}", fontsize=12)
    ax.axis("off")
axes.ravel()[-1].axis("off")
plt.tight_layout()
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_01")
plt.show()

# %% code Ⅲ-3.
answer = pd.DataFrame({"은하": [list(order).index(k) + 1 for k in range(len(galaxies))],
                       "이름": galaxies["name"], "허블 형": galaxies["hubble"], "종류": galaxies["kind"]})
answer.sort_values("은하").reset_index(drop=True)

# %% code Ⅲ-4.
place = {  # 이름: (x, y) — 그림 좌표(0~1)
    "M87": (0.03, 0.42), "M49": (0.16, 0.42), "NGC 5866": (0.31, 0.42),
    "M65": (0.47, 0.70), "M51": (0.62, 0.70), "M101": (0.77, 0.70),
    "M95": (0.47, 0.14), "M109": (0.62, 0.14), "NGC 4449": (0.88, 0.42),
}
fig = plt.figure(figsize=(7.5, 3.8))
bg = fig.add_axes([0, 0, 1, 1])
bg.axis("off")
bg.plot([0.08, 0.40], [0.53, 0.53], color="gray", lw=4)           # 손잡이
bg.plot([0.40, 0.48, 0.92], [0.53, 0.80, 0.80], color="gray", lw=4)  # 위 갈래
bg.plot([0.40, 0.48, 0.77], [0.53, 0.25, 0.25], color="gray", lw=4)  # 아래 갈래
for name, (x, y) in place.items():
    g = galaxies.set_index("name").loc[name]
    ax = fig.add_axes([x, y, 0.13, 0.22])
    ax.imshow(cutout(g.ra, g.dec, g.scale, name.replace(" ", "")))
    ax.set_title(f"{name} ({g.hubble})", fontsize=10)
    ax.axis("off")
for text, (x, y) in {"타원 은하 E": (0.10, 0.36), "렌즈형 S0": (0.33, 0.36), "나선 은하 S (a→c)": (0.80, 0.84),
                     "막대 나선 은하 SB": (0.79, 0.21), "불규칙 은하 Irr": (0.90, 0.36)}.items():
    bg.text(x, y, text, fontsize=13, weight="bold", ha="left")
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_02")
plt.show()

# %% code Ⅲ-5.
zoo = sql("""
SELECT TOP 20000 g.objid, g.ra, g.dec, g.spiral, g.elliptical, s.z,
       p.modelMag_u, p.modelMag_g, p.modelMag_r, p.extinction_u, p.extinction_r,
       p.petroR50_r, p.petroR90_r
FROM zooSpec AS g
JOIN SpecObj AS s ON s.specObjID = g.specobjid
JOIN PhotoObj AS p ON p.objID = g.objid
WHERE s.z BETWEEN 0.02 AND 0.08 AND (g.spiral = 1 OR g.elliptical = 1)
""", "galaxyzoo_sample")
zoo["type"] = np.where(zoo["elliptical"] == 1, "타원", "나선")
print(zoo["type"].value_counts())

# %% code Ⅲ-6.
from astropy.cosmology import FlatLambdaCDM

cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
zoo["u_r"] = (zoo["modelMag_u"] - zoo["extinction_u"]) - (zoo["modelMag_r"] - zoo["extinction_r"])
zoo["conc"] = zoo["petroR90_r"] / zoo["petroR50_r"]
d_pc = cosmo.luminosity_distance(zoo["z"].values).to("pc").value
zoo["M_r"] = zoo["modelMag_r"] - zoo["extinction_r"] - 5 * np.log10(d_pc / 10)
zoo = zoo[(zoo["u_r"].between(0.5, 4)) & (zoo["conc"].between(1.5, 4.5))].copy()
zoo.groupby("type")[["u_r", "conc", "M_r"]].median().round(2)

# %% code Ⅲ-7.
colors = {"타원": "tomato", "나선": "royalblue"}
fig, ax = plt.subplots(1, 2, figsize=(7.5, 2.6))
for t, c in colors.items():
    sub = zoo[zoo["type"] == t]
    ax[0].hist(sub["u_r"], bins=np.arange(0.5, 4.01, 0.05), density=True,
               alpha=0.55, color=c, label=f"{t} ({len(sub):,})")
    ax[1].hist(sub["conc"], bins=np.arange(1.5, 4.51, 0.05), density=True,
               alpha=0.55, color=c, label=t)
ax[0].set_xlabel("색지수 u − r (클수록 붉음)")
ax[1].set_xlabel("집중도 R90 / R50 (클수록 중심에 빛이 몰림)")
for a in ax:
    a.set_ylabel("비율")
    a.legend()
    a.grid(alpha=0.3)
ax[0].set_title("은하의 색")
ax[1].set_title("밝기의 집중도")
plt.tight_layout()
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_03")
plt.show()

# %% code Ⅲ-8.
fig, ax = plt.subplots(figsize=(7.5, 4.3))
for t, c in [("나선", "royalblue"), ("타원", "tomato")]:
    sub = zoo[zoo["type"] == t]
    ax.scatter(sub["M_r"], sub["u_r"], s=2, alpha=0.25, color=c, label=t)
ax.invert_xaxis()
ax.set_xlim(-18, -23.5)
ax.set_ylim(0.8, 3.6)
ax.set_xlabel("r 필터 절대 등급 M_r (왼쪽일수록 어두움)")
ax.set_ylabel("색지수 u − r")
ax.text(-22.8, 3.0, "붉은 계열\n(red sequence)", color="darkred", fontsize=11)
ax.text(-19.0, 1.25, "푸른 구름\n(blue cloud)", color="navy", fontsize=11)
ax.legend(markerscale=6)
ax.grid(alpha=0.3)
ax.set_title("은하의 색-등급도 (갤럭시 주 형태 분류)", fontsize=11)
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_04")
plt.show()

# %% code Ⅲ-9.
def rule(df, cut_color, cut_conc):
    return np.where((df["u_r"] > cut_color) & (df["conc"] > cut_conc), "타원",
                    "나선")

results = []
for cc in np.arange(1.8, 3.01, 0.1):
    for ck in np.arange(2.2, 3.21, 0.1):
        pred = rule(zoo, cc, ck)
        acc = (pred == zoo["type"]).mean()
        # 두 종류의 수가 크게 다르므로 종류별 정확도의 평균도 확인
        bal = np.mean([(pred[zoo["type"] == t] == t).mean() for t in ("타원",
                                                                      "나선")])
        results.append((round(cc, 1), round(ck, 1), acc, bal))
res = pd.DataFrame(results,
                   columns=["색 기준", "집중도 기준", "정확도", "균형 정확도"])
best = res.loc[res["균형 정확도"].idxmax()]
print("가장 좋은 기준:", best.round(3).to_dict())

pred = rule(zoo, best["색 기준"], best["집중도 기준"])
pd.crosstab(zoo["type"], pred, rownames=["갤럭시 주 분류"],
            colnames=["규칙의 예측"], margins=True)

# %% code Ⅲ-10.
from astropy.io import fits

spectra = [  # (이름, plate, mjd, fiber, z)
    ("타원 은하", 1665, 52976, 518, 0.0214),
    ("별 생성 나선 은하", 539, 52017, 194, 0.0351),
    ("세이퍼트은하(1형, 활동 은하핵)", 1820, 54208, 373, 0.0337),
    ("퀘이사", 487, 51943, 391, 0.4869),
]
LINES = {"Hβ": 4861, "[OIII]": 5007, "Hα": 6563, "[NII]": 6584, "Mg II": 2798,
         "Hγ": 4341}

def spectrum(plate, mjd, fiber):
    f = Path(proj_dir) / f"spec-{plate:04d}-{mjd}-{fiber:04d}.fits"
    if not f.exists():
        url = (f"https://data.sdss.org/sas/dr17/sdss/spectro/redux/26/spectra/lite/{plate:04d}/"
               f"spec-{plate:04d}-{mjd}-{fiber:04d}.fits")
        f.write_bytes(get(url).content)
    with fits.open(f) as h:
        d = h[1].data
        return 10 ** d["loglam"], d["flux"]

fig, axes = plt.subplots(4, 1, figsize=(7.5, 6.6), sharex=False)
for ax, (name, plate, mjd, fiber, z) in zip(axes, spectra):
    wave, flux = spectrum(plate, mjd, fiber)
    rest = wave / (1 + z)
    smooth = pd.Series(flux).rolling(5, center=True).mean()
    ax.plot(rest, smooth, color="k", lw=0.7)
    top = np.nanpercentile(smooth, 99.7)
    for line, lam in LINES.items():
        if rest.min() < lam < rest.max():
            ax.axvline(lam, color="crimson", ls=":", lw=0.8)
            ax.text(lam, top * (0.9 if line in ("[OIII]", "[NII]") else 1.02), line,   # 가까운 두 선은 높이를 달리
                    color="crimson", fontsize=9,
                    ha="center")
    ax.set_ylim(0, top * 1.15)
    ax.set_ylabel("밝기")
    ax.set_title(f"{name} (z = {z})", fontsize=11, loc="left")
    ax.grid(alpha=0.3)
axes[-1].set_xlabel("정지 파장 (Å)")
plt.tight_layout()
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_05")
plt.show()

# %% code Ⅲ-11.
bpt = sql("""
SELECT TOP 20000 l.h_alpha_flux, l.h_beta_flux, l.oiii_5007_flux, l.nii_6584_flux, s.z
FROM galSpecLine AS l JOIN SpecObj AS s ON s.specObjID = l.specObjID
WHERE s.z BETWEEN 0.02 AND 0.2
  AND l.h_alpha_flux > 5 * l.h_alpha_flux_err AND l.h_beta_flux > 3 * l.h_beta_flux_err
  AND l.oiii_5007_flux > 3 * l.oiii_5007_flux_err AND l.nii_6584_flux > 3 * l.nii_6584_flux_err
""", "bpt_sample")
x = np.log10(bpt["nii_6584_flux"] / bpt["h_alpha_flux"])
y = np.log10(bpt["oiii_5007_flux"] / bpt["h_beta_flux"])
ok = np.isfinite(x) & np.isfinite(y)
x, y = x[ok], y[ok]

kauff = lambda v: 0.61 / (v - 0.05) + 1.30      # v < 0.05
kewley = lambda v: 0.61 / (v - 0.47) + 1.19     # v < 0.47
sf = (x < 0.05) & (y < kauff(x))
agn = (x >= 0.47) | (y > kewley(x))
comp = ~sf & ~agn
seyfert = agn & (y > 1.05 * x + 0.45)
liner = agn & ~seyfert

fig, ax = plt.subplots(figsize=(5.0, 4.4))
for mask, c, label in [(sf, "royalblue", "별 생성 은하"), (comp, "seagreen", "중간(복합)"),
                       (seyfert, "crimson", "세이퍼트"), (liner, "darkorange", "라이너")]:
    ax.scatter(x[mask], y[mask], s=2, alpha=0.3, color=c,
               label=f"{label} {mask.mean() * 100:.0f}%")
v1 = np.linspace(-2, 0.0, 200)
v2 = np.linspace(-2, 0.4, 200)
ax.plot(v1, kauff(v1), "k--", lw=1.2, label="Kauffmann(2003)")
ax.plot(v2, kewley(v2), "k-", lw=1.2, label="Kewley(2001)")
ax.set_xlim(-1.6, 0.6)
ax.set_ylim(-1.2, 1.4)
ax.set_xlabel("log([NII] 6584 / Hα)", fontsize=9)
ax.set_ylabel("log([OIII] 5007 / Hβ)", fontsize=9)
ax.tick_params(labelsize=8)
ax.legend(markerscale=6, fontsize=8)
ax.grid(alpha=0.3)
ax.set_title("BPT 도표 — 방출선 은하 2만 개", fontsize=10)
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_06")
plt.show()

# %% code Ⅲ-12.
zdist = pd.concat([
    sql("SELECT z, class FROM SpecObj WHERE class = 'QSO' AND zWarning = 0 AND fiberID % 25 = 0",
        "redshift_qso"),
    sql("SELECT z, class FROM SpecObj WHERE class = 'GALAXY' AND zWarning = 0 AND fiberID % 100 = 0",
        "redshift_galaxy"),
])

fig, ax = plt.subplots(figsize=(7.5, 3.4))
bins = np.arange(0, 5.01, 0.05)
for cls, c, label in [("GALAXY", "seagreen", "은하"),
                      ("QSO", "purple", "퀘이사")]:
    sub = zdist[zdist["class"] == cls]["z"]
    ax.hist(sub, bins=bins, alpha=0.6, color=c,
            label=f"{label} (중앙값 z = {sub.median():.2f})")
ax.set_xlabel("적색편이 z")
ax.set_ylabel("천체 수")
ax.legend()
ax.grid(alpha=0.3)
zz = np.linspace(0, 5, 200)
tt = cosmo.lookback_time(zz).value
top = ax.secondary_xaxis("top",
                         functions=(lambda z: np.interp(z, zz, tt), lambda t: np.interp(t, tt, zz)))
top.set_xticks([4, 6, 8, 10, 11, 12])   # 가까운 쪽(z < 0.3)은 눈금이 몰리므로 4 Gyr부터
top.set_xlabel("되돌아본 시간 (10억 년, Gyr)")
ax.set_title("은하와 퀘이사의 적색편이 분포", fontsize=11)
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_07")
plt.show()

q = zdist[zdist["class"] == "QSO"]["z"]
print(f"퀘이사 적색편이 중앙값 {q.median():.2f} → 빛이 출발한 지 약 {cosmo.lookback_time(q.median()).value * 10:.0f}억 년")

# %% code Ⅲ-13.
fig, ax = plt.subplots(1, 2, figsize=(7.5, 3.7))
ax[0].imshow(cutout(187.2779, 2.0524, 0.4, "3C273"))
ax[0].set_title("퀘이사 3C 273\n(z = 0.158, 빛이 출발한 지 약 20억 년)")
ax[1].imshow(cutout(187.7059, 12.3911, 0.25, "M87_core"))
ax[1].set_title("전파 은하 M87의 중심부와 제트")
for a in ax:
    a.axis("off")
plt.tight_layout()
du.save_figure(plt.gcf(), proj_dir / f"{proj_dir.name}_08")
plt.show()
