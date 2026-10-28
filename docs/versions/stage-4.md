# 📚 최종/4차

최종 앙상블의 단일 프레임 표시와 문서 PDF 렌더 작업을 보관합니다.

- [근거 자료](../../%EC%B5%9C%EC%A2%85/4%EC%B0%A8/_%EC%9E%91%EC%97%85/make_frame.py)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

3차 모델의 출력과 문서를 설명 자료로 정리한 단계입니다.


## 🧩 주요 내용

- make_frame은 selected_model의 ensemble/policy/conf로 첫 영상 프레임을 예측하고 사람 상단 영역에 블러를 적용한 설명 PNG를 만듭니다.
- 그림에는 단일 프레임 기능 확인·투기 사건 판정 결과 아님을 명시하고 test_metrics_recomputed를 False로 기록합니다.
- render_with_word는 문서 렌더러의 PDF 변환을 Word 호출로 연결합니다. 학습이나 테스트 지표 계산 코드가 아닙니다.

## 🔄 자료 구성

3차 모델의 단일 프레임 결과와 문서를 정리했습니다.

## 📍 관련 자료

- [최종/4차/_작업/make_frame.py](../../%EC%B5%9C%EC%A2%85/4%EC%B0%A8/_%EC%9E%91%EC%97%85/make_frame.py) · `pred=predict` · 11
- [최종/4차/_작업/make_frame.py](../../%EC%B5%9C%EC%A2%85/4%EC%B0%A8/_%EC%9E%91%EC%97%85/make_frame.py) · `test_metrics_recomputed` · 24
- [최종/4차/_작업/render_with_word.py](../../%EC%B5%9C%EC%A2%85/4%EC%B0%A8/_%EC%9E%91%EC%97%85/render_with_word.py) · `def native_word` · 10

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 
