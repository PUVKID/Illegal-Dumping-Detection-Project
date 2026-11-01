'use strict';
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const path = require('node:path');
const f = require('../web/presentation.js');
let checked = 0;
function test(name, run) { run(); checked++; console.log('통과 · ' + name); }
test('GiB는 이진 단위이며 누락은 미측정', () => { assert.equal(f.gib(1024 ** 3), '1.00 GiB'); assert.equal(f.gib(null), '미측정'); });
test('파일 비율과 미측정 구분', () => { assert.equal(f.percent(25), '25.0%'); assert.equal(f.percent(null), '—'); });
test('미측정 성능과 실제 0 구분', () => { assert.equal(f.metric(null), '미측정'); assert.equal(f.metric(0), '0.0%'); });
test('예측하지 못한 시간은 추정 불가', () => assert.equal(f.duration(null), '추정 불가'));
const make = () => ({job:'a',source:'official',file:'one.zip',file_bytes:1000,downloaded_bytes:100,updated:100,state:'running'});
test('첫 표본은 속도·ETA를 만들지 않음', () => assert.deepEqual(f.sampler()(make()), {speed:null,eta:null}));
test('두 저장 시각으로 실측하며 동일 표본 중복 제외', () => { const read=f.sampler(), a=make(); read(a); const b={...a,updated:110,downloaded_bytes:200}; assert.deepEqual(read(b), {speed:10,eta:80}); assert.deepEqual(read(b), {speed:10,eta:80}); });
test('파일 변경 시 표본 초기화', () => { const read=f.sampler(), a=make(); read(a); read({...a,updated:110,downloaded_bytes:200}); assert.deepEqual(read({...a,file:'two.zip',updated:120}), {speed:null,eta:null}); });
test('오래된 기록과 감소한 바이트는 추정하지 않음', () => { const read=f.sampler(), a=make(); read(a); assert.equal(read({...a,stale:true}).speed,null); read(a); assert.equal(read({...a,updated:110,downloaded_bytes:50}).speed,null); });
for (const file of ['web/app.js','web/scene.js','web/presentation.js']) test(file + ' 구문', () => { const p=spawnSync(process.execPath,['--check',path.resolve(__dirname,'..',file)],{encoding:'utf8'}); assert.equal(p.status,0,p.stderr); });

test('실패에서 새 실행으로 바뀌면 상태 오류만 제거', () => { const n=f.noticeState(); assert.equal(n.apply({job:'old',state:'failed'},'실패 안내'),'실패 안내'); assert.equal(n.apply({job:'new',state:'running'},''),''); });
test('정상에서 실패 전환은 새 상태 안내', () => { const n=f.noticeState(); n.apply({job:'a',state:'running'},''); assert.equal(n.apply({job:'a',state:'failed'},'실패 안내'),'실패 안내'); });
test('사용자 동작 및 네트워크 안내는 회복 중 보존', () => { for(const text of ['영상 업로드 완료','네트워크 오류']) { const n=f.noticeState(); n.apply({job:'a',state:'failed'},'실패 안내'); n.set(text); assert.equal(n.apply({job:'a',state:'failed'},'실패 안내'),text); assert.equal(n.apply({job:'b',state:'running'},''),text); } });
test('실제 완료 단계만 민트·대기 회색·현재 활성·실패·재시도 색 구분', () => { const p={step:2,badge:'진행 중',steps:[{status:'complete'},{status:'complete'},{status:'active'},{status:'pending'}]}; assert.equal(f.stageStyle(p,0).kind,'complete'); assert.equal(f.stageStyle(p,3).kind,'pending'); assert.equal(f.stageStyle(p,2).color,'#00c84f'); assert.equal(f.stageStyle({...p,badge:'실패'},2).kind,'error'); assert.equal(f.stageStyle({...p,retry:true},2).kind,'retry'); });
test('표시 에포크가 없으면 이전 원문 에포크를 사용하지 않음', () => { assert.equal(f.epochText({epoch:null},60),'—'); assert.equal(f.epochText({epoch:3},60),'3 / 60'); });
test('PMREM 사전 블러가 고정 벤더의 표본 상한을 넘지 않음', () => { const fs=require('node:fs'); const scene=fs.readFileSync(path.resolve(__dirname,'../web/scene.js'),'utf8'); const vendor=fs.readFileSync(path.resolve(__dirname,'../web/vendor/three.module.js'),'utf8'); const sigma=Number(scene.match(/pmrem.fromScene\(room,\s*(\.\d+)\)/)[1]); const section=vendor.slice(vendor.indexOf('fromScene( scene, sigma'),vendor.indexOf('this._setSize( size )')); const size=Number(section.match(/size = (\d+),/)[1]); const maximum=Number(vendor.match(/const MAX_SAMPLES = (\d+);/)[1]); const deviations=Number(vendor.match(/const STANDARD_DEVIATIONS = (\d+);/)[1]); const samples=1+Math.floor(deviations*sigma/(Math.PI/(2*(size-1)))); assert.ok(samples<=maximum, samples+' > '+maximum); });
test('다운로드 큐브는 시간에 따라 하강하고 끝에서 위로 재생성', () => { assert.ok(f.dropHeight(100,0)<f.dropHeight(0,0)); assert.ok(f.dropHeight(200,0)<f.dropHeight(100,0)); assert.ok(f.dropHeight(2900,0)>f.dropHeight(2800,0)); });
test('모션 축소 초기값과 동적 변경이 정지 상태를 통지', () => { const events=[]; const m=f.motionPreference(false, value=>events.push(value)); assert.deepEqual(events,[false]); assert.equal(m.changed(true),true); assert.deepEqual(events,[false,true]); assert.equal(m.changed(false),true); assert.equal(m.setPaused(false),false); const reduced=[]; f.motionPreference(true,value=>reduced.push(value)); assert.deepEqual(reduced,[true]); });
test('자원 대기와 기록 없음의 현재 단계도 회색이며 활성으로 표시하지 않음', () => { for (const badge of ['자원 대기','자료 없음','기록 없음','대기']) { const style=f.stageStyle({step:2,badge,steps:[{status:'pending'},{status:'pending'},{status:'active'}]},2); assert.deepEqual(style,{kind:'pending',color:'#c6cecb'}); } });
test('DOM 단계도 3D 상태 판정을 공유해 대기 회색과 기존 상태 의미 유지', () => {
  const p={step:2,badge:'자원 대기',steps:[{status:'complete'},{status:'complete'},{status:'active'},{status:'pending'}]};
  assert.equal(f.stageStyle(p,2).kind,'pending');
  assert.deepEqual(f.stageClasses(p,2),{active:false,complete:false,failed:false,retrying:false,waiting:true});
  assert.equal(f.stageClasses(p,0).complete,true);
  assert.equal(f.stageClasses(p,3).active,false);
  assert.equal(f.stageClasses({...p,badge:'진행 중'},2).active,true);
  assert.equal(f.stageClasses({...p,badge:'실패'},2).failed,true);
  assert.equal(f.stageClasses({...p,badge:'재시도',retry:true},2).retrying,true);
});
console.log('최종 검사 수 ' + checked);
