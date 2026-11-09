// Thumbnails for "Why Evolution Keeps Turning Cars Into SUVs" · round 1 · 4 Oct 2026.
// Drawn in code as SVG (no image generation). Silhouettes are our own drawings; the Miura plate is from the Lamborghini film.
const INK = '#14110D', PAPER = '#EFE6D6', GOLD = '#C9A13B', ORANGE = '#E8702A', YEL = '#FFD21A', RED = '#E5281C', NIGHT = '#0B0A08';

// Each car: body path in a 400-wide box, ground line at y=150, window path, wheel x positions, wheel radius.
const CARS = {
  beetle: {b: 'M22,138 C20,112 40,104 66,100 C86,58 134,40 192,40 C262,40 304,68 332,104 C358,106 378,116 380,138 Z', w: 'M96,98 C108,68 140,54 184,54 L184,98 Z M196,54 C246,54 282,72 304,98 L196,98 Z', x: [98, 304], r: 27},
  saloon: {b: 'M14,136 L14,108 C14,100 30,96 72,92 L122,56 C130,50 142,48 160,48 L238,48 C254,48 264,52 274,60 L312,92 L374,98 C384,100 388,106 388,116 L388,136 Z', w: 'M92,92 L132,62 L192,62 L192,92 Z M204,62 L250,62 L292,92 L204,92 Z', x: [92, 312], r: 27},
  wedge: {b: 'M8,136 L10,120 L150,80 L216,56 L286,56 L338,80 L390,92 L392,136 Z', w: 'M168,82 L222,64 L250,64 L250,82 Z M260,64 L284,64 L320,82 L260,82 Z', x: [94, 316], r: 27},
  estate: {b: 'M14,136 L14,106 C14,98 30,94 74,90 L124,54 C132,48 142,47 160,47 L352,47 C368,47 378,56 382,70 L390,136 Z', w: 'M94,90 L134,60 L196,60 L196,90 Z M208,60 L282,60 L282,90 L208,90 Z M294,60 L350,60 C362,60 368,70 370,90 L294,90 Z', x: [92, 314], r: 27},
  suv: {b: 'M10,130 L10,92 C10,82 26,78 70,72 L120,24 C128,16 140,14 158,14 L326,14 C348,14 360,22 368,38 L386,84 C390,92 392,100 392,112 L392,130 Z', w: 'M92,72 L132,30 L196,30 L196,72 Z M208,30 L280,30 L280,72 L208,72 Z M292,30 L330,30 C344,30 350,38 362,72 L292,72 Z', x: [98, 310], r: 36},
};

// Draw one car. x,y = left and ground position, s = scale, col = body, bg = colour behind (for wheel arches and glass).
function car(name, x, y, s, col = INK, bg = PAPER, glass = 0.9, badge = '') {
  const c = CARS[name], gy = 150;
  const wheels = c.x.map((wx) => `<circle cx="${wx}" cy="${gy - c.r + 6}" r="${c.r + 6}" fill="${bg}"/><circle cx="${wx}" cy="${gy - c.r + 6}" r="${c.r}" fill="${col}"/><circle cx="${wx}" cy="${gy - c.r + 6}" r="${c.r * 0.42}" fill="${bg}"/>`).join('');
  return `<g transform="translate(${x},${y - gy * s}) scale(${s})"><path d="${c.b}" fill="${col}"/><path d="${c.w}" fill="${bg}" opacity="${glass}"/>${wheels}${badge}</g>`;
}
const outline = (name, x, y, s, col, sw = 5) => { const c = CARS[name]; return `<g transform="translate(${x},${y - 150 * s}) scale(${s})" fill="none" stroke="${col}" stroke-width="${sw / s}" stroke-linejoin="round"><path d="${c.b}"/>${c.x.map((wx) => `<circle cx="${wx}" cy="${150 - c.r + 6}" r="${c.r}"/>`).join('')}</g>`; };
// Generic badges (shapes only, no real logos): shield, roundel, wings.
const BADGE = {
  shield: (c) => `<path d="M-13,-15 L13,-15 L13,2 C13,12 6,17 0,20 C-6,17 -13,12 -13,2 Z" fill="${c}"/>`,
  round: (c) => `<circle r="15" fill="none" stroke="${c}" stroke-width="6"/><circle r="5" fill="${c}"/>`,
  wings: (c) => `<path d="M-26,-4 L26,-4 L18,6 L-18,6 Z" fill="${c}"/><rect x="-6" y="-11" width="12" height="22" fill="${c}"/>`,
};
const onDoor = (kind, col) => `<g transform="translate(244,100)">${BADGE[kind](col)}</g>`;
const txt = (t, x, y, size, col, anchor = 'middle', extra = '') => `<text x="${x}" y="${y}" font-family="Michroma, sans-serif" font-size="${size}" fill="${col}" stroke="${col}" stroke-width="${size * 0.035}" text-anchor="${anchor}" letter-spacing="${size * 0.02}" ${extra}>${t}</text>`;
const leg = (t, x, y, size, col, anchor = 'middle') => `<text x="${x}" y="${y}" font-family="Saira, sans-serif" font-weight="700" font-size="${size}" fill="${col}" text-anchor="${anchor}" letter-spacing="${size * 0.22}">${t}</text>`;
const grain = `<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.11 0"/></filter>`;
const stripes = (y, a, b, h = 16) => `<rect x="0" y="${y}" width="1280" height="${h}" fill="${a}"/><rect x="0" y="${y + h}" width="1280" height="${h * 0.45}" fill="${b}"/>`;
const wrap = (bg, inner) => `<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice"><defs>${grain}</defs><rect width="1280" height="720" fill="${bg}"/>${inner}<rect width="1280" height="720" filter="url(#g)"/></svg>`;
const arrow = (x1, y1, x2, y2, col, w = 10) => { const a = Math.atan2(y2 - y1, x2 - x1), h = w * 2.6; return `<line x1="${x1}" y1="${y1}" x2="${x2 - Math.cos(a) * h * 0.8}" y2="${y2 - Math.sin(a) * h * 0.8}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/><polygon points="${x2},${y2} ${x2 - Math.cos(a - 0.45) * h},${y2 - Math.sin(a - 0.45) * h} ${x2 - Math.cos(a + 0.45) * h},${y2 - Math.sin(a + 0.45) * h}" fill="${col}"/>`; };

