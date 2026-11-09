// 3D opportunity board · niche-bend harness · reads /state.json (SPEC.md section 4)
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {CSS2DRenderer, CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js';

const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = n => n == null || n === '' || isNaN(n) ? '?' : n >= 1e6 ? (n/1e6).toFixed(1).replace('.0','') + 'M' : n >= 1e3 ? Math.round(n/1e3) + 'K' : '' + n;
const num = v => typeof v === 'number' && isFinite(v);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const W = v => v - 50;                 // axis value 0-100 -> world -50..50
const R = 55;                          // frontier radius around the best corner (demand 100, saturation 0, fit 100)
const COL = {g:'#79B791', y:'#E8A838', r:'#F26157'};
const GREEN = ['open','confirmed','proven','supported','go'];
const RED = ['pass','weak','crowded','against','dropped','reject','mismatch'];
const tone = v => { v = String(v || '').toLowerCase(); return GREEN.includes(v) ? 'g' : RED.some(x => v.includes(x)) ? 'r' : 'y'; };
const ytThumb = id => 'https://i.ytimg.com/vi/' + encodeURIComponent(id) + '/mqdefault.jpg';
const ytUrl = id => 'https://www.youtube.com/watch?v=' + encodeURIComponent(id);

// ---------- state ----------
let data = null, lastText = '', source = '', points = [], pinned = null, hovered = null, keepMap = new Map();
const filters = {round:'all', verdict:'all', niche:'all'};

// ---------- scene ----------
const stage = $('#stage'), canvas = $('#gl');
const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x0A0805, 300, 640);
const camera = new THREE.PerspectiveCamera(36, 1, 1, 2000);
camera.position.set(196, 118, 222);
const labels = new CSS2DRenderer();
labels.domElement.className = 'labels';
stage.appendChild(labels.domElement);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true; controls.dampingFactor = .08;
controls.minDistance = 80; controls.maxDistance = 520; controls.target.set(0, -8, 0);
controls.autoRotateSpeed = .6;

scene.add(new THREE.AmbientLight(0xffffff, .55));
const key = new THREE.DirectionalLight(0xFFF4EA, 1.3); key.position.set(90, 160, 120); scene.add(key);
const rim = new THREE.PointLight(0xF26157, 400, 300, 1.6); rim.position.set(-80, 40, -80); scene.add(rim);

function segs(list, color, opacity) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(list, 3));
  return new THREE.LineSegments(g, new THREE.LineBasicMaterial({color, transparent:true, opacity, depthWrite:false}));
}
function label(html, cls, x, y, z, center) {
  const el = document.createElement('div'); el.className = cls; el.innerHTML = html;
  const o = new CSS2DObject(el); o.position.set(x, y, z); if (center) o.center.set(...center);
  return o;
}

// space: walls with grid, frame, ticks, axis titles
(function buildSpace() {
  const minor = [], major = [];
  for (let t = 0; t <= 100; t += 10) {
    const a = (t % 50 === 0) ? major : minor, v = W(t);
    a.push(v,-50,-50, v,-50,50,  -50,-50,v, 50,-50,v);   // floor: demand x fit
    a.push(v,-50,-50, v,50,-50,  -50,v,-50, 50,v,-50);   // back wall: demand x saturation
    a.push(-50,v,-50, -50,v,50,  -50,-50,v, -50,50,v);   // side wall: saturation x fit
  }
  scene.add(segs(minor, 0xFFF4EA, .055), segs(major, 0xFFF4EA, .14));
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), new THREE.MeshBasicMaterial({color:0x14110D, transparent:true, opacity:.55, depthWrite:false}));
  floor.rotation.x = -Math.PI/2; floor.position.y = -50.05; scene.add(floor);
  const box = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(100,100,100)), new THREE.LineBasicMaterial({color:0xFFF4EA, transparent:true, opacity:.2}));
  scene.add(box);
  for (const t of [0,25,50,75,100]) {
    scene.add(label(t, 'tk', W(t), -55, 57));
    scene.add(label(t, 'tk', -57, W(t), 54));
    scene.add(label(t, 'tk', 57, -55, W(t)));
  }
  scene.add(label('Demand &rarr;<small>target-topic views · same query, same day</small>', 'ax', 0, -64, 66));
  scene.add(label('Saturation &uarr;<small>successful copies on the crossing</small>', 'ax', -70, 6, 56));
  scene.add(label('Fit &rarr;<small>faceless 2D × audience</small>', 'ax', 68, -64, 0));
  scene.add(label('Best corner', 'corner', 50, -50, 50, [-.08, -.6]));
})();

