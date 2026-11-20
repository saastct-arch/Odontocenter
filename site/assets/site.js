(function(){
  var root=document.documentElement,reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  var vh=function(){return window.innerHeight||800};
  var UNITS={canaa:{nome:'Canaã',num:'5531996252944'},centro:{nome:'Centro',num:'5531975103555'}};
  function wa(u,text){return 'https://wa.me/'+UNITS[u].num+'?text='+encodeURIComponent(text)}
  function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(_){return null}}

  // ---------- animações de entrada
  var hero=$('.hero');
  if(!reduce&&'IntersectionObserver' in window){
    root.classList.add('anim');
    var els=$$('.rv,.rv-img,.ring');
    els.forEach(function(el){var r=el.getBoundingClientRect();if(r.top<vh()*0.98&&r.bottom>0)el.classList.add('in')});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);if(e.target.classList.contains('ring'))count(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.12});
    els.forEach(function(el){if(!el.classList.contains('in'))io.observe(el)});
    requestAnimationFrame(function(){requestAnimationFrame(function(){if(hero)hero.classList.add('ready');var d=$('.doc-hero');if(d)d.classList.add('ready')})});
  }else{if(hero)hero.classList.add('ready')}
  function count(ring){var s=$('[data-count]',ring);if(!s)return;var to=+s.getAttribute('data-count'),t0=null;function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1600),e=1-Math.pow(1-p,3);s.textContent=Math.round(to*e);if(p<1)requestAnimationFrame(step)}s.textContent='0';requestAnimationFrame(step)}

  // ---------- scroll: faixa fixa, parallax, menu fixo
  var pin=$('.pin'),media=$('.pin-media'),pcopy=$('.pin-copy'),stick=$('#stick'),pars=$$('[data-par]'),ticking=false;
  function onScroll(){ticking=false;var h=vh();
    if(root.classList.contains('anim')){
      if(pin){var r=pin.getBoundingClientRect(),tot=r.height-h,p=Math.min(1,Math.max(0,-r.top/(tot||1))),q=Math.min(1,p/0.55),e=1-Math.pow(1-q,2);
        media.style.setProperty('--iy',(14*(1-e))+'%');media.style.setProperty('--ix',(18*(1-e))+'%');media.style.setProperty('--ir',(28*(1-e))+'px');
        media.style.setProperty('--sc',(1.18-0.18*e).toFixed(3));media.style.setProperty('--ov',(0.15+0.45*e).toFixed(3));
        pcopy.style.setProperty('--op',Math.min(1,Math.max(0,(p-0.3)/0.3)).toFixed(3))}
      pars.forEach(function(img){var b=img.parentNode.getBoundingClientRect();if(b.bottom<0||b.top>h)return;var k=((b.top+b.height/2)-h/2)/h;img.style.transform='translate3d(0,'+(k*-6).toFixed(2)+'%,0)'});
    }
    if(stick){var top=hero||$('.doc-hero'),show=top?top.getBoundingClientRect().bottom<0:window.scrollY>400;stick.classList.toggle('show',show);stick.setAttribute('aria-hidden',show?'false':'true');$$('a,button',stick).forEach(function(x){x.tabIndex=show?0:-1})}
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});
  window.addEventListener('resize',onScroll);onScroll();

  // ---------- menu do celular
  var drawer=$('#drawer');
  function menu(o){root.classList.toggle('menu-open',o);$$('.burger').forEach(function(b){b.setAttribute('aria-expanded',o?'true':'false')});if(drawer){drawer.setAttribute('aria-hidden',o?'false':'true');if(o){var c=$('.drawer-close',drawer);c&&c.focus()}}}
  $$('.burger').forEach(function(b){b.addEventListener('click',function(){menu(!root.classList.contains('menu-open'))})});
  if(drawer){$$('a',drawer).forEach(function(a){a.addEventListener('click',function(){menu(false)})});$('.drawer-close',drawer).addEventListener('click',function(){menu(false)})}

  // ---------- formulário → WhatsApp (o botão é um link real: abre no primeiro clique)
  var form=$('#form-agenda');
  function clear(el){el&&el.classList.remove('invalid')}
  function val(n){var c=$('input[name='+n+']:checked');return c?c.value:''}
  if(form){
    var send=$('#send');
    var setUnit=function(u){var r=$('input[name=unidade][value='+u+']',form);if(r){r.checked=true;clear($('#f-unit'))}};
    $$('a[data-unit]').forEach(function(a){a.addEventListener('click',function(){setUnit(a.getAttribute('data-unit'))})});
    $$('input[name=tipo]',form).forEach(function(r){r.addEventListener('change',function(){$('#conv-box').hidden=(r.value!=='Convênio'||!r.checked);clear($('#f-tipo'))})});
    $$('input,select',form).forEach(function(i){i.addEventListener('change',function(){clear(i.closest('fieldset,#f-serv,#f-nome,.conv'))});i.addEventListener('input',function(){clear(i.closest('#f-nome'))})});
    var build=function(mark){
      var unit=val('unidade'),serv=$('#servico').value,tipo=val('tipo'),conv=$('#convenio').value,nome=$('#nome').value.trim(),desc=$('#desc').value.trim(),bad=[];
      function chk(ok,el){if(!el)return;if(!ok){bad.push(el);if(mark)el.classList.add('invalid')}else clear(el)}
      chk(!!unit,$('#f-unit'));chk(!!serv,$('#f-serv'));chk(!!tipo,$('#f-tipo'));
      chk(tipo!=='Convênio'||!!conv,$('.conv'));if(mark&&tipo==='Convênio'&&!conv){$('#f-tipo').classList.add('invalid')}
      chk(nome.length>1,$('#f-nome'));
      if(bad.length)return {bad:bad};
      var tx='Olá! Vim pelo site da OdontoCenter e gostaria de agendar.\n\n*Unidade:* '+UNITS[unit].nome+'\n*Serviço:* '+serv+'\n*Atendimento:* '+(tipo==='Convênio'?'Convênio ('+conv+')':'Particular')+'\n*Paciente:* '+nome+(desc?'\n*Observações:* '+desc:'')+'\n\nPodem confirmar um horário? Obrigado!';
      return {url:wa(unit,tx)};
    };
    var sync=function(){var r=build(false);send.href=r.url||'#agendar'};
    form.addEventListener('input',sync);form.addEventListener('change',sync);
    send.addEventListener('click',function(e){var r=build(true);if(r.bad){e.preventDefault();var f=r.bad[0];f.scrollIntoView({block:'center'});var fe=$('input,select',f);if(fe)fe.focus({preventScroll:true});return}send.href=r.url});
    form.addEventListener('submit',function(e){e.preventDefault();send.click()});
  }
  $$('[data-wa]').forEach(function(a){var u=a.getAttribute('data-wa'),s=a.getAttribute('data-svc');a.href=wa(u,'Olá! Vim pelo site da OdontoCenter e gostaria de '+(s?'agendar uma avaliação de '+s+' na':'falar com a')+' unidade '+UNITS[u].nome+'.');a.target='_blank';a.rel='noopener'});

  // ---------- aviso do topo, unidades, abas
  var ax=$('#announce-x');if(ax)ax.addEventListener('click',function(){$('#announce').hidden=true});
  var photos=$$('.photos img');
  $$('.item > button').forEach(function(b){b.addEventListener('click',function(){var it=b.parentNode,o=!it.classList.contains('open');$$('.item.open').forEach(function(x){x.classList.remove('open');$('button',x).setAttribute('aria-expanded','false')});if(o){it.classList.add('open');b.setAttribute('aria-expanded','true');var i=+it.getAttribute('data-photo');photos.forEach(function(p,k){p.classList.toggle('on',k===i)})}})});
  var tabs=$$('.tab');
  function selTab(t){tabs.forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false');x.tabIndex=x===t?0:-1});$$('.tcard').forEach(function(c){c.hidden=c.id!==t.getAttribute('aria-controls')})}
  tabs.forEach(function(t,i){t.addEventListener('click',function(){selTab(t)});t.addEventListener('keydown',function(e){var n=e.key==='ArrowRight'?i+1:e.key==='ArrowLeft'?i-1:-1;if(n>=0){n=(n+tabs.length)%tabs.length;tabs[n].focus();selTab(tabs[n])}})});

  // ---------- WhatsApp flutuante
  var fab=$('#fab-btn'),pop=$('#fab-pop');
  function toggle(o){pop.classList.toggle('open',o);fab.setAttribute('aria-expanded',o?'true':'false')}
  $$('[data-fab]').forEach(function(a){var u=a.getAttribute('data-fab');a.href=wa(u,'Olá! Vim pelo site da OdontoCenter e gostaria de falar com a unidade '+UNITS[u].nome+'.');a.addEventListener('click',function(){toggle(false)})});
  if(fab){fab.addEventListener('click',function(){toggle(!pop.classList.contains('open'))});document.addEventListener('click',function(e){if(!$('#fab').contains(e.target))toggle(false)})}
  document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;if(pop&&pop.classList.contains('open')){toggle(false);fab.focus()}if(root.classList.contains('menu-open'))menu(false)});

  // ---------- aviso de cookies (LGPD)
  var ck=$('#cookie');
  if(ck&&!store('oc-cookies')){ck.classList.add('show');$$('[data-ck]',ck).forEach(function(b){b.addEventListener('click',function(){store('oc-cookies',b.getAttribute('data-ck'));ck.classList.remove('show')})})}
})();