window.THUMBS = [
  {id: 'A', name: 'The march', words: 'none',
   why: 'The evolution chart everyone knows, with cars. Four shapes walk left to right and the last one is the SUV, in the only colour. It says “evolution” before the title is read.',
   from: 'Our own layout. The title carries the borrowed formula; the picture pays off the word “evolution”.',
   svg: () => wrap(PAPER, `<rect x="0" y="560" width="1280" height="6" fill="${INK}"/>${car('beetle', 40, 560, 0.62)}${car('saloon', 300, 560, 0.66)}${car('wedge', 574, 560, 0.68)}${car('estate', 852, 560, 0.5)}${car('suv', 800, 560, 1.16, ORANGE)}${leg('1950', 164, 612, 26, INK)}${leg('1970', 432, 612, 26, INK)}${leg('1985', 710, 612, 26, INK)}${leg('TODAY', 1030, 612, 26, ORANGE)}${stripes(660, GOLD, INK)}`.replace(car('estate', 852, 560, 0.5), ''))},
  {id: 'B', name: 'One word, three brands', words: 'MISTAKE?',
   why: 'The source layout carried over: one accusing word across the top and near-identical faces under it. Here the faces are three SUVs with three different badges and one outline.',
   from: 'The Amazon Archives: big-cat faces under the word “MISTAKE” (1.05M).',
   svg: () => wrap(NIGHT, `${txt('MISTAKE?', 640, 190, 150, YEL)}${car('suv', 20, 600, 1.02, PAPER, NIGHT, 0.9, onDoor('shield', GOLD))}${car('suv', 436, 600, 1.02, PAPER, NIGHT, 0.9, onDoor('round', RED))}${car('suv', 852, 600, 1.02, PAPER, NIGHT, 0.9, onDoor('wings', YEL))}${stripes(650, GOLD, PAPER, 12)}`)},
  {id: 'C', name: 'Three outlines, one shape', words: 'SAME CAR.',
   why: 'Three makers’ outlines laid over each other in three inks, almost coinciding. The proof is in the picture: the viewer checks it for themselves.',
   from: 'Our own layout, in the film’s printing language (three passes of ink).',
   svg: () => wrap(PAPER, `${outline('suv', 150, 600, 2.42, RED, 7)}${outline('suv', 164, 592, 2.4, GOLD, 7)}${outline('suv', 140, 606, 2.44, INK, 7)}${txt('SAME CAR.', 640, 150, 104, INK)}${leg('3 BRANDS · 3 BADGES · 1 OUTLINE', 640, 676, 30, INK)}`)},
  {id: 'D', name: 'Then and now', words: '1966 · TODAY',
   why: 'One brand, two cars. The Miura plate from our film on the left, the SUV on the right, both under the same shield. It ties this video to the Lamborghini one.',
   from: 'Animated History: a frame split in two with a year over each side and a one-word question (704K).',
   svg: () => wrap(PAPER, `<rect x="640" y="0" width="640" height="720" fill="${NIGHT}"/><image href="img/miura-side.png" x="40" y="330" width="570"/>${car('suv', 700, 520, 1.3, YEL, NIGHT)}${txt('1966', 320, 150, 92, INK)}${txt('TODAY', 960, 150, 92, YEL)}${txt('WHY?', 640, 668, 120, ORANGE, 'middle', `paint-order="stroke" style="stroke:${NIGHT};stroke-width:22px"`)}`)},
  {id: 'E', name: 'The funnel', words: 'none',
   why: 'Four different cars on the left, four arrows, one SUV on the right. It reads in one glance at phone size and needs no words.',
   from: 'The evolution idea drawn as a diagram, the way the film draws its gauges.',
   svg: () => wrap(NIGHT, `${car('beetle', 50, 170, 0.56, PAPER, NIGHT)}${car('wedge', 40, 330, 0.6, PAPER, NIGHT)}${car('saloon', 44, 492, 0.58, PAPER, NIGHT)}${car('estate', 44, 656, 0.58, PAPER, NIGHT)}${arrow(310, 130, 560, 300, GOLD)}${arrow(310, 296, 560, 350, GOLD)}${arrow(310, 456, 560, 400, GOLD)}${arrow(310, 620, 560, 450, GOLD)}${car('suv', 600, 520, 1.6, ORANGE, NIGHT)}`)},
  {id: 'F', name: 'The march, at night', words: 'none',
   why: 'The same march on black with a yellow SUV. Higher contrast against a white feed and against the pale thumbnails car-design channels use.',
   from: 'Variant of A for contrast.',
   svg: () => wrap(NIGHT, `<rect x="0" y="560" width="1280" height="6" fill="${PAPER}"/>${car('beetle', 40, 560, 0.62, PAPER, NIGHT)}${car('saloon', 300, 560, 0.66, PAPER, NIGHT)}${car('wedge', 574, 560, 0.68, PAPER, NIGHT)}${car('suv', 800, 560, 1.16, YEL, NIGHT)}${arrow(180, 300, 760, 300, PAPER, 8)}${stripes(660, GOLD, PAPER)}`)},
];
window.TITLES = [
  {id: 't1', t: 'Why Evolution Keeps Turning Cars Into SUVs', note: 'The source title with one word swapped. The proven one.'},
  {id: 't2', t: 'Why Evolution Keeps Turning Supercars Into SUVs', note: 'Narrower and sharper: Lamborghini, Ferrari, Aston Martin. Fits thumbnail D.'},
  {id: 't3', t: 'Why Every Car Keeps Turning Into an SUV', note: 'Without “evolution”. Plainer, and further from the source.'},
];
window.META = {kicker: 'SUV evolution · thumbnail and title · round 1 · 4 Oct 2026', title: 'Why evolution keeps turning cars into SUVs', length: '19:30', channel: 'Our channel'};
window.SOURCE = {id: 'SfRc7xXE_fY', title: 'Why Evolution Keeps Turning Animals Into Cats', channel: 'The Amazon Archives', views: '1.05M', age: '27 Aug', subs: '4.6K'};
window.NEIGHBOURS = [
  {img: '-Y7xSIHdZ-8', t: 'Why boxy cars disappeared', c: 'Bart’s Car Stories', m: '520K views · 11 days ago', d: '18:42'},
  {img: 'lmY8ZQTZJVA', t: 'The Chevy That Hunted Hemi — Then GM Buried It On Purpose', c: 'Rare Car Storys', m: '655K views · 1 month ago', d: '31:07'},
  {img: 'n5ib_RIHY58', t: 'Porsche Lost 93% of Its Profit — Here’s WHY', c: 'The Sleeper List', m: '526K views · 12 days ago', d: '21:35'},
  {img: '2z86OVxTAO4', t: 'Death of Car Design', c: 'Bart’s Car Stories', m: '264K views · 4 weeks ago', d: '16:20'},
  {img: '2ZS01obvQR0', t: 'Every Gun With A Strange Mechanism Explained', c: 'Cowball', m: '1.7M views · 4 weeks ago', d: '12:48'},
  {img: 'csonTUj_cv0', t: 'The ENTIRE History of Germany in 32 Minutes', c: 'Animated History', m: '704K views · 3 weeks ago', d: '32:13'},
  {img: 'yZZqdPpvXdY', t: 'How a Fearless Engineer Built the World’s First Car', c: 'Hidden Genius', m: '535K views · 1 month ago', d: '14:09'},
  {img: 'nAWpLtG-kNs', t: 'How Long You’d Last in Every Prehistoric Era', c: 'Fossil', m: '9.4M views · 1 month ago', d: '22:51'},
];