// frontier shell: a quarter dome of radius R centred on the best corner
(function buildFrontier() {
  const seg = 48, pos = [], idx = [];
  const P = (th, ph) => [50 - R*Math.sin(th)*Math.cos(ph), -50 + R*Math.cos(th), 50 - R*Math.sin(th)*Math.sin(ph)];
  for (let i = 0; i <= seg; i++) for (let j = 0; j <= seg; j++) pos.push(...P(i/seg*Math.PI/2, j/seg*Math.PI/2));
  for (let i = 0; i < seg; i++) for (let j = 0; j < seg; j++) { const a = i*(seg+1)+j, b = a+seg+1; idx.push(a,b,a+1, b,b+1,a+1); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
  scene.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({color:0x79B791, transparent:true, opacity:.085, side:THREE.DoubleSide, depthWrite:false})));
  const arc = (fn, op) => { const p = []; for (let k = 0; k < 64; k++) p.push(...fn(k/63*Math.PI/2), ...fn((k+1)/63*Math.PI/2)); p.length -= 6; return segs(p, 0x79B791, op); };
  for (const th of [Math.PI/8, Math.PI/4, 3*Math.PI/8]) scene.add(arc(ph => P(th, ph), .26));
  for (const ph of [Math.PI/8, Math.PI/4, 3*Math.PI/8]) scene.add(arc(t => P(t, ph), .26));
  scene.add(arc(ph => P(Math.PI/2, ph), .75), arc(t => P(t, 0), .6), arc(t => P(t, Math.PI/2), .6));
})();

// halo texture
const haloTex = (() => {
  const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d');
  const g = x.createRadialGradient(64,64,0,64,64,64); g.addColorStop(0,'rgba(255,255,255,.9)'); g.addColorStop(.25,'rgba(255,255,255,.35)'); g.addColorStop(1,'rgba(255,255,255,0)');
  x.fillStyle = g; x.fillRect(0,0,128,128); return new THREE.CanvasTexture(c);
})();
const sphere = new THREE.SphereGeometry(1, 36, 24);
const ringGeo = new THREE.RingGeometry(.62, .82, 48);
const pointsRoot = new THREE.Group(); scene.add(pointsRoot);
let meshes = [];
const pin = new THREE.Mesh(new THREE.RingGeometry(1.55, 1.68, 64), new THREE.MeshBasicMaterial({color:0xFFF4EA, transparent:true, opacity:.95, side:THREE.DoubleSide, depthTest:false}));
pin.visible = false; pin.renderOrder = 10; scene.add(pin);

