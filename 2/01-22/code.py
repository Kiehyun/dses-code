# 지구과학 데이터 사이언스 2 | I-02. Miniconda와 VS Code로 작업 환경 만들기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 10.
import sys
from importlib.metadata import version, PackageNotFoundError

print("실행 중인 파이썬:", sys.executable)          # 경로에 envs\dses_Python 포함 여부 확인
print("파이썬 버전     :", sys.version.split()[0])

packages = ["numpy", "pandas", "matplotlib", "scipy", "astropy", "photutils",
            "cartopy", "xarray", "netCDF4", "metpy", "gsw", "folium"]
for name in packages:
    try:
        print(f"  {name:<11} {version(name)}")
    except PackageNotFoundError:
        print(f"  {name:<11} 설치 안 됨 — conda install {name.lower()}")

# %% code 11.
import matplotlib.pyplot as plt
import os

years = [1980, 1990, 2000, 2010, 2020, 2024]
co2 = [338.9, 354.5, 369.7, 389.9, 414.2, 424.6]     # 마우나로아 연평균 CO2 농도(ppm)

fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.plot(years, co2, marker="o")
ax.set_xlabel("연도")
ax.set_ylabel("CO$_2$ 농도 (ppm)")
ax.set_title("마우나로아 대기 중 CO$_2$ 연평균 농도")
ax.grid(True, alpha=0.4)
du.save_figure(fig, os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()
