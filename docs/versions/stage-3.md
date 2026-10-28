# 📚 최종/3차

데이터 준비, 검증 선택, 고정 테스트, 클린뷰 영상 실행을 분리합니다.

- [근거 자료](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/train_round3.py)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

고정 테스트 평가는 선택된 모델과 정책을 고정한 뒤 수행하도록 구성합니다.


## 🧩 주요 내용

- data_pipeline은 자료 준비와 고정 holdout 검사를, train_round3는 학습 실행을 맡습니다.
- inference의 공통 predict/evaluate와 임계값 선택을 영상 루프의 detector.detect와 구분합니다.
- detector의 Events와 detect가 시간에 따른 물체·사람 상태와 영상 결과를 구성합니다. 정지·이탈 규칙의 후보 출력은 행위 정답 라벨 기반 정확도가 아닙니다.

## 🔄 자료 구성

1·2차 단일 노트북에서 데이터·학습·추론·화면을 파일별로 분리한 단계입니다. 검증으로 선택한 정책과 고정 시험 결과의 역할을 구분합니다.

## 📍 관련 자료

- [최종/3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py) · `def verify_holdout` · 20
- [최종/3차/클린뷰/inference.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/inference.py) · `def choose_threshold` · 42
- [최종/3차/클린뷰/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py) · `def detect` · 52

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 
