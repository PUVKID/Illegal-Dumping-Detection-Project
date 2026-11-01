'use strict';
const token = new URLSearchParams(location.search).get('token') || '';
const $ = id => document.getElementById(id);
let state = {}, loading = false, pending = false, resultKey = null, format = null, sample = null, scene = null, notices = null;
const formatReady = import('/presentation.js?token=' + encodeURIComponent(token)).then(() => { format = globalThis.CleanviewFormat; sample = format.sampler(); notices = format.noticeState(); });
const asset = path => '/asset?token=' + encodeURIComponent(token) + '&path=' + encodeURIComponent(path);
function message(value) { $('message').textContent = notices ? notices.set(value) : value; }
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
function curves(history, id = 'curves') {
  const canvas = $(id), context = canvas.getContext('2d'), width = canvas.width, height = canvas.height;
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
  if (!format) return;
  renderOverview();
  const jobs = Array.isArray(state.jobs) ? state.jobs : [], training = state.training || {};
  const metrics = state.metrics || state.selection?.test?.operating || {};
  $('precision').textContent = metric(metrics.precision); $('recall').textContent = metric(metrics.recall);
  $('map50').textContent = metric(metrics.map50 ?? state.selection?.test?.metrics?.['metrics/mAP50(B)']);
  $('metricNote').textContent = '목표 P·R 각각 90% · 평가 구분: ' + (metrics.split || '상태 원문 확인') + ' · 객체 탐지 지표이며 투기 행동 정확도와 구분합니다.';
  const names = {failed: '실패', interrupted: '중단', complete: '완료', running: '실행 중', queued: '대기', starting: '시작 중'};
  const progress = [names[training.state] || training.state, training.job ? '최신 작업 ' + training.job : null,
    training.stage ? '마지막 단계: ' + training.stage : null];
  if (state.presentation?.epoch != null) progress.push('현재 작업 에포크 ' + format.epochText(state.presentation, training.epochs));
  if (training.images != null) progress.push('이미지 ' + training.images + '장');
  if (training.downloaded_bytes != null) progress.push('다운로드 ' + (training.downloaded_bytes / 1024 ** 2).toFixed(1) + 'MB');
  if (training.progress != null) progress.push('진행 ' + training.progress + '%');
  $('trainingState').textContent = progress.filter(value => value !== undefined && value !== null && value !== '').join(' · ') || '작업 대기';
  $('message').textContent = notices.apply(training, state.presentation?.description || '작업이 중단됐습니다. 기존 자료는 유지됩니다. 작업 기록에서 오류를 확인하세요.');
  const historyContext = training.history_context;
  $('observation').textContent = '마지막 관측 ' + (training.observed_kst || '자료 없음') + '\n갱신 지연 ' + (training.delay_seconds == null ? '확인 불가' : training.delay_seconds + '초') + (training.stale ? ' · 오래된 관측 자료' : '') + ' · 현재 조회 ' + (state.now_kst || '확인 불가');
  const legend = document.querySelector('.legend');
  if (legend) legend.textContent = (historyContext ? '보존된 실행 ' + historyContext.run + ' · ' + (historyContext.phase_complete ? '학습 단계 완료 기록 있음' : '학습 단계 완료 미확인') + ' · CSV 마지막 에포크 ' + (historyContext.last_epoch ?? '없음') + ' · 최신 작업의 진행률과 별개입니다. ' : '') + '파랑 정밀도 · 초록 재현율 · 주황 mAP50';
  const runs = training.runs || [];
  curves(runs[0]?.history || []); curves(runs[1]?.history || [], 'curves2');
  if (legend) legend.textContent = '7차 각 후보의 실측 CSV만 표시합니다. 파랑 정밀도 · 초록 재현율 · 주황 mAP50 · 최종 테스트 성능과 구분합니다.';
  $('raw').textContent = JSON.stringify(state, null, 2);
  const newResultKey = JSON.stringify(jobs.filter(job => job.kind === 'detect' && job.result).map(job => [job.id, job.result]));
  const updateResults = newResultKey !== resultKey;
  $('jobs').replaceChildren();
  if (updateResults) { $('results').replaceChildren(); resultKey = newResultKey; }
  jobs.forEach(job => {
    const card = document.createElement('article'); card.append(textNode('p', ({train:'학습',detect:'탐지'}[job.kind] || '작업') + ' · ' + (names[job.state] || job.state || '') + ' · ' + (job.stage || '') + (job.epoch ? ' · ' + job.epoch + '/' + job.epochs : '')));
    if (job.error) card.append(textNode('p', job.error));
    if (job.log || job.log_path) { const button = textNode('button', '이 작업 로그'); button.className = 'secondary'; button.onclick = () => { $('log').textContent = job.log || '아래 로그 읽기를 눌러 이 작업의 끝부분을 조회하세요.'; $('logInfo').textContent = '상태 응답에 포함된 로그 끝부분 · 전체 파일은 아래 경로에서 확인'; if (/^[A-Za-z0-9_-]+$/.test(job.id || '')) $('logPath').value = job.log_path || 'jobs/' + job.id + '.log'; }; card.append(button); }
    $('jobs').append(card);
    if (updateResults && job.kind === 'detect' && job.result) { const result = document.createElement('article'); result.append(textNode('p', job.id || '탐지 결과')); const video = document.createElement('video'); video.controls = true; video.preload = 'metadata'; video.src = asset(job.result); result.append(video); const link = textNode('a', '결과 파일 열기'); link.href = asset(job.result); link.target = '_blank'; link.rel = 'noopener'; result.append(link); $('results').append(result); }
  });
  if (!$('results').children.length) $('results').textContent = '아직 완료된 탐지 결과가 없습니다.';
  const busy = state.busy || jobs.some(job => ['running', 'queued', 'starting'].includes(job.state));
  $('train').disabled = pending || busy; $('detect').disabled = pending || !$('videos').value;
}
async function refresh() { await formatReady; if (loading) return; loading = true; try { state = await api('status'); render(); } catch (error) { message(error.message); } finally { loading = false; } }
async function videos() { try { const result = await api('videos'), list = Array.isArray(result) ? result : result.videos || [], previous = $('videos').value; $('videos').replaceChildren(new Option('영상 선택', '')); list.forEach(video => $('videos').add(new Option(video.name || video.path, video.path))); if (list.some(video => video.path === previous)) $('videos').value = previous; render(); } catch (error) { message(error.message); } }
async function probe() { const path = $('videos').value; render(); if (!path) return; try { const data = await api('probe', {path}); $('probe').textContent = JSON.stringify(data, null, 2); if (data.preview) $('previewImage').src = asset(data.preview); if (path.replaceAll('\\', '/').includes('/work/uploads/')) $('preview').src = asset(path); else $('preview').removeAttribute('src'); } catch (error) { message(error.message); } }
async function start(action, params) { if (pending) return; pending = true; render(); try { await api(action, params); message(action === 'train' ? '추가 학습 요청을 전달했습니다.' : '영상 탐지 요청을 전달했습니다.'); } catch (error) { message(error.message); } finally { pending = false; await refresh(); } }
async function loadLog() { try { const data = await api('log?path=' + encodeURIComponent($('logPath').value)); $('log').textContent = data.text; $('logInfo').textContent = '원본 ' + data.original_bytes + '바이트 · 표시 ' + data.captured_bytes + '바이트' + (data.truncated ? ' · 앞부분 생략' : ' · 전체'); } catch (error) { message(error.message); } }
$('reload').onclick = videos; $('videos').onchange = probe; $('logButton').onclick = loadLog;
$('detect').onclick = () => start('detect', {path: $('videos').value});
$('train').onclick = () => start('train', {resume: $('resume').checked});
$('upload').onchange = async () => { const file = $('upload').files[0]; if (!file) return; if (file.size > 4 * 1024 ** 3) { message('4GB 이하 영상을 선택해 주세요.'); return; } try { message('영상을 가져오는 중입니다.'); const response = await fetch('/api/upload', {method: 'POST', headers: {'X-Token': token, 'X-CSRF-Token': token, 'X-Filename': encodeURIComponent(file.name)}, body: file}); const result = await response.json(); if (!response.ok || !result.ok) throw Error(result.error); await videos(); $('videos').value = result.data.path; await probe(); message('영상 가져오기를 마쳤습니다.'); } catch (error) { message(error.message); } };
formatReady.then(() => { refresh(); videos(); initializeScene(); }).catch(error => message('표시 모듈을 불러오지 못했습니다: ' + error.message)); setInterval(refresh, 8000);

