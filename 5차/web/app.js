'use strict';
const token = new URLSearchParams(location.search).get('token') || '';
const $ = id => document.getElementById(id);
let state = {}, loading = false, pending = false, resultKey = null;
const asset = path => '/asset?token=' + encodeURIComponent(token) + '&path=' + encodeURIComponent(path);
function message(value) { $('message').textContent = value; }
async function api(name, data) {
  const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 65000);
  try {
    const response = await fetch('/api/' + name, {method: data === undefined ? 'GET' : 'POST', headers: {'X-Token': token, 'X-CSRF-Token': token, 'Content-Type': 'application/json'}, body: data === undefined ? undefined : JSON.stringify(data), signal: controller.signal});
    const value = await response.json();
    if (!response.ok || !value.ok) throw Error(value.error || '요청을 처리하지 못했습니다.');
    return value.data;
  } finally { clearTimeout(timer); }
}
function textNode(tag, value) { const element = document.createElement(tag); element.textContent = value; return element; }
function metric(value) { return typeof value === 'number' && Number.isFinite(value) ? (value * 100).toFixed(1) + '%' : '미측정'; }
function curves(history) {
  const canvas = $('curves'), context = canvas.getContext('2d'), width = canvas.width, height = canvas.height;
  context.clearRect(0, 0, width, height); context.font = '700 13px Nanum'; context.fillStyle = '#64778a';
  for (let i = 0; i <= 4; i++) { const y = 20 + i * 45; context.strokeStyle = '#e1e8ee'; context.beginPath(); context.moveTo(48, y); context.lineTo(width - 15, y); context.stroke(); context.fillText((100 - i * 25) + '%', 5, y + 4); }
  if (!Array.isArray(history) || !history.length) { context.fillText('에포크별 실측 데이터가 아직 없습니다.', 300, 110); return; }
  [['precision', '#2770b1'], ['recall', '#21866c'], ['map50', '#dc8a35']].forEach(([key, color]) => {
    context.strokeStyle = color; context.lineWidth = 2; context.beginPath(); let active = false;
    history.forEach((row, i) => { const value = row[key]; if (typeof value !== 'number' || !Number.isFinite(value)) { active = false; return; } const x = 48 + i * (width - 65) / Math.max(1, history.length - 1), y = 200 - Math.max(0, Math.min(1, value)) * 180; if (active) context.lineTo(x, y); else context.moveTo(x, y); active = true; }); context.stroke();
  });
  context.fillStyle = '#64778a'; context.fillText('에포크 ' + history[0].epoch, 48, 222); context.fillText('에포크 ' + history[history.length - 1].epoch, width - 120, 222);
}
function render() {
  const jobs = Array.isArray(state.jobs) ? state.jobs : [], training = state.training || {};
  const metrics = state.metrics || state.selection?.test?.operating || {};
  $('precision').textContent = metric(metrics.precision); $('recall').textContent = metric(metrics.recall);
  $('map50').textContent = metric(metrics.map50 ?? state.selection?.test?.metrics?.['metrics/mAP50(B)']);
  $('metricNote').textContent = '목표 P·R 각각 90% · 평가 구분: ' + (metrics.split || '상태 원문 확인') + ' · 객체 탐지 지표이며 투기 행동 정확도와 구분합니다.';
  const names = {failed: '실패', interrupted: '중단', complete: '완료', running: '실행 중', queued: '대기', starting: '시작 중'};
  const progress = [names[training.state] || training.state, training.job ? '최신 작업 ' + training.job : null,
    training.stage ? '마지막 단계: ' + training.stage : null];
  if (training.epoch != null) progress.push('현재 작업 에포크 ' + training.epoch + (training.epochs ? ' / ' + training.epochs : ''));
  if (training.images != null) progress.push('이미지 ' + training.images + '장');
  if (training.downloaded_bytes != null) progress.push('다운로드 ' + (training.downloaded_bytes / 1024 ** 2).toFixed(1) + 'MB');
  if (training.progress != null) progress.push('진행 ' + training.progress + '%');
  $('trainingState').textContent = progress.filter(value => value !== undefined && value !== null && value !== '').join(' · ') || '작업 대기';
  if (['failed', 'interrupted'].includes(training.state)) {
    message('최신 학습 작업 ' + (names[training.state] || training.state) + ': ' + (training.error || '작업 로그를 확인해 주세요.') + '\n현재 작업은 진행 중이 아닙니다. 오류 원인을 확인하고 검증을 통과한 뒤에만 체크포인트 재개를 진행하세요.');
  }
  const historyContext = training.history_context;
  const legend = document.querySelector('.legend');
  if (legend) legend.textContent = (historyContext ? '보존된 실행 ' + historyContext.run + ' · ' + (historyContext.phase_complete ? '학습 단계 완료 기록 있음' : '학습 단계 완료 미확인') + ' · CSV 마지막 에포크 ' + (historyContext.last_epoch ?? '없음') + ' · 최신 작업의 진행률과 별개입니다. ' : '') + '파랑 정밀도 · 초록 재현율 · 주황 mAP50';
  curves(training.history || state.history || []);
  $('raw').textContent = JSON.stringify(state, null, 2);
  const newResultKey = JSON.stringify(jobs.filter(job => job.kind === 'detect' && job.result).map(job => [job.id, job.result]));
  const updateResults = newResultKey !== resultKey;
  $('jobs').replaceChildren();
  if (updateResults) { $('results').replaceChildren(); resultKey = newResultKey; }
  jobs.forEach(job => {
    const card = document.createElement('article'); card.append(textNode('p', (job.kind || '작업') + ' · ' + (job.state || '') + ' · ' + (job.stage || '') + (job.epoch ? ' · ' + job.epoch + '/' + job.epochs : '')));
    if (job.error) card.append(textNode('p', job.error));
    if (job.log) { const button = textNode('button', '이 작업 로그'); button.className = 'secondary'; button.onclick = () => { $('log').textContent = job.log; $('logInfo').textContent = '상태 응답에 포함된 로그 끝부분 · 전체 파일은 아래 경로에서 확인'; if (/^[A-Za-z0-9_-]+$/.test(job.id || '')) $('logPath').value = 'jobs/' + job.id + '.log'; }; card.append(button); }
    $('jobs').append(card);
    if (updateResults && job.kind === 'detect' && job.result) { const result = document.createElement('article'); result.append(textNode('p', job.id || '탐지 결과')); const video = document.createElement('video'); video.controls = true; video.preload = 'metadata'; video.src = asset(job.result); result.append(video); const link = textNode('a', '결과 파일 열기'); link.href = asset(job.result); link.target = '_blank'; link.rel = 'noopener'; result.append(link); $('results').append(result); }
  });
  if (!$('results').children.length) $('results').textContent = '아직 완료된 탐지 결과가 없습니다.';
  const busy = jobs.some(job => ['running', 'queued', 'starting'].includes(job.state));
  $('train').disabled = pending || busy; $('detect').disabled = pending || !$('videos').value;
}
async function refresh() { if (loading) return; loading = true; try { state = await api('status'); render(); } catch (error) { message(error.message); } finally { loading = false; } }
async function videos() { try { const result = await api('videos'), list = Array.isArray(result) ? result : result.videos || [], previous = $('videos').value; $('videos').replaceChildren(new Option('영상 선택', '')); list.forEach(video => $('videos').add(new Option(video.name || video.path, video.path))); if (list.some(video => video.path === previous)) $('videos').value = previous; render(); } catch (error) { message(error.message); } }
async function probe() { const path = $('videos').value; render(); if (!path) return; try { const data = await api('probe', {path}); $('probe').textContent = JSON.stringify(data, null, 2); if (data.preview) $('previewImage').src = asset(data.preview); if (path.replaceAll('\\', '/').includes('/work/uploads/')) $('preview').src = asset(path); else $('preview').removeAttribute('src'); } catch (error) { message(error.message); } }
async function start(action, params) { if (pending) return; pending = true; render(); try { await api(action, params); message(action === 'train' ? '추가 학습 요청을 전달했습니다.' : '영상 탐지 요청을 전달했습니다.'); } catch (error) { message(error.message); } finally { pending = false; await refresh(); } }
async function loadLog() { try { const data = await api('log?path=' + encodeURIComponent($('logPath').value)); $('log').textContent = data.text; $('logInfo').textContent = '원본 ' + data.original_bytes + '바이트 · 표시 ' + data.captured_bytes + '바이트' + (data.truncated ? ' · 앞부분 생략' : ' · 전체'); } catch (error) { message(error.message); } }
$('reload').onclick = videos; $('videos').onchange = probe; $('logButton').onclick = loadLog;
$('detect').onclick = () => start('detect', {path: $('videos').value});
$('train').onclick = () => start('train', {resume: $('resume').checked});
$('upload').onchange = async () => { const file = $('upload').files[0]; if (!file) return; if (file.size > 4 * 1024 ** 3) { message('4GB 이하 영상을 선택해 주세요.'); return; } try { message('영상을 가져오는 중입니다.'); const response = await fetch('/api/upload', {method: 'POST', headers: {'X-Token': token, 'X-CSRF-Token': token, 'X-Filename': encodeURIComponent(file.name)}, body: file}); const result = await response.json(); if (!response.ok || !result.ok) throw Error(result.error); await videos(); $('videos').value = result.data.path; await probe(); message('영상 가져오기를 마쳤습니다.'); } catch (error) { message(error.message); } };
refresh(); videos(); setInterval(refresh, 8000);