// ---------- data ----------
function keptIds(d) {
  const s = new Set(), k = d.keeps || d.kept || [];
  (Array.isArray(k) ? k : (k.ids || [])).forEach(x => typeof x === 'string' ? s.add(x) : x && (x.id ? s.add(x.id) : (x.ids || []).forEach(i => s.add(i))));
  return s;
}
function norm(p, i, d, kept) {
  const src = p.source || {};
  const q = Object.assign({}, p);
  q.id = String(p.id ?? ('point-' + (i+1)));
  q.round = String(p.round || d.round || (d.run && d.run.date) || d.runId || '—');
  q.niche = p.niche || '—';
  q.verdict = String(p.verdict || 'untested').toLowerCase();
  q.conf = num(p.confidence) ? clamp(p.confidence, 0, 1) : .5;
  q.fresh = num(p.freshness) ? clamp(p.freshness, 0, 1) : null;
  q.missing = ['demand','saturation','fit'].filter(k => !num(p[k]));
  q.measured = q.missing.length === 0;
  q.dist = q.measured ? Math.hypot(100 - p.demand, p.saturation, 100 - p.fit) : null;
  q.front = q.measured && q.dist <= R;
  q.tone = tone(q.verdict);
  q.checkedAt = src.checkedAt || p.checkedAt || p.readAt || d.checkedAt || null;
  const ke = keepMap.get(q.id);
  q.keepStatus = ke ? ke.status : (p.kept || kept.has(q.id) ? 'kept' : null);
  q.kept = q.keepStatus === 'kept';
  q.keepEntry = ke || null;
  q.sample = !!(p.sample || d.sample || source === 'sample');
  return q;
}
function imgSrc(p, which) {
  const o = p[which] || {};
  const t = which === 'source' ? (p.sourceThumb || o.thumb) : (p.proofThumb || o.thumb);
  if (t) { if (/^https?:/.test(t)) return t; const i = t.indexOf('format-lab/'); return '/round-img/' + (i >= 0 ? t.slice(i + 11) : t.replace(/^\/+/, '')); }
  if (o.id) return '/round-img/' + encodeURIComponent(p.round) + '/img/' + encodeURIComponent(o.id) + '.jpg';
  return '';
}
function img(p, which, cls) {
  const o = p[which] || {}, s = imgSrc(p, which);
  if (!s) return '';
  const fb = o.id ? "this.onerror=function(){this.style.visibility='hidden'};this.src='" + ytThumb(o.id) + "'" : "this.style.visibility='hidden'";
  return '<img class="' + (cls||'') + '" src="' + esc(s) + '" alt="" loading="lazy" onerror="' + esc(fb) + '">';
}
const evItems = p => (p.evidence || []).map(e => typeof e === 'string' ? e : e && (e.url || e.href || e.path || (e.id && 'https://youtu.be/' + e.id))).filter(Boolean);
function links(p) { return evItems(p).filter(u => /^https?:\/\//.test(u)); }
const localEv = p => evItems(p).filter(u => !/^https?:\/\//.test(u));
async function loadKeeps() {
  try { const r = await fetch('/keeps.json', {cache:'no-store'}); if (!r.ok) return; const j = await r.json(); keepMap = new Map((j.entries || []).map(k => [k.id, k])); } catch (e) {}
}

async function load(force) {
  let res, src;
  try {
    res = await fetch('/state.json', {cache:'no-store'});
    if (!res.ok) throw new Error('HTTP ' + res.status);
    src = res.headers.get('X-Board-Source') || 'state';
  } catch (e) {
    if (data && !force) { setSource(source, 'state.json unreadable; showing the last good copy'); return; }
    try { res = await fetch('sample-state.json', {cache:'no-store'}); if (!res.ok) throw 0; src = 'sample'; }
    catch (e2) { showEmpty('No state.json and no sample-state.json. Start the board with python3 server.py.'); return; }
  }
  const text = await res.text();
  if (!force && text === lastText && src === source) return;
  let d; try { d = JSON.parse(text); } catch (e) { return; }
  lastText = text; source = (d.sample ? 'sample' : src); data = d;
  await loadKeeps();
  build();
}

function setSource(src, warn) {
  const b = $('#src');
  if (src === 'sample') { b.className = 'b warn'; b.textContent = 'Sample data'; }
  else { b.className = 'b live'; b.textContent = 'state.json' + (data && (data.updatedAt || data.generatedAt) ? ' · ' + String(data.updatedAt || data.generatedAt).slice(0, 16).replace('T', ' ') : ''); }
  if (warn) { b.className = 'b warn'; b.textContent = warn; }
  const n = $('#note');
  if (src === 'sample') { n.hidden = false; n.innerHTML = '<b>Sample data</b>' + esc(data && data.note || 'The runner has not written state.json yet.') ; }
  else n.hidden = true;
}

function build() {
  const raw = (data.points || (data.board && data.board.points) || []);
  const kept = keptIds(data);
  points = raw.filter(p => p && typeof p === 'object').map((p, i) => norm(p, i, data, kept));
  setSource(source);
  const rounds = [...new Set(points.map(p => p.round))].sort().reverse();
  $('#kicker').textContent = 'Harness board · demand × saturation × fit · ' + (rounds.length === 1 ? 'round ' + rounds[0] : rounds.length + ' rounds');
  fill('#f-round', 'round', rounds);
  fill('#f-verdict', 'verdict', [...new Set(points.map(p => p.verdict))].sort());
  fill('#f-niche', 'niche', [...new Set(points.map(p => p.niche))].sort());
  // rebuild meshes
  pointsRoot.children.slice().forEach(g => { g.traverse(o => o.isCSS2DObject && o.element.remove()); pointsRoot.remove(g); });
  meshes = [];
  for (const p of points) if (p.measured) pointsRoot.add(makePoint(p));
  const hashId = decodeURIComponent(location.hash.slice(1));
  if (pinned) pinned = points.find(p => p.id === pinned.id) || null;
  else if (hashId) pinned = points.find(p => p.id === hashId) || null;
  apply();
  renderDetail();
}

function makePoint(p) {
  const g = new THREE.Group(), c = new THREE.Color(COL[p.tone]);
  const x = W(clamp(p.demand,0,100)), y = W(clamp(p.saturation,0,100)), z = W(clamp(p.fit,0,100));
  const r = 1.1 + (p.fresh ?? .35) * 2.2;
  const m = new THREE.Mesh(sphere, new THREE.MeshStandardMaterial({color:c, emissive:c, emissiveIntensity:.12 + .6*p.conf, roughness:.38, metalness:.05, transparent:true, opacity:.5 + .5*p.conf}));
  m.position.set(x, y, z); m.scale.setScalar(r); m.userData = {p, r}; g.add(m); meshes.push(m);
  const h = new THREE.Sprite(new THREE.SpriteMaterial({map:haloTex, color:c, transparent:true, opacity:.2 + .35*p.conf, depthWrite:false, blending:THREE.AdditiveBlending}));
  h.position.copy(m.position); h.scale.setScalar(r * 5.5); g.add(h);
  const dl = new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x, y - r, z), new THREE.Vector3(x, -50, z)]), new THREE.LineDashedMaterial({color:c, dashSize:1.4, gapSize:1.4, transparent:true, opacity:.45}));
  dl.computeLineDistances(); g.add(dl);
  const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({color:c, transparent:true, opacity:.55, side:THREE.DoubleSide, depthWrite:false}));
  ring.rotation.x = -Math.PI/2; ring.position.set(x, -49.8, z); ring.scale.setScalar(r * 1.1); g.add(ring);
  const l = label(esc(p.id), 'pl' + (p.front ? ' front' : ''), x, y, z, [0, .5]);
  l.element.style.marginLeft = (r * 3 + 6) + 'px';
  g.add(l); g.userData = {p, mesh:m, label:l};
  return g;
}

