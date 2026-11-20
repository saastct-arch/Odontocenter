// Gera favicons, ícones do app e imagens de compartilhamento (Open Graph) a partir da logo.
// Uso: node make_icons.js   (requer playwright)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const P=JSON.parse(fs.readFileSync('parts.json','utf8'));
const toothSvg=fs.readFileSync('assets/logo/odontocenter-dente.svg','utf8');
const toothD=toothSvg.match(/ d="([^"]+)"/)[1];
const logo=P.logo_nav.replace('class="logo"','class="lg"');
const specs=JSON.parse(fs.readFileSync('og/specs.json','utf8'));
const FONT='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500&family=Instrument+Serif:ital@1&display=swap">';
const tooth=(fill,extra='')=>`<svg viewBox="0 0 100 100" ${extra}><path fill="${fill}" d="${toothD}"/></svg>`;
// favicon.svg: dente azul, troca para azul-claro no modo escuro
fs.writeFileSync('favicon.svg',`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><style>path{fill:#0858B8}@media (prefers-color-scheme:dark){path{fill:#2FA4D8}}</style><path d="${toothD}"/></svg>\n`);
fs.writeFileSync('icons/safari-pinned-tab.svg',`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="${toothD}"/></svg>\n`);
(async()=>{
  const b=await chromium.launch();
  async function shot(html,w,h,out,transparent=false){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
    await p.setContent(`<!doctype html><html><head>${FONT}<style>html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden;${transparent?'background:transparent':''}}*{box-sizing:border-box}</style></head><body>${html}</body></html>`,{waitUntil:'networkidle'});
    await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:out,omitBackground:transparent});await p.close()}
  // ícones transparentes (favicon.ico é montado depois em Python)
  for(const s of [16,32,48]) await shot(`<div style="width:${s}px;height:${s}px;padding:${s*0.04}px">${tooth('#0858B8','width="100%" height="100%"')}</div>`,s,s,`icons/favicon-${s}.png`,true);
  // ícones com fundo (Apple, Android, PWA)
  const app=(s,pad)=>`<div style="width:${s}px;height:${s}px;background:radial-gradient(120% 120% at 70% 0%,#0A63CC 0%,#0848A8 45%,#031A40 100%);display:grid;place-items:center"><div style="width:${s*(1-2*pad)}px;height:${s*(1-2*pad)}px">${tooth('#FFFFFF','width="100%" height="100%"')}</div></div>`;
  await shot(app(180,.18),180,180,'apple-touch-icon.png');
  await shot(app(192,.18),192,192,'icons/icon-192.png');
  await shot(app(512,.18),512,512,'icons/icon-512.png');
  await shot(app(512,.28),512,512,'icons/icon-512-maskable.png');
  // imagem de compartilhamento da página inicial
  const og=(bg,eyebrow,title,sub)=>`<div style="position:relative;width:1200px;height:630px;background:#031A40;color:#fff;font-family:'Hanken Grotesk',Arial,sans-serif;overflow:hidden">
    ${bg?`<img src="${bg}" style="position:absolute;right:0;top:0;width:62%;height:100%;object-fit:cover;filter:saturate(.92)">`:''}
    <div style="position:absolute;inset:0;background:${bg?'linear-gradient(90deg,#031A40 0%,#031A40 38%,rgba(3,26,64,.6) 60%,rgba(3,26,64,.15) 100%)':'radial-gradient(90% 120% at 85% 10%,#0A63CC 0%,#0848A8 38%,#031A40 80%)'}"></div>
    ${bg?'':`<div style="position:absolute;right:-40px;top:40px;width:520px;height:520px;opacity:.16;transform:rotate(-8deg)">${tooth('#FFFFFF','width="100%" height="100%"')}</div>`}
    <div style="position:absolute;left:72px;top:64px;width:380px;color:#fff">${logo.replace('fill="currentColor"','fill="#FFFFFF"')}</div>
    <div style="position:absolute;left:72px;bottom:72px;right:${bg?'520px':'200px'}">
      <div style="display:flex;align-items:center;gap:12px;font:500 18px/1 'Hanken Grotesk';letter-spacing:.14em;text-transform:uppercase;color:#9FD8F5;margin-bottom:22px"><span style="width:9px;height:9px;border-radius:50%;background:#19D3F3"></span>${eyebrow}</div>
      <div style="font:300 ${bg?64:76}px/1 'Hanken Grotesk';letter-spacing:-.035em">${title}</div>
      <div style="font:400 24px/1.4 'Hanken Grotesk';color:rgba(255,255,255,.85);margin-top:24px">${sub}</div>
    </div>
    <div style="position:absolute;left:0;right:0;bottom:0;height:8px;background:linear-gradient(90deg,#19D3F3,#2FA4D8,#0858B8)"></div></div>`;
  await shot(og(null,'Clínica odontológica em Ipatinga','O seu sorriso é a sua <span style="font-family:\'Instrument Serif\';font-style:italic">marca registrada</span>','Canaã e Centro · Segunda a sexta, 8h às 18h · Desde 2001'),1200,630,'og/og-home.png');
  const imgData=f=>'data:image/jpeg;base64,'+fs.readFileSync(f).toString('base64');
  for(const s of specs){
    const [a,...rest]=s.h1.split(' em ');
    await shot(og(imgData(`img/${s.img}.jpg`),'Especialidade · OdontoCenter',`${a}<br>em <span style="font-family:'Instrument Serif';font-style:italic">Ipatinga</span>`,'Unidades Canaã e Centro · Agende pelo WhatsApp'),1200,630,`og/og-${s.slug}.png`);
  }
  await shot(og(null,'LGPD','Política de privacidade e <span style="font-family:\'Instrument Serif\';font-style:italic">cookies</span>','OdontoCenter · Ipatinga-MG'),1200,630,'og/og-privacidade.png');
  await b.close();console.log('ok');
})();
