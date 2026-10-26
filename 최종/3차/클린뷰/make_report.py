"""Run in Docker after round 2 completes. Offline Korean Bold report, honest target status."""
import json,csv,html,shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from data_pipeline import ROOT
APP=Path(__file__).resolve().parent
OUT=ROOT/'report'

def main():
    final=json.loads((ROOT/'final.json').read_text());OUT.mkdir(exist_ok=True)
    font=APP/'fonts/NanumGothic-Bold.ttf';font_manager.fontManager.addfont(str(font))
    plt.rcParams.update({'font.family':font_manager.FontProperties(fname=font).get_name(),'font.weight':'bold','axes.titleweight':'bold','axes.labelweight':'bold','axes.unicode_minus':False,'figure.dpi':150})
    (OUT/'fonts').mkdir(exist_ok=True)
    for name in ('NanumGothic-Bold.ttf','OFL.txt'):shutil.copy2(APP/'fonts'/name,OUT/'fonts'/name)
    test=final['test'];op=test['operating'];m=test['metrics'];selected=final['selected']
    values=[('정밀도',op['precision']),('재현율',op['recall']),('F1',op['f1']),('mAP50',m['metrics/mAP50(B)']),('mAP50–95',m['metrics/mAP50-95(B)'])]
    with (OUT/'최종성능.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['지표','비율','퍼센트','평가조건']);w.writerows((k,v,v*100,'고정 테스트 150장 / 신뢰도는 검증에서 선택') for k,v in values)
    fig,ax=plt.subplots(figsize=(9,4.5));bars=ax.bar([k for k,v in values],[v*100 for k,v in values],color=['#107d71','#107d71','#4b8194','#52709b','#8b9eb7'])
    ax.set_ylim(0,110);ax.set_ylabel('성능 (%)');ax.set_title('3차 고정 테스트셋 최종 성능');ax.axhline(90,color='#c47d28',ls='--',label='정밀도·재현율 목표 90%');ax.legend(loc='upper right')
    for bar,(_,v) in zip(bars,values):ax.text(bar.get_x()+bar.get_width()/2,v*100+2,f'{v*100:.2f}%',ha='center')
    fig.tight_layout();fig.savefig(OUT/'최종성능.png');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.3))
    for run in sorted((ROOT/'runs').glob('*')):
        p=run/'results.csv'
        if not p.exists():continue
        with p.open() as f:rows=[{k.strip():v for k,v in r.items()} for r in csv.DictReader(f)]
        for ax,col,title in zip(axes,['metrics/mAP50(B)','val/box_loss'],['epoch별 검증 mAP50','epoch별 검증 박스 손실']):
            ax.plot([float(r['epoch']) for r in rows],[float(r[col]) for r in rows],label=run.name)
            ax.set_xlabel('Epoch');ax.set_title(title);ax.legend()
    fig.tight_layout();fig.savefig(OUT/'학습곡선.png');plt.close(fig)
    operating=json.loads((ROOT/'evaluation'/('val_'+selected['candidate']+'_'+selected['policy'])/'operating_thresholds.json').read_text())
    fig,ax=plt.subplots(figsize=(8,4));ax.plot([r['threshold'] for r in operating],[r['precision'] for r in operating],label='정밀도');ax.plot([r['threshold'] for r in operating],[r['recall'] for r in operating],label='재현율');ax.axvline(op['threshold'],color='#999',ls='--',label='선택한 신뢰도');ax.set(xlabel='신뢰도 임계값',ylabel='검증 성능',ylim=(0,1.05),title='검증셋에서 정한 운영 임계값');ax.legend();fig.tight_layout();fig.savefig(OUT/'검증임계값.png');plt.close(fig)
    # PR/F1 curves from official AP computation; redraw with bundled Korean font.
    from ultralytics.utils.metrics import DetMetrics
    s=np.load(ROOT/'evaluation/test_final/stats.npz');dm=DetMetrics(names={0:'trash'})
    for k in dm.stats:dm.stats[k]=[s[k]]
    dm.process(plot=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    axes[0].plot(dm.box.px,dm.box.prec_values[0],color='#107d71');axes[0].set(xlabel='재현율',ylabel='정밀도',title='테스트 PR 곡선',xlim=(0,1),ylim=(0,1.05))
    axes[1].plot(dm.box.px,dm.box.f1_curve[0],color='#107d71');axes[1].set(xlabel='신뢰도',ylabel='F1',title='테스트 F1 곡선 · 선택 변경에 사용하지 않음',xlim=(0,1),ylim=(0,1.05))
    fig.tight_layout();fig.savefig(OUT/'테스트곡선.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(5,4));arr=np.array([[op['tp'],op['fp']],[op['fn'],0]])
    ax.imshow(arr,cmap='Greens');ax.set_xticks([0,1],['실제 쓰레기','배경']);ax.set_yticks([0,1],['탐지','놓침']);ax.set_title('탐지 개수 · IoU 0.50')
    for i in range(2):
        for j in range(2):ax.text(j,i,'해당 없음' if i==j==1 else str(arr[i,j]),ha='center',va='center')
    fig.tight_layout();fig.savefig(OUT/'탐지개수.png');plt.close(fig)
    rows=''.join(f'<tr><td>{html.escape(k)}</td><td>{v*100:.2f}%</td></tr>' for k,v in values)
    history=''.join(f"<tr><td>{html.escape(r['name'])}</td><td>{r['epochs']}</td></tr>" for r in final['history'])
    val=json.loads((ROOT/'validation_comparison.json').read_text())
    vrows=''.join(f"<tr><td>{r['candidate']}</td><td>{r['policy']}</td><td>{r['operating']['precision']*100:.2f}%</td><td>{r['operating']['recall']*100:.2f}%</td><td>{r['metrics']['metrics/mAP50(B)']*100:.2f}%</td></tr>" for r in val)
    doc=f'''<!doctype html><html lang="ko"><meta charset="utf-8"><title>클린뷰 3차 최종 보고서</title><style>@font-face{{font-family:Nanum;src:url(fonts/NanumGothic-Bold.ttf);font-weight:700}}*{{box-sizing:border-box;font-family:Nanum,sans-serif;font-weight:700}}body{{max-width:1080px;margin:40px auto;padding:0 25px;color:#243448;background:#f7f9fb;line-height:1.8}}h1{{color:#107d71}}section{{background:white;border:1px solid #e2e7ed;border-radius:16px;padding:25px;margin:20px 0}}table{{border-collapse:collapse;width:100%}}td,th{{text-align:left;padding:10px;border-bottom:1px solid #e7ebee}}img{{max-width:100%;display:block;margin:20px auto}}.note{{color:#68788b}}code{{word-break:break-all}}</style>
    <h1>클린뷰 · 3차 최종 학습 보고서</h1><p>정밀도·재현율 90% 목표: <b>{'달성' if final['target_met'] else '미달성'}</b></p>
    <section><h2>실제 고정 테스트 성능</h2><table><tr><th>지표</th><th>측정값</th></tr>{rows}</table><p>테스트 150장 · IoU 0.50 · 신뢰도 {op['threshold']:.2f} (검증에서 선택) · 탐지 방식 {selected['policy']}</p><img src="최종성능.png"><p class="note">정밀도·재현율은 검증에서 선택한 고정 신뢰도에서 재매칭하여 계산했습니다. mAP는 전체 신뢰도 곡선으로 계산합니다. 분류 정확도나 CCTV 투기 행동 정확도를 뜻하지 않습니다.</p></section>
    <section><h2>학습과 모델 선택</h2><p>YOLO26x와 YOLO26l-P2의 사전학습 가중치에서 시작했습니다. 추가 데이터 학습 뒤 쓰레기 범주와 작은 물체에 집중해 미세 조정했습니다. 검증셋에서 단독·앙상블, 일반·확대 탐지를 비교했습니다.</p><table><tr><th>새 학습 모델</th><th>완료 epoch</th></tr>{history}</table><p>최종 선택: {selected['candidate']} / {selected['policy']}</p><table><tr><th>모델</th><th>방식</th><th>검증 정밀도</th><th>검증 재현율</th><th>검증 mAP50</th></tr>{vrows}</table><img src="학습곡선.png"><img src="검증임계값.png"></section>
    <section><h2>데이터와 검증</h2><p>기존 학습 {final['data']['original_train']}장, SALSA/OpenLitterMap {final['data']['salsa_train']}장, 추가 TACO {final['data']['additional_taco']}장, 도로변 pLitterStreet {final['data']['additional_street']}장, 작은 물체 확대 {final['data']['zoom_images']}장. 확대 사진은 학습 분할의 사진에서만 만들었습니다.</p><p>검증 150장과 테스트 150장의 사진 정체성과 정답을 유지했습니다. 기존 축소본의 SHA-256과 복원한 원본 사진의 SHA-256을 모두 고정했습니다. 이번 평가는 원본 해상도를 사용하므로 이전의 축소 입력 성능과 동일 조건 비교가 아닙니다. 추가 사진은 원본 URL과 pHash 중복 검사를 거쳐 학습에만 넣었습니다. 모든 유사 장면을 완벽히 배제했다는 뜻은 아닙니다.</p><p><a href="https://github.com/alinacherkas/salsa">SALSA 출처와 라이선스</a> · 원본 출처·이미지별 라이선스·중복 제외 내역은 출처 폴더에 보관했습니다.</p></section>
    <section><h2>테스트 곡선과 오류 개수</h2><img src="테스트곡선.png"><img src="탐지개수.png"><p>정밀도·재현율 목표를 달성하지 못했다면 위 수치가 실제 결과입니다. 더 높은 목표에는 추가 라벨 검수와 실제 CCTV 환경의 정답 데이터가 필요할 수 있습니다.</p></section>
    <section><h2>CCTV 앱과 자료 위치</h2><p>물체가 남는 시간, 기존 물체 제외, 주변 사람 이탈 규칙을 적용합니다. 행동 정답 라벨이 없는 CCTV에서는 투기 행동 정확도를 계산하지 않았습니다. </p><p>바탕화면: 월요일 PBL / 3차. 필요한 원본과 영상은 3차로 이동했고, 이전 폴더는 휴지통으로 정리했습니다. 최종 모델, 학습 로그, 데이터 출처, 평가 원자료와 코드가 포함됩니다.</p><p>최종 모델 SHA-256: <code>{html.escape(str(final['best_sha256']))}</code></p></section></html>'''
    (OUT/'3차_최종보고서.html').write_text(doc,encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(final,ensure_ascii=False,indent=2))
    print(str(OUT),flush=True)

if __name__=='__main__':main()