function fill(sel, key, values) {
  const el = $(sel), cur = filters[key];
  el.innerHTML = '<option value="all">All</option>' + values.map(v => '<option value="' + esc(v) + '">' + esc(v) + '</option>').join('');
  filters[key] = values.includes(cur) ? cur : 'all'; el.value = filters[key];
}
const pass = p => (filters.round === 'all' || p.round === filters.round) && (filters.verdict === 'all' || p.verdict === filters.verdict) && (filters.niche === 'all' || p.niche === filters.niche);

function apply() {
  const shown = points.filter(pass);
  for (const g of pointsRoot.children) { const v = pass(g.userData.p); g.visible = v; g.userData.label.visible = v; }
  const on = shown.filter(p => p.measured), off = shown.filter(p => !p.measured);
  const named = new Set([...on].sort((a, b) => a.dist - b.dist).slice(0, 8).map(p => p.id));
  for (const g of pointsRoot.children) { const id = g.userData.p.id, el = g.userData.label.element; el.classList.toggle('off', !named.has(id)); el.classList.toggle('pin', !!pinned && pinned.id === id); }
  $('#count').innerHTML = '<b>' + on.length + '</b> on the chart · <b>' + off.length + '</b> not measured · <b>' + on.filter(p => p.front).length + '</b> inside the frontier';
  if (!points.length) showEmpty('state.json has no points yet.');
  else if (!on.length) showEmpty('No measured point matches these filters.');
  else $('#empty').hidden = true;
  // tray
  $('#tray-n').textContent = off.length + ' point' + (off.length === 1 ? '' : 's');
  $('#tray').innerHTML = off.length ? off.map(p => '<li tabindex="0" data-id="' + esc(p.id) + '" class="' + (pinned && pinned.id === p.id ? 'sel' : '') + '"><span class="b ' + p.tone + '">' + esc(p.verdict) + '</span><span class="t">' + esc(p.ourTitle || p.id) + '</span><span class="m">Missing: ' + esc(p.missing.join(', ')) + '</span></li>').join('') : '<li class="none">Every point here has all three axes.</li>';
  // table
  const rows = [...on].sort((a, b) => a.dist - b.dist).concat(off);
  const cell = (p, k) => num(p[k]) ? '<td class="r"><b>' + Math.round(p[k]) + '</b></td>' : '<td class="r na">not measured</td>';
  $('#table tbody').innerHTML = rows.map(p => '<tr tabindex="0" data-id="' + esc(p.id) + '" class="' + (p.front ? 'front ' : '') + (pinned && pinned.id === p.id ? 'sel' : '') + '">' +
    '<td><span class="idc"><code>' + esc(p.id) + '</code><button class="cp" data-copy="' + esc(p.id) + '" aria-label="Copy ID ' + esc(p.id) + '">Copy</button></span></td>' +
    '<td class="t">' + esc(p.ourTitle || '—') + '</td><td>' + esc(p.niche) + '</td>' +
    '<td><span class="b ' + p.tone + '">' + esc(p.verdict) + '</span>' + keepBadge(p, ' ') + (p.sample ? ' <span class="b">Sample</span>' : '') + '</td>' +
    cell(p, 'demand') + cell(p, 'saturation') + cell(p, 'fit') +
    '<td class="r">' + (p.fresh == null ? '—' : p.fresh.toFixed(2)) + '</td>' +
    '<td class="r">' + (p.dist == null ? '—' : '<b>' + Math.round(p.dist) + '</b>') + '</td>' +
    '<td>' + (p.query ? '<span class="qq">' + esc(p.query) + '</span>' : '<span class="na">no query</span>') + '<span class="dd">' + (p.checkedAt ? 'read ' + esc(p.checkedAt) : 'date missing') + '</span></td></tr>').join('');
}
function showEmpty(t) { const e = $('#empty'); e.hidden = false; e.textContent = t; }

