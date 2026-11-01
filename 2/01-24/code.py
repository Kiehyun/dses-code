# 지구과학 데이터 사이언스 2 | I-04. 코딩 에이전트로 분석 프로젝트 하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 16.
from pathlib import Path

guide = '''# 프로젝트 지침 — 우리 학교 기상 관측 데이터 분석

## 목적
학교 자동기상관측장비(AWS)의 1분 데이터로 월별 기온 · 강수 요약표와 그래프를 만든다.

## 폴더
- data/raw/      : 내려받은 원시 데이터 (읽기만 한다. 절대 고치지 않는다)
- data/clean/    : 전처리한 데이터
- notebooks/     : 분석 노트북
- figures/       : 그림 (PNG, PDF)

## 실행 환경
- conda 환경 dses_Python (파이썬 3.12)에서 실행한다.
- 새 패키지가 필요하면 설치하기 전에 먼저 물어본다.

## 규칙
- 기온은 섭씨(°C), 강수량은 mm로 표기한다.
- 그래프의 축 이름과 제목은 한글로 쓴다.
- 결측값을 지우거나 채울 때는 몇 개를 어떻게 처리했는지 출력한다.

## 마치기 전에 확인할 것
- 노트북을 처음부터 다시 실행해 오류 셀이 없는지 확인한다.
- 바꾼 파일과 이유를 짧게 정리해 보고한다.
'''

(proj_dir / "AGENTS.md").write_text(guide, encoding="utf-8")         # 지침 본문
(proj_dir / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")  # AGENTS.md 불러오기

print((proj_dir / "AGENTS.md").read_text(encoding="utf-8"))
print("--- CLAUDE.md ---")
print((proj_dir / "CLAUDE.md").read_text(encoding="utf-8"))

# %% code 17.
import json

def check_notebook(path):
    nb = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    errors, not_run = [], 0
    for c in code_cells:
        source = "".join(c["source"]).strip()
        for out in c.get("outputs", []):
            if out.get("output_type") == "error":
                errors.append(out.get("ename", "Error"))
        if source and c.get("execution_count") is None:
            not_run += 1
    return {"노트북": Path(path).name, "코드 셀": len(code_cells),
            "오류 셀": len(errors), "실행 안 한 셀": not_run,
            "오류 종류": ", ".join(sorted(set(errors)))}

nb_paths = sorted(Path.cwd().glob("*.ipynb"))      # 지금 폴더의 노트북 목록
if nb_paths:
    display(check_notebook(nb_paths[0]))           # 첫 노트북으로 시험
else:
    print("이 폴더에는 노트북 파일(.ipynb)이 없습니다.")

# %% code 18.
import pandas as pd

folder = Path.cwd()                                  # 점검할 폴더(지금 노트북이 있는 곳)
nb_paths = sorted(folder.glob("*.ipynb"))
if nb_paths:
    report = pd.DataFrame([check_notebook(p) for p in nb_paths])
    report = report.sort_values(["오류 셀", "실행 안 한 셀"], ascending=False,
                                ignore_index=True)
    display(report)
    print(f"오류가 남은 노트북: {(report['오류 셀'] > 0).sum()}개")
else:
    print(f"{folder.name} 폴더에는 노트북 파일(.ipynb)이 없습니다.")
