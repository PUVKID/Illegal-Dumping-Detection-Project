# 📚 1차

여러 쓰레기 자료를 한 클래스로 통합해 YOLOv8m을 학습하고 영상 후보를 추적합니다.

- [근거 자료](../../1%EC%B0%A8/illegal_dumping_trash_all_new_datasets.ipynb)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

행위 정답 라벨이 없는 영상의 정지·추적 결과는 검토 후보입니다.

## 🧩 설정과 차이

기본 모델 설정은 `yolov8m.pt`이며 쓰레기 한 클래스 학습과 사람 탐지를 별도로 구성합니다. 모델명과 사람 모델 설명 주석이 서로 다른 부분이 있어 실제 설정 셀을 기준으로 읽습니다.


## 🧩 구체적으로 살펴볼 내용

- 데이터 수집·라벨 통합 뒤 학습·검증·시험 자료를 나누며 기본 학습 epoch는 150입니다.
- 사람 겹침·기존 정지 물체·새 물체와 추적을 사용해 쓰레기 후보를 후처리합니다.

## 🔄 앞선 자료와의 관계

쓰레기 한 클래스 탐지가 중심입니다. 2차의 봉투/낱개 구분 및 사람 체류 기반 절차와 구분합니다.

## 📍 파일 안에서 확인하기

- [1차/illegal_dumping_trash_all_new_datasets.ipynb](../../1%EC%B0%A8/illegal_dumping_trash_all_new_datasets.ipynb) · `EPOCHS = 150` · 셀 1 소스 44행
- [1차/illegal_dumping_trash_all_new_datasets.ipynb](../../1%EC%B0%A8/illegal_dumping_trash_all_new_datasets.ipynb) · `def postprocess_trash` · 셀 20 소스 190행

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 문서와 코드의 정적 대조이며, 새 학습·추론·장치 측정·공격 실행 결과는 아닙니다.