// ---------- hover / pin ----------
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
let down = null;
function pick(ev) {
  const b = canvas.getBoundingClientRect();
  mouse.set((ev.clientX - b.left) / b.width * 2 - 1, -(ev.clientY - b.top) / b.height * 2 + 1);
  ray.setFromCamera(mouse, camera);
  const hit = ray.intersectObjects(meshes.filter(m => m.parent.visible), false)[0];
  return hit ? hit.object : null;
}
function setHover(m, ev) {
  if (hovered && hovered !== m) { hovered.scale.setScalar(hovered.userData.r); hovered.parent.userData.label.element.classList.remove('hot'); }
  hovered = m;
  const card = $('#hover');
  if (!m) { card.hidden = true; canvas.style.cursor = ''; return; }
  canvas.style.cursor = 'pointer';
  m.scale.setScalar(m.userData.r * 1.3); m.parent.userData.label.element.classList.add('hot');
  const p = m.userData.p, s = p.source || {}, ev2 = links(p);
  card.innerHTML = img(p, 'source', 'th') + '<div class="bd">' +
    '<div class="card-row"><span class="b ' + p.tone + '">' + esc(p.verdict) + '</span><span class="b m">' + esc(p.niche) + '</span>' + (p.front ? '<span class="b live">Frontier</span>' : '') + (p.sample ? '<span class="b">Sample</span>' : '') + '</div>' +
    '<div class="card-src"><span class="lab">Source</span><br>' + esc(s.title || '—') + '</div>' +
    '<div class="mono"><b>' + fmt(s.views) + '</b> views · checked <b>' + esc(p.checkedAt || '?') + '</b></div>' +
    '<div><span class="lab">Our title</span><div class="card-our">' + esc(p.ourTitle || '—') + '</div></div>' +
    '<div class="mono">D <b>' + Math.round(p.demand) + '</b> · S <b>' + Math.round(p.saturation) + '</b> · F <b>' + Math.round(p.fit) + '</b> · to corner <b>' + Math.round(p.dist) + '</b></div>' +
    (p.query ? '<div><span class="q">' + esc(p.query) + '</span></div>' : '') +
    '<div class="mono">' + ev2.length + ' evidence link' + (ev2.length === 1 ? '' : 's') + ' · click to pin</div></div>';
  card.hidden = false;
  placeCard(ev);
}
function placeCard(ev) {
  const card = $('#hover'), b = stage.getBoundingClientRect();
  let x = ev.clientX - b.left + 18, y = ev.clientY - b.top + 18;
  if (x + card.offsetWidth > b.width - 10) x = ev.clientX - b.left - card.offsetWidth - 18;
  if (y + card.offsetHeight > b.height - 10) y = Math.max(10, b.height - card.offsetHeight - 10);
  card.style.left = x + 'px'; card.style.top = y + 'px';
}
canvas.addEventListener('pointermove', ev => { const m = pick(ev); if (m !== hovered) setHover(m, ev); else if (m) placeCard(ev); });
canvas.addEventListener('pointerleave', () => setHover(null));
canvas.addEventListener('pointerdown', ev => { down = [ev.clientX, ev.clientY]; });
canvas.addEventListener('pointerup', ev => {
  if (!down || Math.hypot(ev.clientX - down[0], ev.clientY - down[1]) > 5) return;
  const m = pick(ev); if (m) pinPoint(m.userData.p);
});

