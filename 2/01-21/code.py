# 지구과학 데이터 사이언스 2 | I-01. 공통 함수 모듈 dses_utils 이해하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅰ-1.
# 필요한 모듈 정의 (버전 명시 가능)
packages_str = "numpy, pandas, matplotlib, version_information"

# %% code Ⅰ-2.
# 공통 함수(dses_utils) 불러오기 — 코랩/로컬 모두 동작(별도 설치 불필요)
import os, sys, importlib, urllib.request

_url = "https://raw.githubusercontent.com/Kiehyun/dses_utils/main/dses_utils.py"
try:
    _new = urllib.request.urlopen(_url, timeout=10).read()   # 최신 내용을 메모리로 받아옴
    _old = open("dses_utils.py", "rb").read() if os.path.exists("dses_utils.py") else None
    if _new != _old:                                          # 내용이 다를 때만 덮어씀
        with open("dses_utils.py", "wb") as _f:
            _f.write(_new)
        if "dses_utils" in sys.modules:                       # 이미 불러왔다면 다시 불러옴
            importlib.reload(sys.modules["dses_utils"])
except Exception:
    pass  # 인터넷이 안 되면 기존에 받아둔 dses_utils.py 사용

import dses_utils as du
du.check_and_install(packages_str)              # 패키지 확인·설치와 버전 출력
du.set_korean_font()                            # 그래프의 한글 글꼴 설정
proj_dir = du.make_project_dir(du.current_notebook_name())   # 데이터 저장 폴더 생성

# %% code Ⅰ-3.
src = '''"""단위 변환 함수 모음(연습용 모듈)."""


def c_to_k(c):
    """섭씨온도(°C)를 켈빈(K)으로 바꾼다."""
    return c + 273.15


def k_to_c(k):
    """켈빈(K)을 섭씨온도(°C)로 바꾼다."""
    return k - 273.15
'''
mod_path = proj_dir / "my_units.py"
mod_path.write_text(src, encoding="utf-8")
print(mod_path, "저장됨")

# %% code Ⅰ-4.
import sys
from pathlib import Path

sys.path.insert(0, str(proj_dir))     # 모듈을 찾을 폴더를 맨 앞에 더한다
print("맨 앞 경로:", sys.path[0])

import my_units

print("불러온 파일:", Path(my_units.__file__).name)
print("15 °C =", my_units.c_to_k(15.0), "K")
help(my_units.k_to_c)

# %% code Ⅰ-5.
import importlib

print("sys.modules에 있음:", "my_units" in sys.modules)

mod_path.write_text(src + '''

def c_to_f(c):
    """섭씨온도(°C)를 화씨온도(°F)로 바꾼다."""
    return c * 9 / 5 + 32
''', encoding="utf-8")

import my_units                      # 기억해 둔 모듈을 그대로 돌려준다
print("import 뒤 c_to_f 있음:", hasattr(my_units, "c_to_f"))

importlib.reload(my_units)            # 파일을 다시 읽어 새로 실행한다
print("reload 뒤 c_to_f 있음:", hasattr(my_units, "c_to_f"))
print("15 °C =", my_units.c_to_f(15.0), "°F")

# %% code Ⅰ-6.
import inspect

print("불러온 파일:", Path(du.__file__).name)
for name, f in inspect.getmembers(du, inspect.isfunction):
    if name.startswith("_") or f.__module__ != du.__name__:
        continue
    first = (f.__doc__ or "").strip().splitlines()[0]   # 설명 문자열의 첫 줄
    print(f"{name:21} {first}")

print()
print("download의 인자:", inspect.signature(du.download))

# %% code Ⅰ-7.
import importlib.util

for pypi, mod in list(du._PYPI_TO_IMPORT.items())[:5]:
    print(f"{pypi:16} → import {mod}")

print()
for mod in ["numpy", "pandas", "sklearn", "없는_패키지"]:
    found = importlib.util.find_spec(mod) is not None
    print(f"{mod:12} {'설치됨' if found else '없음'}")
print("\n지금 쓰는 파이썬 환경:", Path(sys.prefix).name)   # 가상환경 폴더 이름

# %% code Ⅰ-8.
import pandas as pd

df = pd.DataFrame({
    "월": range(1, 13),
    "평균기온(°C)": [-2.4, 0.4, 5.7, 12.5, 17.8, 22.2, 24.9, 25.7, 21.2, 14.8,
                     7.2, 0.4],
})
csv_path = proj_dir / "월평균기온_예시.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")

fpaths = du.list_files(proj_dir, "csv")
lines = du.preview_text(fpaths[0], n=5)

# %% code Ⅰ-9.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.plot(df["월"], df["평균기온(°C)"], "o-")
ax.set_xticks(range(1, 13))
ax.set_xlabel("월")
ax.set_ylabel("평균기온 (°C)")
ax.set_title("월평균기온 (예시 데이터)")
ax.grid(alpha=0.3)
saved = du.save_figure(fig, proj_dir / "월평균기온_예시")
plt.show()
