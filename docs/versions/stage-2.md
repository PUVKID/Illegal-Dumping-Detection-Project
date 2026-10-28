# 📚 2차

봉투·낱개 쓰레기 분류와 배경 변화·사람 체류를 결합하는 노트북입니다.

- [근거 자료](../../2%EC%B0%A8/illegal_dumping_detector.ipynb)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

노트북의 설정과 데이터 조건을 직접 확인해 사용합니다.

## 🧩 설정과 차이

이 노트북은 봉투와 낱개 쓰레기 분류용으로 `yolov8n.pt`에서 시작하며, 영상 처리 흐름도 함께 담습니다. 1차의 한 클래스 재학습과 출력 역할이 다릅니다.


## 🧩 구체적으로 살펴볼 내용

- YOLOv8n에서 50 epoch 학습을 구성합니다. 1차의 YOLOv8m·150 epoch와 초기 모델·학습 조건이 다릅니다.
- DualBackgroundSubtractor와 ChangeTracker로 지속 변화를 추적하며 사람 탐지·근접·체류 조건으로 후보를 연결합니다.
- 합성 프레임·더미 모델 검사 코드도 포함합니다. 코드 존재와 실제 CCTV 행위 정확도 검증 완료는 다릅니다.

## 🔄 앞선 자료와의 관계

학습 모델만 교체한 판이 아니라 영상 사건 후보의 구성 방식이 달라집니다. 가까운 사람과 물체를 연결하는 휴리스틱을 행위 정답으로 보지 않습니다.

## 📍 파일 안에서 확인하기

- [2차/illegal_dumping_detector.ipynb](../../2%EC%B0%A8/illegal_dumping_detector.ipynb) · `EPOCHS = 50` · 셀 6 소스 3행
- [2차/illegal_dumping_detector.ipynb](../../2%EC%B0%A8/illegal_dumping_detector.ipynb) · `def run_realtime_dumping_pipeline` · 셀 22 소스 6행
- [2차/illegal_dumping_detector.ipynb](../../2%EC%B0%A8/illegal_dumping_detector.ipynb) · `def _make_synthetic_frames` · 셀 26 소스 5행

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 문서와 코드의 정적 대조이며, 새 학습·추론·장치 측정·공격 실행 결과는 아닙니다.