const detailText = ['공식 원자료를 수신합니다. 표시되는 비율은 현재 파일 기준이며 전체 실험 진행률이 아닙니다.', '원본 무결성 검사·압축 해제·정규화·고정 데이터 분할을 준비합니다.', '준비된 자료로 두 후보 모델을 학습합니다. 실측 에포크만 성능 분석에 표시합니다.', '고정 검증 자료로 후보 모델·추론 방식·임계값을 비교합니다.', '선택을 고정한 뒤 테스트 성능을 측정합니다. 저장된 최종 평가만 성능 카드에 표시합니다.'];
function selectStep(index) {
  document.querySelectorAll('[data-step]').forEach(button => button.classList.toggle('selected', Number(button.dataset.step) === index));
  $('stepDetail').textContent = ['다운로드', '데이터 준비', 'GPU 학습', '검증', '최종 평가'][index] + ' · ' + detailText[index] + ' (설명 선택이며 실제 작업을 변경하지 않습니다.)';
}
function showTab(id) {
  document.querySelectorAll('.tab-panel').forEach(panel => panel.hidden = panel.id !== id);
  document.querySelectorAll('[data-tab]').forEach(button => { const active = button.dataset.tab === id; button.classList.toggle('active', active); button.setAttribute('aria-current', active ? 'page' : 'false'); if (active) $('pageTitle').textContent = button.textContent.replace(/^\s*0[1-4]\s*/, '').trim(); });
  if (scene) scene.setVisible(id === 'overview');
  document.title = '클린뷰 · ' + $('pageTitle').textContent;
}
function renderOverview() {
  const training = state.training || {}, p = state.presentation || {};
  $('currentTitle').textContent = p.title || '실험 상태를 확인하고 있습니다';
  $('currentDescription').textContent = p.description || '마지막 저장 기록을 안전하게 읽어옵니다.';
  $('stateBadge').textContent = p.badge || '상태 확인 중';
  $('stateBadge').hidden = !['재시도','실패','중단'].includes(p.badge);
  $('stateBadge').classList.toggle('problem', ['재시도', '실패', '중단'].includes(p.badge));
  $('currentFile').textContent = [training.source, training.file].filter(Boolean).join(' · ') || '기록된 파일이 없습니다';
  $('filePercent').textContent = format.percent(p.file_percent);
  $('fileSize').textContent = format.gib(p.downloaded_bytes) + ' / ' + format.gib(p.file_bytes);
  $('fileProgress').value = p.file_percent || 0;
  $('gpuState').textContent = p.gpu_state || '대기 중';
  $('epoch').textContent = format.epochText(p, training.epochs);
  $('nextStage').textContent = p.next || '상태 확인 중';
  $('nextDescription').textContent = p.next_description || '실제 작업 기록에서 다음 단계를 확인합니다.';
  const measured = sample(training);
  $('speed').textContent = measured.speed == null ? '미측정' : (measured.speed / 1024 ** 2).toFixed(2) + ' MiB/s';
  $('eta').textContent = format.duration(measured.eta);
  $('retry').hidden = !p.retry;
  $('retry').textContent = p.retry ? '재시도 ' + (training.retry_attempt || 0) + ' / ' + (training.retry_limit || '미확인') + ' · ' + (training.retry_reason || '') : '';
  $('lastUpdated').textContent = training.observed_kst ? '마지막 관측 ' + training.observed_kst : '기록된 관측 시각이 없습니다';
  $('observation').classList.toggle('stale', !!training.stale);
  $('now').textContent = state.now_kst || '';
  $('gpuNote').textContent = p.gpu_state === '대기 중' ? '현재 GPU 학습 전입니다. 준비·다운로드는 학습 에포크에 포함하지 않습니다.' : '실제 저장된 각 후보 곡선과 현재 작업 에포크를 구분합니다.';
  document.querySelectorAll('[data-step]').forEach((button, i) => { const status = p.steps?.[i]?.status || 'pending'; Object.entries(format.stageClasses(p, i)).forEach(([name, enabled]) => button.classList.toggle(name, enabled)); button.querySelector('small').textContent = status === 'active' ? p.badge || '진행 중' : status === 'complete' ? '완료' : '대기'; });
  $('recentJobs').replaceChildren();
  (state.jobs || []).slice(0,4).forEach(job => { const tr = document.createElement('tr'); const date = typeof job.updated === 'number' ? new Intl.DateTimeFormat('sv-SE', {timeZone:'Asia/Seoul', dateStyle:'short', timeStyle:'medium'}).format(new Date(job.updated * 1000)) : '시각 미확인'; tr.append(textNode('td', date), textNode('td', job.stage || ({train:'학습 작업',detect:'영상 탐지'}[job.kind] || '작업')), textNode('td', {running:'진행 중',queued:'대기',starting:'시작 중',failed:'실패',interrupted:'중단',complete:'완료'}[job.state] || '미확인')); $('recentJobs').append(tr); });
  if (!$('recentJobs').children.length) { const tr = document.createElement('tr'); const td = textNode('td','기록된 작업이 없습니다.'); td.colSpan = 3; tr.append(td); $('recentJobs').append(tr); }
  if (scene) scene.update(p);
}
function synchronizeMotion(paused) { $('motion').setAttribute('aria-pressed', String(paused)); $('motion').textContent = paused ? '3D 움직임 재생' : '3D 움직임 정지'; }
async function initializeScene() {
  try { const module = await import('/scene.js?token=' + encodeURIComponent(token)); scene = module.createScene($('scene'), selectStep, value => $('sceneError').textContent = value, synchronizeMotion); scene.update(state.presentation || {}); }
  catch (error) { $('gpuLabel').hidden = true; $('sceneError').textContent = '3D 화면을 사용할 수 없습니다. 아래 다섯 단계와 실제 상태는 계속 표시합니다. ' + error.message; $('motion').disabled = true; }
}
document.querySelectorAll('[data-tab]').forEach(button => button.onclick = () => showTab(button.dataset.tab));
document.querySelectorAll('[data-step]').forEach(button => button.onclick = () => selectStep(Number(button.dataset.step)));
$('openRecords').onclick = () => showTab('records'); $('refreshButton').onclick = refresh;
$('motion').onclick = () => { if (scene) scene.pause(!scene.paused); };
