'use strict';
// 실제 저장 시각이 다른 두 표본만 속도 계산에 사용합니다.
(function (target) {
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  const gib = value => finite(value) && value >= 0 ? (value / 1024 ** 3).toFixed(2) + ' GiB' : '미측정';
  const percent = value => finite(value) ? value.toFixed(1) + '%' : '—';
  const metric = value => finite(value) ? (value * 100).toFixed(1) + '%' : '미측정';
  function duration(seconds) {
    if (!finite(seconds) || seconds < 0) return '추정 불가';
    const minutes = Math.ceil(seconds / 60);
    return minutes < 1 ? '1분 이내' : minutes < 60 ? minutes + '분' : Math.floor(minutes / 60) + '시간 ' + minutes % 60 + '분';
  }
  function sampler() {
    let previous = null, measured = {speed: null, eta: null};
    return training => {
      const key = JSON.stringify([training.job, training.source, training.file, training.file_bytes]);
      const bytes = training.downloaded_bytes, at = training.updated, total = training.file_bytes;
      if (!training.job || training.stale || training.state !== 'running' || !finite(bytes) || !finite(at) || !finite(total) || total <= 0) {
        previous = null; measured = {speed: null, eta: null}; return measured;
      }
      if (!previous || previous.key !== key || bytes < previous.bytes || at < previous.at) {
        previous = {key, bytes, at}; measured = {speed: null, eta: null}; return measured;
      }
      if (at > previous.at) {
        const speed = (bytes - previous.bytes) / (at - previous.at);
        measured = {speed: speed > 0 ? speed : null, eta: speed > 0 ? Math.max(0, total - bytes) / speed : null};
        previous = {key, bytes, at};
      }
      return measured;
    };
  }
  function motionPreference(initialReduced, notify) {
    let paused = Boolean(initialReduced);
    notify(paused);
    return {
      get paused() { return paused; },
      setPaused(value) { paused=Boolean(value); notify(paused); return paused; },
      changed(reduced) { if (reduced) paused=true; notify(paused); return paused; }
    };
  }
  const dropHeight = (milliseconds, offset) => 2.75 - ((milliseconds * .0006 + offset) % 1.7);
  const epochText = (presentation, epochs) => presentation?.epoch == null ? '—' : presentation.epoch + (epochs ? ' / ' + epochs : '');
  function noticeState() {
    let current = {text:'', kind:'general'}, failureKey = null;
    return {
      set(text, kind='general') { current={text,kind}; return text; },
      apply(training, failureText) {
        if (['failed','interrupted'].includes(training.state)) {
          const key = JSON.stringify([training.job, training.state]);
          if (failureKey !== key) { current={text:failureText,kind:'state'}; failureKey=key; }
        } else {
          failureKey=null;
          if (current.kind === 'state') current={text:'',kind:'general'};
        }
        return current.text;
      }
    };
  }
  function stageStyle(p, index) {
    if (p.steps?.[index]?.status === 'complete') return {kind:'complete',color:'#a9e3cd'};
    if (index !== p.step) return {kind:'pending',color:'#c6cecb'};
    if (['실패','중단'].includes(p.badge)) return {kind:'error',color:'#dc9688'};
    if (['자원 대기','자료 없음','기록 없음','대기'].includes(p.badge)) return {kind:'pending',color:'#c6cecb'};
    if (p.retry) return {kind:'retry',color:'#e2b457'};
    return {kind:'active',color:'#00c84f'};
  }
  function stageClasses(p, index) {
    const kind = stageStyle(p, index).kind;
    return {active:['active','error','retry'].includes(kind), complete:kind==='complete',
      failed:kind==='error', retrying:kind==='retry', waiting:kind==='pending' && index===p.step};
  }
  const api = {gib, percent, metric, duration, sampler, noticeState, stageStyle, stageClasses, epochText, dropHeight, motionPreference};
  target.CleanviewFormat = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(globalThis);
