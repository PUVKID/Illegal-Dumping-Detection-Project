import * as THREE from './vendor/three.module.js';

// 화면 문구와 값은 DOM에 두고, 입체 모형은 단계 설명 선택만 담당합니다.
export function createScene(canvas, onSelect, reportError, onPauseChange = () => {}) {
  const renderer = new THREE.WebGLRenderer({canvas, antialias: true, alpha: true, powerPreference: 'low-power'});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.02;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#eaf8f2');
  const camera = new THREE.OrthographicCamera(-10.5, 10.5, 5, -5, .1, 100);
  camera.position.set(-6, 9, 18); camera.lookAt(0, 1.1, 0);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xc4d4ce, 1.6));
  const key = new THREE.DirectionalLight(0xffffff, 2.6);
  key.position.set(-5, 12, 7); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, {left:-14, right:14, top:10, bottom:-10, near:1, far:40});
  key.shadow.normalBias = .025; key.shadow.bias = -.0001;
  key.shadow.radius = 4; scene.add(key);
  const fill = new THREE.DirectionalLight(0xe1f2eb, 1.1); fill.position.set(8, 6, -8); scene.add(fill);
  const mat = (color, metalness=.08, roughness=.3) => new THREE.MeshStandardMaterial({color, metalness, roughness});
  const white = mat('#f4faf7'), silver = mat('#b5c2bd', .45, .24), dark = mat('#424c50', .55), green = mat('#13d08b', .2, .22), pale = mat('#aedecb'), gold = mat('#c8ad60', .65), grey = mat('#91aaa1');
  const glow = new THREE.MeshStandardMaterial({color:'#20eca1',emissive:'#08cd7d',emissiveIntensity:.7,roughness:.25});
  function rounded(w,h,d,r=.1) {
    r=Math.min(r,w/3,h/3); const shape = new THREE.Shape();
    shape.moveTo(-w/2+r,-h/2); shape.lineTo(w/2-r,-h/2); shape.quadraticCurveTo(w/2,-h/2,w/2,-h/2+r); shape.lineTo(w/2,h/2-r); shape.quadraticCurveTo(w/2,h/2,w/2-r,h/2); shape.lineTo(-w/2+r,h/2); shape.quadraticCurveTo(-w/2,h/2,-w/2,h/2-r); shape.lineTo(-w/2,-h/2+r); shape.quadraticCurveTo(-w/2,-h/2,-w/2+r,-h/2);
    const geometry = new THREE.ExtrudeGeometry(shape,{depth:d,bevelEnabled:true,bevelSegments:3,steps:1,bevelSize:.035,bevelThickness:.035,curveSegments:6}); geometry.translate(0,0,-d/2); return geometry;
  }
  function mesh(parent, geometry, material, x=0,y=0,z=0) {
    const object = new THREE.Mesh(geometry, material); object.position.set(x,y,z); object.castShadow = true; object.receiveShadow = true; parent.add(object); return object;
  }
  const box = (p,w,h,d,m,x=0,y=0,z=0,r=.1) => mesh(p,rounded(w,h,d,r),m,x,y,z);
  const sphere = (p,r,m,x=0,y=0,z=0) => mesh(p,new THREE.SphereGeometry(r,24,16),m,x,y,z);
  const cylinder = (p,r,h,m,x=0,y=0,z=0) => mesh(p,new THREE.CylinderGeometry(r,r,h,32),m,x,y,z);
  const ring = (p,r,t,m,x=0,y=0,z=0) => mesh(p,new THREE.TorusGeometry(r,t,12,48),m,x,y,z);
  function slab(parent,w,height,depth,material,x,y,z,r=.4){const object=mesh(parent,rounded(w,depth,height,r),material,x,y,z);object.rotation.x=-Math.PI/2;return object;}
  const room=new THREE.Scene();room.background=new THREE.Color('#d5e1dc');
  const panelMaterial=new THREE.MeshBasicMaterial({color:'#ffffff',side:THREE.DoubleSide});
  for(const [x,y,z,scale] of [[-6,8,4,8],[7,4,2,4],[0,7,-8,6]]){const panel=new THREE.Mesh(new THREE.PlaneGeometry(scale,scale),panelMaterial);panel.position.set(x,y,z);panel.lookAt(0,0,0);room.add(panel);}
  const pmrem=new THREE.PMREMGenerator(renderer);const environment=pmrem.fromScene(room,.04);scene.environment=environment.texture;scene.environmentIntensity=.55;pmrem.dispose();
  const stage = new THREE.Group(); scene.add(stage);
  slab(stage,18.7,.45,4.0,white,0,-.2,0,.5);
  slab(stage,18.0,.11,3.7,silver,0,.08,0,.45);
  const models=[], plinths=[], drops=[], fans=[], connectors=[], flow=[];
  for(let i=0;i<5;i++) {
    const group = new THREE.Group(); group.position.x=(i-2)*3.6; group.userData.step=i; stage.add(group); models.push(group);
    slab(group,2.95,.45,2.9,silver,0,.4,0,.43);
    slab(group,2.75,.13,2.7,white,0,.71,0,.38);
    const activeMaterial=mat('#bcd0c7');plinths.push(activeMaterial);
    slab(group,2.83,.10,2.76,activeMaterial,0,.17,0,.4);
    if(i<4){const connector=cylinder(stage,.18,.8,silver,(i-1.5)*3.6,.48,0);connector.rotation.z=Math.PI/2;connector.material=connector.material.clone();connector.material.transparent=true;connector.material.opacity=.32;connector.material.depthWrite=false;const light=cylinder(stage,.14,.85,pale,(i-1.5)*3.6,.49,0);light.rotation.z=Math.PI/2;light.material=light.material.clone();connectors.push(light);}
  }
  // 구름 아래 수신 트레이·회로와 낙하 큐브를 배치합니다.
  for(let i=0;i<6;i++){const cube=box(stage,.10,.10,.10,glow,-5.4+i*.13,.52,0,.02);flow.push(cube);}
  const cloud=models[0];slab(cloud,2.55,.25,2.20,white,0,.94,0,.32);slab(cloud,2.39,.07,2.04,glow,0,1.10,0,.29);slab(cloud,2.25,.10,1.9,dark,0,1.16,0,.28);slab(cloud,1.7,.05,1.35,glow,0,1.24,0,.25);
  for(let i=0;i<8;i++){const a=i/8*Math.PI*2; sphere(cloud,.055,silver,Math.cos(a)*.94,1.24,Math.sin(a)*.70);}
  const cloudBody = new THREE.Group(); cloudBody.position.y=3.4;cloud.add(cloudBody);
  sphere(cloudBody,.64,white,-.7,0,0);sphere(cloudBody,.86,white,0,.22,0);sphere(cloudBody,.65,white,.76,-.02,0);box(cloudBody,1.6,.8,.9,white,0,-.2,0,.28);
  box(cloudBody,.30,.80,.22,green,0,-.25,.85,.06); const arrow=mesh(cloudBody,new THREE.ConeGeometry(.42,.5,4),green,0,-.8,.85);arrow.rotation.z=Math.PI; arrow.rotation.y=Math.PI/4;
  for(let i=0;i<12;i++){const cube=box(cloud,.15+(i%2)*.04,.18,.18,glow,(i%3-1)*.43,1.1+(i/3)*.42,(i%2-.5)*.38,.03);cube.userData.offset=i*.35;drops.push(cube);}
  // 이미지 스택은 프레임·민트색 인화지·산 모양·태양을 각각 입체 부품으로 만듭니다.
  function photo(parent,x,y,z,rotation=0){const g=new THREE.Group();g.position.set(x,y,z);g.rotation.z=rotation;parent.add(g);g.userData.sheet=true;g.userData.restY=y;box(g,1.88,1.8,.15,white,0,0,0,.13);box(g,1.58,1.18,.06,pale,0,.03,.12,.07);sphere(g,.13,white,.45,.35,.18);const mountain=new THREE.Shape();mountain.moveTo(-.69,-.4);mountain.lineTo(-.15,.28);mountain.lineTo(.12,-.08);mountain.lineTo(.36,.15);mountain.lineTo(.69,-.4);mountain.closePath();mesh(g,new THREE.ExtrudeGeometry(mountain,{depth:.04,bevelEnabled:false}),grey,0,0,.2);box(g,.85,.06,.06,silver,-.25,-.72,.14,.02);return g;}
  for(let i=3;i>=0;i--) photo(models[1],(i-1.5)*-.12,1.8+i*.10,-i*.22, -.04+i*.025);
  // 그래픽 보드의 방열판·회로·팬·접점과 나사를 분리합니다.
  const gpu=models[2];box(gpu,2.45,1.7,.48,dark,0,1.85,0,.17);box(gpu,2.50,.12,.55,silver,0,2.7,0,.03);box(gpu,2.50,.12,.55,silver,0,1.0,0,.03);box(gpu,.85,.75,.10,dark,-.65,1.95,.30,.10);
  for(let i=0;i<13;i++)box(gpu,.06,.08,.56,grey,-1.1+i*.18,2.79,0,.01);
  box(gpu,.28,.20,.06,glow,0,1.20,.30,.03);
  for(let i=0;i<9;i++)box(gpu,.12,.25,.12,gold,-.7+i*.17,.91,0,.01);
  for(const x of [.58]){ring(gpu,.48,.055,silver,x,1.9,.32);mesh(gpu,new THREE.CircleGeometry(.43,40),dark,x,1.9,.35);const fan=new THREE.Group();fan.position.set(x,1.9,.40);gpu.add(fan);fans.push(fan);for(let i=0;i<7;i++){const blade=box(fan,.16,.31,.05,grey,Math.sin(i*Math.PI*2/7)*.23,Math.cos(i*Math.PI*2/7)*.23,0,.05);blade.rotation.z=-i*Math.PI*2/7+.5;}sphere(fan,.13,silver,0,0,.05);}
  for(const x of [-1.08,1.08])for(const y of [1.2,2.5]){sphere(gpu,.05,silver,x,y,.3);}
  // 돋보기와 검증 이미지, 투명 렌즈입니다.
  const verify=models[3];photo(verify,-.3,1.73,-.16,.09);
  const magnify = new THREE.Group();magnify.position.set(.15,2.02,.47);magnify.rotation.z=-.2;verify.add(magnify);
  ring(magnify,.84,.11,silver);ring(magnify,.71,.025,white,0,0,.02);
  const glass=new THREE.MeshPhysicalMaterial({color:'#bfe8d9',transparent:true,opacity:.32,roughness:.07,metalness:.1,side:THREE.DoubleSide});mesh(magnify,new THREE.CircleGeometry(.70,48),glass,0,0,.035);
  const handle=box(magnify,.25,.95,.25,dark,.65,-.92,0,.1);handle.rotation.z=.55;
  // 보고서의 막대와 체크 도장은 장식이며 실측 수치를 표현하지 않습니다.
  const report=models[4];box(report,1.85,2.55,.22,silver,-.13,2.13,-.08,.15);box(report,1.72,2.43,.12,white,-.15,2.18,.10,.1);
  for(let i=0;i<3;i++)box(report,1.13-i*.18,.09,.06,grey,-.18-i*.08,2.95-i*.3,.21,.03);
  for(let i=0;i<3;i++)box(report,.18,.3+i*.18,.08,silver,-.68+i*.35,1.25+(.3+i*.18)/2,.22,.03);
  const stamp = new THREE.Group();stamp.position.set(.62,1.55,.5);report.add(stamp);const disc=cylinder(stamp,.59,.18,silver);disc.rotation.x=Math.PI/2;
  const checkA=box(stamp,.13,.37,.06,white,-.16,-.01,.12,.03);checkA.rotation.z=.65;const checkB=box(stamp,.13,.65,.06,white,.10,.07,.12,.03);checkB.rotation.z=-.65;
  models.forEach(model=>model.scale.setScalar(1.08));
  const accents=models.map(group=>{const values=[];group.traverse(object=>{if(object.isMesh&&[green,glow,pale].includes(object.material)){object.material=object.material.clone();values.push(object.material);}});return values;});
  const accentLight=new THREE.PointLight('#00c84f',.75,5,2);accentLight.position.set(-7.2,1.3,0);stage.add(accentLight);
  const floor=mesh(scene,new THREE.PlaneGeometry(80,45),new THREE.ShadowMaterial({color:'#2c7152',opacity:.13}),0,-.46,0);floor.rotation.x=-Math.PI/2;floor.castShadow=false;
  const ray = new THREE.Raycaster(), pointer=new THREE.Vector2();
  const motion=globalThis.CleanviewFormat.motionPreference(matchMedia('(prefers-reduced-motion: reduce)').matches,onPauseChange);
  let active=null, badge=null, paused=motion.paused, lost=false, selected=null, visible=true, frame=0, last=0;
  function size(){const w=canvas.clientWidth,h=canvas.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);const aspect=w/h;camera.left=-9.6;camera.right=9.6;camera.top=9.6/aspect;camera.bottom=-9.6/aspect;camera.updateProjectionMatrix();draw();}
  function draw(){if(!lost&&!document.hidden&&visible){renderer.render(scene,camera);const label=document.getElementById('gpuLabel');if(label){const point=new THREE.Vector3(-.702,2.106,.432).project(camera);label.style.left=(point.x*.5+.5)*canvas.clientWidth+'px';label.style.top=(-point.y*.5+.5)*canvas.clientHeight+'px';label.hidden=false;}}}
  function tick(now){frame=0;if(paused||lost||document.hidden||!visible)return;if(now-last>=1000/30){last=now;drops.forEach(cube=>{cube.visible=active===0&&badge==='진행 중';cube.position.y=globalThis.CleanviewFormat.dropHeight(now,cube.userData.offset);});flow.forEach((cube,i)=>{cube.visible=active===0&&badge==='진행 중';cube.position.x=-5.7+((now*.00045+i*.13)%.68);});models[1].children.filter(object=>object.userData.sheet).forEach((sheet,i)=>{sheet.position.y=sheet.userData.restY+(active===1?Math.sin(now*.002+i)*.045:0);});if(active===2)fans.forEach(f=>f.rotation.z-=.13);magnify.position.x=.15+(active===3?Math.sin(now*.0015)*.16:0);stamp.scale.setScalar(active===4?1+Math.sin(now*.002)*.035:1);if(active===2)accents[2].forEach(m=>m.emissiveIntensity=.35+Math.sin(now*.003)*.2);cloudBody.position.y=3.4+(active===0?Math.sin(now*.001)*.055:0);draw();}frame=requestAnimationFrame(tick);}
  function start(){if(!frame&&!paused&&!lost&&!document.hidden&&visible)frame=requestAnimationFrame(tick);else draw();}
  document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;}else start();});
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');reduced.addEventListener('change',e=>{paused=motion.changed(e.matches);if(paused){cancelAnimationFrame(frame);frame=0;draw();}else start();});
  canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();lost=true;cancelAnimationFrame(frame);frame=0;reportError('3D 그래픽 연결이 끊겼습니다. 아래 단계와 모든 실제 상태는 계속 확인할 수 있습니다.');});
  canvas.addEventListener('webglcontextrestored',()=>{lost=false;reportError('');size();start();});
  canvas.addEventListener('click',event=>{if(lost)return;const rect=canvas.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(models,true)[0];if(hit){let object=hit.object;while(object&&object.userData.step===undefined)object=object.parent;if(object){selected=object.userData.step;onSelect(selected);draw();}}});
  const observer=new ResizeObserver(size);observer.observe(canvas);size();start();
  return {update(p){active=['진행 중','재시도'].includes(p.badge)?p.step:null;badge=p.badge;const style=i=>globalThis.CleanviewFormat.stageStyle(p,i);const color=i=>style(i).color;plinths.forEach((material,i)=>{material.color.set(color(i));material.toneMapped=false;material.emissive.set(i===p.step?color(i):'#000000');material.emissiveIntensity=i===p.step?.14:0;accents[i].forEach(m=>{m.color.set(color(i));m.toneMapped=false;m.emissive.set(i===p.step?color(i):'#000000');m.emissiveIntensity=i===p.step?.18:0;});});connectors.forEach((object,i)=>{object.material.color.set(color(i));object.material.toneMapped=false;object.material.emissive.set(i===p.step?color(i):'#000000');object.material.emissiveIntensity=i===p.step?.25:0;});accentLight.color.set(color(p.step ?? 0));accentLight.intensity=p.step===0?.75:0;drops.forEach(cube=>cube.visible=active===0&&badge==='진행 중');flow.forEach(cube=>cube.visible=active===0&&badge==='진행 중');draw();},pause(value){paused=motion.setPaused(value);cancelAnimationFrame(frame);frame=0;start();return paused;},setVisible(value){visible=value;cancelAnimationFrame(frame);frame=0;if(value){size();start();}},get paused(){return paused;}};
}