function pinPoint(p, scroll) {
  pinned = p; renderDetail();
  for (const g of pointsRoot.children) g.userData.label.element.classList.toggle('pin', g.userData.p.id === p.id);
  history.replaceState(null, '', '#' + encodeURIComponent(p.id));
  document.querySelectorAll('[data-id]').forEach(e => e.classList.toggle('sel', e.dataset.id === p.id));
  if (scroll) stage.scrollIntoView({behavior:'smooth', block:'center'});
}
function keepBadge(p, pre) {
  if (!p.keepStatus) return '';
  return pre + (p.keepStatus === 'kept' ? '<span class="b live" title="' + esc((p.keepEntry && p.keepEntry.by) || '') + '">Kept</span>' : '<span class="b" title="' + esc((p.keepEntry && p.keepEntry.by) || '') + '">Proposed keep</span>');
}
function axisRow(name, v, inv, note, why) {
  const w = why ? '<div class="axw">' + esc(why) + '</div>' : '';
  if (!num(v)) return '<div class="axr na"><span>' + name + '</span><span class="tr"></span><b>—</b></div>' + w;
  return '<div class="axr' + (inv ? ' inv' : '') + '"><span>' + name + '</span><span class="tr"><i style="width:' + clamp(v,0,100) + '%"></i></span><b>' + (note || Math.round(v)) + '</b></div>' + w;
}
function renderDetail() {
  const el = $('#detail');
  if (!pinned) { el.innerHTML = '<div class="placeholder"><span class="n">Detail</span><p>Hover a point to read it. Click to pin it here with the evidence, the copy-ID button and the keep gate.</p></div>'; pin.visible = false; return; }
  const p = pinned, s = p.source || {}, pr = p.proof || null, ev = links(p), lev = localEv(p);
  const ax = (p.axes && typeof p.axes === 'object') ? p.axes : {};
  const reading = ax.reading && typeof ax.reading === 'object' ? Object.entries(ax.reading).map(([k, v]) => k + ': ' + v).join(' · ') : '';
  const cs = Array.isArray(p.crossSample) ? p.crossSample.filter(c => c && c.title) : [];
  const ytLink = (o, label) => o && o.id ? '<a href="' + ytUrl(o.id) + '" target="_blank" rel="noopener">' + img(p, label) + '<span>' + label + '</span></a>' : '';
  const th = [ytLink(s, 'source'), pr && pr.id ? ytLink(pr, 'proof') : ''].filter(Boolean);
  const canKeep = !p.sample && source !== 'sample' && !p.kept;
  const why = p.sample ? 'Sample data. Keep opens when the runner writes state.json.' : p.kept ? 'Already kept' + (p.keepEntry ? ' by ' + p.keepEntry.by + ' on ' + String(p.keepEntry.at || '').slice(0, 10) : '') + '.' : p.keepStatus === 'proposed' ? 'An agent proposed this keep' + (p.keepEntry ? ' (' + p.keepEntry.by + ')' : '') + '. It is not kept until you keep it.' : '';
  el.innerHTML = (th.length ? '<div class="d-th" style="grid-template-columns:repeat(' + th.length + ',1fr)">' + th.join('') + '</div>' : '') +
    '<div class="d-bd">' +
    '<div class="d-id"><code title="' + esc(p.id) + '">' + esc(p.id) + '</code><button class="btn" data-copy="' + esc(p.id) + '">Copy ID</button></div>' +
    '<div class="d-meta"><span class="b ' + p.tone + '">' + esc(p.verdict) + '</span><span class="b">confidence ' + Math.round(p.conf*100) + '%</span><span class="b m">' + esc(p.round) + '</span><span class="b m">' + esc(p.niche) + '</span>' + (p.front ? '<span class="b live">Inside frontier</span>' : '') + (p.reconciled === false ? '<span class="b" title="Single-agent verdict; the independent reconciler has not run">Not reconciled</span>' : p.reconciled ? '<span class="b live">Reconciled</span>' : '') + keepBadge(p, '') + (p.sample ? '<span class="b warn">Sample</span>' : '') + '</div>' +
    '<div><span class="lab">Our title</span><h3 class="d-title">' + esc(p.ourTitle || '—') + '</h3>' + (p.format ? '<div class="mono" style="margin-top:6px">Format · <b>' + esc(p.format) + '</b></div>' : '') + '</div>' +
    '<div class="axes">' + axisRow('Demand', p.demand, false, null, ax.demand) + axisRow('Saturation', p.saturation, true, null, ax.saturation) + axisRow('Fit', p.fit, false, null, ax.fit) + axisRow('Freshness', p.fresh == null ? null : p.fresh*100, false, p.fresh == null ? null : p.fresh.toFixed(2)) +
      '<div class="mono">' + (p.measured ? 'Distance to the best corner <b>' + Math.round(p.dist) + '</b> · frontier at ' + R : 'Not on the chart · missing ' + esc(p.missing.join(', '))) + '</div></div>' +
    '<div class="blk"><span class="lab">Source</span><div class="src"><b>' + esc(s.title || '—') + '</b><span class="mono"><b>' + fmt(s.views) + '</b> views · checked <b>' + esc(p.checkedAt || 'date missing') + '</b>' + (s.id ? ' · <a href="' + ytUrl(s.id) + '" target="_blank" rel="noopener">' + esc(s.id) + ' ↗</a>' : '') + '</span></div></div>' +
    (pr ? '<div class="blk"><span class="lab">Proof in the target niche</span><div class="src"><b>' + esc(pr.title || '—') + '</b><span class="mono"><b>' + fmt(pr.views) + '</b> views' + (pr.checkedAt ? ' · checked <b>' + esc(pr.checkedAt) + '</b>' : '') + (pr.id ? ' · <a href="' + ytUrl(pr.id) + '" target="_blank" rel="noopener">' + esc(pr.id) + ' ↗</a>' : '') + '</span></div></div>' : '') +
    '<div class="blk"><span class="lab">Query</span><div style="margin-top:4px">' + (p.query ? '<span class="q">' + esc(p.query) + '</span>' : '<span class="mono" style="color:var(--amber)">No query recorded</span>') + '</div></div>' +
    (p.notes ? '<div class="blk"><span class="lab">Notes</span><p>' + esc(p.notes) + '</p></div>' : '') +
    (p.contradiction || p.contradictions ? '<div class="blk"><span class="lab">Contradiction</span><p>' + esc([].concat(p.contradiction || p.contradictions).join(' ')) + '</p></div>' : '') +
    (p.axisNotes || reading || ax.period ? '<div class="blk"><span class="lab">How the axes were read</span><p>' + esc([p.axisNotes, reading, ax.period ? 'Period: ' + ax.period + (ax.readOn ? ', read ' + ax.readOn : '') : ''].filter(Boolean).join(' · ')) + '</p></div>' : '') +
    (cs.length ? '<div class="blk"><span class="lab">Already on the crossing</span><ul class="cs">' + cs.map(c => '<li>' + (c.id ? '<a href="' + ytUrl(c.id) + '" target="_blank" rel="noopener">' : '<span>') + '<b>' + fmt(c.views) + '</b> ' + esc(c.title) + (c.age ? ' <span class="mono">· ' + esc(c.age) + '</span>' : '') + (c.id ? '</a>' : '</span>') + '</li>').join('') + '</ul></div>' : '') +
    (ev.length ? '<div class="blk"><span class="lab">Evidence</span><ul class="ev">' + ev.map(u => '<li><a href="' + esc(u) + '" target="_blank" rel="noopener">' + esc(u.replace(/^https?:\/\//, '')) + '</a></li>').join('') + lev.map(u => '<li><code class="lp">' + esc(u) + '</code></li>').join('') + '</ul></div>' : lev.length ? '<div class="blk"><span class="lab">Evidence</span><ul class="ev">' + lev.map(u => '<li><code class="lp">' + esc(u) + '</code></li>').join('') + '</ul></div>' : '') +
    '<div class="gate"><span class="lab">Keep gate</span><p class="sub" style="margin:0">Your click writes the keep through nb.py, signed with the owner name the board server was started with (--by). The agent that proposed this point cannot keep it.</p>' +
      '<textarea id="keep-note" placeholder="Why you keep it (optional)"' + (canKeep ? '' : ' disabled') + '></textarea>' +
      '<div class="row"><button class="btn keep" id="keep-btn"' + (canKeep ? '' : ' disabled') + '>' + (p.kept ? 'Kept' : 'Keep') + '</button><button class="btn" data-copy="' + esc(p.id) + '">Copy ID</button></div>' +
      '<div class="msg" id="keep-msg">' + esc(why) + '</div></div></div>';
  const kb = $('#keep-btn'); if (kb && canKeep) kb.onclick = () => keep(p);
  const g = pointsRoot.children.find(g => g.userData.p.id === p.id);
  if (g && p.measured) { pin.position.copy(g.userData.mesh.position); pin.scale.setScalar(g.userData.mesh.userData.r * 1.6); pin.visible = g.visible; } else pin.visible = false;
}
async function keep(p) {
  const btn = $('#keep-btn'), msg = $('#keep-msg'), note = ($('#keep-note').value || '').trim();
  btn.disabled = true; msg.className = 'msg'; msg.textContent = 'Writing the keep…';
  try {
    const r = await fetch('/keep', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ids:[p.id], note})});
    const j = await r.json().catch(() => ({}));
    if (!r.ok || !j.ok) throw new Error(j.error || (j.stderr || '').trim() || ('HTTP ' + r.status));
    let out = {}; try { out = JSON.parse(j.stdout); } catch (e) {}
    const status = out.status || (/"status":\s*"(\w+)"/.exec(j.stdout || '') || [])[1] || 'written';
    if (status === 'kept') { msg.className = 'msg okm'; msg.textContent = 'Kept. nb.py wrote keeps.json.'; btn.textContent = 'Kept'; btn.classList.add('ok'); toast('Kept ' + p.id); }
    else { msg.className = 'msg err'; msg.textContent = 'Recorded as ' + status + ', not kept. Restart the board server and click again, or run: nb.py keep ' + p.id + ' --note "…" --by <your name>'; btn.textContent = 'Keep'; toast('Recorded as ' + status); }
    setTimeout(() => load(true), 400);
  } catch (e) { msg.className = 'msg err'; msg.textContent = 'Not kept: ' + e.message; btn.disabled = false; }
}

// ---------- ui ----------
function toast(t) { const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove('on'), 1400); }
async function copy(text) {
  try { await navigator.clipboard.writeText(text); }
  catch (e) { const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); }
  toast('Copied ' + text);
}
document.addEventListener('click', ev => {
  const c = ev.target.closest('[data-copy]'); if (c) { ev.stopPropagation(); copy(c.dataset.copy); return; }
  if (ev.target.closest('a')) return;
  const row = ev.target.closest('tr[data-id], #tray li[data-id]');
  if (row) { const p = points.find(p => p.id === row.dataset.id); if (p) pinPoint(p, !!row.closest('table')); }
});
document.addEventListener('keydown', ev => {
  if (ev.key === 'Enter' && ev.target.matches('tr[data-id], #tray li[data-id]')) { const p = points.find(p => p.id === ev.target.dataset.id); if (p) pinPoint(p, ev.target.matches('tr')); }
  if (ev.key === 'Escape' && pinned && !ev.target.matches('textarea')) { pinned = null; renderDetail(); history.replaceState(null, '', location.pathname); document.querySelectorAll('.sel').forEach(e => e.classList.remove('sel')); }
});
for (const [sel, k] of [['#f-round','round'], ['#f-verdict','verdict'], ['#f-niche','niche']]) $(sel).addEventListener('change', e => { filters[k] = e.target.value; apply(); renderDetail(); });

const VIEWS = {iso:[196, 118, 222], ds:[0, -6, 300], df:[0, 310, 0.01]};
let tween = null;
document.querySelectorAll('.views button').forEach(b => b.addEventListener('click', () => {
  const v = b.dataset.view;
  if (v === 'spin') { controls.autoRotate = !controls.autoRotate; b.classList.toggle('on', controls.autoRotate); b.setAttribute('aria-pressed', controls.autoRotate); return; }
  document.querySelectorAll('.views button:not([data-view=spin])').forEach(x => x.classList.toggle('on', x === b));
  tween = new THREE.Vector3(...VIEWS[v]); controls.target.set(0, v === 'iso' ? -8 : 0, 0);
}));

function resize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h, false); labels.setSize(w, h);
  camera.aspect = w / h; camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(stage); resize();

(function loop(t) {
  requestAnimationFrame(loop);
  if (tween) { camera.position.lerp(tween, .1); if (camera.position.distanceTo(tween) < .5) tween = null; }
  controls.update();
  if (pin.visible) { pin.quaternion.copy(camera.quaternion); pin.material.opacity = .65 + .3 * Math.sin((t || 0) / 260); }
  renderer.render(scene, camera); labels.render(scene, camera);
})();

load(true);
setInterval(() => load(false), 10000);
