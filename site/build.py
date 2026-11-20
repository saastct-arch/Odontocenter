"""Gera o site da OdontoCenter: página inicial, páginas de especialidade e política de privacidade.
python3 build.py  -> escreve index.html, artifact.html, especialidades/*.html, politica-de-privacidade.html
"""
import json, re, html
from pages import SPECS

P = json.load(open('parts.json'))
WA = P['wa']
AR = '<svg class="ar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&display=swap">'
HOURS = 'Segunda a sexta, das 8h às 18h'
# Endereço público do site. Trocar pelo domínio definitivo quando estiver registrado e rodar o build de novo.
SITE_URL = 'https://odontocenter-ipatinga.vercel.app'
U = {
 'canaa': dict(nome='Canaã', rua='Rua dos Profetas, 210', bairro='Canaã', cep='35164-201', fone='(31) 99625-2944', tel='+5531996252944', extra=''),
 'centro': dict(nome='Centro', rua='Rua Juiz de Fora, 60, sala 102', bairro='Centro', cep='35160-031', fone='(31) 97510-3555', tel='+5531975103555', extra='Edifício Sandra Andrade'),
}
def maps(u):
    q = f"{u['rua']} - {u['bairro']}, Ipatinga - MG, {u['cep']}"
    return 'https://www.google.com/maps/search/?api=1&query=' + re.sub(r'\s+', '+', q)
def addr(u, sep=' · '):
    return f"{u['rua']}{(', ' + u['extra']) if u['extra'] else ''}{sep}{u['bairro']}, Ipatinga-MG{sep}CEP {u['cep']}"

def nav(pre, home):
    h = '' if home else pre + 'index.html'
    links = [('Especialidades', h + '#especialidades'), ('Unidades', h + '#unidades'), ('Convênios', h + '#convenios'), ('Equipe', h + '#equipe'), ('Dúvidas', h + '#duvidas')]
    lk = ''.join(f'<a href="{u}">{t}</a>' for t, u in links)
    return (f'<a href="{h or "#topo"}" aria-label="OdontoCenter, página inicial">{P["logo_nav"]}</a><nav aria-label="Principal">{lk}</nav>'
            f'<div class="end"><a class="tel btn btn-ob" href="tel:+5531996252944">(31) 99625-2944</a><a class="btn btn-b" href="#agendar">Agendar avaliação</a>'
            f'<button class="burger" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="drawer"><span></span></button></div>')

def drawer(pre, home):
    h = '' if home else pre + 'index.html'
    links = [('Especialidades', h + '#especialidades'), ('Unidades', h + '#unidades'), ('Convênios', h + '#convenios'), ('Equipe', h + '#equipe'), ('Dúvidas', h + '#duvidas'), ('Agendar avaliação', '#agendar')]
    sub = ''.join(f'<a href="{pre}especialidades/{s["slug"]}.html">{s["name"]}</a>' for s in SPECS)
    return (f'<div class="drawer" id="drawer" aria-hidden="true" role="dialog" aria-label="Menu"><button class="drawer-close" type="button" aria-label="Fechar menu">×</button>'
            + ''.join(f'<a class="dl" href="{u}">{t}{AR}</a>' for t, u in links)
            + f'<div class="dsub">{sub}</div><div class="dbot"><a class="btn btn-wa" data-wa="canaa" href="#">{WA} WhatsApp Canaã</a><a class="btn btn-wa" data-wa="centro" href="#">{WA} WhatsApp Centro</a><span class="hours">{HOURS}</span></div></div>')

def announce(pre):
    return f'<div class="announce" id="announce"><span><b style="font-weight:500">Site proposta</b> · equipe, CRO e fotos são ilustrativos. Conheça os <a href="{pre}index.html#convenios">convênios aceitos</a>.</span><button type="button" id="announce-x" aria-label="Fechar aviso">×</button></div>'

def form(service=None):
    if service:
        serv = f'<div id="f-serv"><span class="lb">2. Tratamento</span><div class="svc-chip"><span>{service["name"]}<small>Você pode detalhar a sua necessidade no último campo</small></span></div><input type="hidden" id="servico" value="{service["svc"]}"></div>'
    else:
        serv = f'<div id="f-serv"><label class="lb" for="servico">2. Qual serviço você procura?</label><select id="servico" name="servico" required><option value="">Selecione</option>{P["svc_opts"]}</select><p class="err">Escolha um serviço.</p></div>'
    units = ''.join(f'<label><input type="radio" name="unidade" value="{k}"><span class="c">{u["nome"]}<small>{u["rua"]}</small></span></label>' for k, u in U.items())
    return f'''<form class="card rv" style="--d:.12s" id="form-agenda" novalidate>
    <fieldset id="f-unit"><legend>1. Qual unidade?</legend><div class="choices units">{units}</div><p class="err">Escolha uma unidade.</p></fieldset>
    {serv}
    <fieldset id="f-tipo"><legend>3. Como será o atendimento?</legend>
      <div class="choices"><label><input type="radio" name="tipo" value="Convênio"><span class="c">Convênio</span></label><label><input type="radio" name="tipo" value="Particular"><span class="c">Particular</span></label></div><p class="err">Informe se é convênio ou particular.</p>
      <div class="conv" id="conv-box" hidden style="margin-top:14px"><label class="lb" for="convenio">Qual convênio?</label><select id="convenio" name="convenio"><option value="">Selecione</option>{P["conv_opts"]}</select><p class="err">Escolha o convênio.</p></div></fieldset>
    <div id="f-nome"><label class="lb" for="nome">4. Nome do paciente</label><input type="text" id="nome" name="nome" autocomplete="name" required placeholder="Nome completo"><p class="err">Informe o nome do paciente.</p></div>
    <div><label class="lb" for="desc">5. Conte o que você precisa <span class="opt">(opcional)</span></label><textarea id="desc" name="desc" placeholder="Ex.: dor no dente, orçamento, consulta para meu filho de 8 anos"></textarea></div>
    <div class="submit"><a class="btn btn-wa" id="send" href="#agendar" target="_blank" rel="noopener" role="button">{WA} Enviar para o WhatsApp</a><p>Abre a conversa com a unidade escolhida, com a mensagem pronta. Atendimento {HOURS.lower()}.</p></div>
  </form>'''

def cta(service=None):
    t = f'Agende sua avaliação de <span class="it">{service["lower"]}</span>' if service else 'Agende sua <span class="it">avaliação</span>'
    return f'''<section class="cta light" id="agendar" aria-labelledby="h-ag"><div class="wrap"><div class="cta-grid">
  <div>
    <span class="eyebrow rv">Agendamento</span>
    <h2 class="rv" id="h-ag" style="--d:.08s">{t}</h2>
    <p class="intro rv" style="--d:.16s">Preencha em menos de um minuto. Ao enviar, abrimos o WhatsApp da unidade com a mensagem pronta.</p>
    <ol class="steps rv" style="--d:.22s"><li><span>01</span>Escolha a unidade mais perto de você.</li><li><span>02</span>Informe se o atendimento é por convênio ou particular.</li><li><span>03</span>Envie pelo WhatsApp e a recepção confirma o seu horário.</li></ol>
    <p class="hours rv" style="--d:.28s;margin-top:22px">{HOURS}, nas duas unidades</p>
  </div>
  {form(service)}
</div></div></section>'''

def footer(pre, home):
    h = '' if home else pre + 'index.html'
    sp = ''.join(f'<a href="{pre}especialidades/{s["slug"]}.html">{s["name"]}</a>' for s in SPECS)
    un = ''.join(f'<p style="margin-top:{14 if i else 0}px">{u["nome"]}<br><span style="color:var(--dull)">{u["rua"]}{"<br>" + u["extra"] if u["extra"] else ""}<br>{u["bairro"]}, Ipatinga-MG · CEP {u["cep"]}<br>{u["fone"]}</span></p>' for i, u in enumerate(U.values()))
    return f'''<footer>
  <div class="fcols">
    <div><h4>Especialidades</h4>{sp}</div>
    <div><h4>Unidades</h4>{un}<p class="hours" style="margin-top:14px">{HOURS}</p></div>
    <div><h4>OdontoCenter</h4><a href="{h}#equipe">Equipe</a><a href="{h}#convenios">Convênios</a><a href="{h}#unidades">Unidades</a><a href="{h}#duvidas">Perguntas frequentes</a><a href="#agendar">Agendar avaliação</a><a href="{pre}politica-de-privacidade.html">Política de privacidade</a><a href="https://www.instagram.com/odontocenter.ipa/" target="_blank" rel="noopener">Instagram</a></div>
    <div class="fcard"><p>Fale com a recepção pelo WhatsApp</p><a class="btn btn-wa" data-wa="canaa" href="#">{WA} Unidade Canaã</a><a class="btn btn-wa" data-wa="centro" href="#">{WA} Unidade Centro</a></div>
  </div>
  <div class="fbig" aria-hidden="true">{P["logo_foot"].replace('class="logo foot"', 'class="foot"')}</div>
  <div class="legal"><span>© 2026 OdontoCenter · Centro Odontológico Especializado Ltda · CNPJ 04.598.376/0001-09</span><span><b>Responsável técnico:</b> Dr. Rafael Moreira · CRO-MG 00000 (dado fictício da proposta)</span><span><a href="{pre}politica-de-privacidade.html">Política de privacidade e cookies</a></span></div>
</footer>'''

def fab_cookie(pre):
    return f'''<div class="fab" id="fab">
  <div class="fab-pop" id="fab-pop" role="dialog" aria-label="Escolha a unidade para conversar no WhatsApp"><h2>Falar no WhatsApp</h2><p>Para qual unidade você quer mandar mensagem?</p>
    <a class="opt-u" data-fab="canaa" href="#" target="_blank" rel="noopener">{WA}<span>Unidade Canaã<small>{U["canaa"]["rua"]}</small></span></a>
    <a class="opt-u" data-fab="centro" href="#" target="_blank" rel="noopener">{WA}<span>Unidade Centro<small>{U["centro"]["rua"]}</small></span></a></div>
  <button class="fab-btn" id="fab-btn" type="button" aria-label="Falar no WhatsApp: escolher unidade" aria-expanded="false" aria-controls="fab-pop">{WA}</button>
</div>
<div class="cookie" id="cookie" role="region" aria-label="Aviso de cookies"><h2>Sua privacidade</h2><p>Usamos apenas o armazenamento essencial para o funcionamento do site. Saiba mais na nossa <a href="{pre}politica-de-privacidade.html">política de privacidade</a>.</p><div class="row"><button class="btn btn-b" type="button" data-ck="ok">Entendi</button><button class="btn btn-ob" type="button" data-ck="essential">Apenas essenciais</button></div></div>'''

def ld_units():
    out = []
    for k, u in U.items():
        out.append({"@context": "https://schema.org", "@type": "Dentist", "name": f"OdontoCenter {u['nome']}", "url": SITE_URL + "/",
                    "telephone": u['tel'], "foundingDate": "2001-08-09", "priceRange": "$$", "hasMap": maps(u),
                    "address": {"@type": "PostalAddress", "streetAddress": f"{u['rua']} - {u['bairro']}", "addressLocality": "Ipatinga", "addressRegion": "MG", "postalCode": u['cep'], "addressCountry": "BR"},
                    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
                    "sameAs": ["https://www.instagram.com/odontocenter.ipa/"]})
    return out
def ld_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def faq_html(faq):
    return ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq))

def page(title, desc, pre, body, canonical, full=True, og='og-home.jpg', og_alt='OdontoCenter, clínica odontológica em Ipatinga'):
    """full=True: documento completo (site e páginas extras). full=False: fragmento da página principal do artifact."""
    links = f'{FONTS}\n<link rel="stylesheet" href="{pre}assets/site.css">'
    tail = f'<script src="{pre}assets/site.js"></script>'
    if not full:
        return f'<title>OdontoCenter Ipatinga</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{links}\n<style>body{{margin:0}}</style>\n{body}\n{tail}\n'
    url = SITE_URL + '/' + re.sub(r'\.html$', '', canonical)
    img = f'{SITE_URL}/og/{og}'
    e = html.escape
    head = (f'<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<title>{e(title)}</title>\n<meta name="description" content="{e(desc)}">\n<link rel="canonical" href="{url}">\n'
            f'<meta name="theme-color" content="#031A40">\n<meta name="application-name" content="OdontoCenter">\n<meta name="apple-mobile-web-app-title" content="OdontoCenter">\n<meta name="format-detection" content="telephone=no">\n'
            f'<link rel="icon" href="{pre}favicon.ico" sizes="48x48">\n<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">\n'
            f'<link rel="mask-icon" href="{pre}icons/safari-pinned-tab.svg" color="#0858B8">\n<link rel="manifest" href="{pre}site.webmanifest">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="OdontoCenter">\n<meta property="og:locale" content="pt_BR">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:title" content="{e(title)}">\n<meta property="og:description" content="{e(desc)}">\n'
            f'<meta property="og:image" content="{img}">\n<meta property="og:image:secure_url" content="{img}">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="{e(og_alt)}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{e(title)}">\n<meta name="twitter:description" content="{e(desc)}">\n<meta name="twitter:image" content="{img}">\n<meta name="twitter:image:alt" content="{e(og_alt)}">\n')
    return (head + f'{links}\n<style>html,body{{margin:0}}:root{{color-scheme:dark}}</style>\n</head>\n<body>\n{body}\n{tail}\n</body>\n</html>\n')

def shell(pre, home, main):
    return (f'<a class="skip" href="#conteudo">Ir para o conteúdo</a>\n{announce(pre)}\n<div class="navcard stick" id="stick" aria-hidden="true">{nav(pre, home)}</div>\n'
            f'{drawer(pre, home)}\n<main id="conteudo">\n{main}\n</main>\n{footer(pre, home)}\n{fab_cookie(pre)}')

# ------------------------------------------------------------ página inicial
HOME_FAQ = [
 ('Como agendo uma consulta?', 'Preencha o formulário desta página: escolha a unidade, o serviço e se o atendimento será por convênio ou particular. Ao enviar, abrimos o WhatsApp da unidade com a mensagem pronta, e a recepção confirma o horário com você.'),
 ('Qual é o horário de atendimento?', 'As duas unidades atendem de segunda a sexta, das 8h às 18h.'),
 ('Qual unidade fica mais perto de mim?', f'A unidade Canaã fica na {U["canaa"]["rua"]}, bairro Canaã. A unidade Centro fica na {U["centro"]["rua"]}, Edifício Sandra Andrade, no Centro de Ipatinga.'),
 ('A clínica atende crianças?', 'Sim, a OdontoCenter tem atendimento pensado para crianças. Ao agendar, informe a idade da criança no campo de descrição.'),
 ('O que levo na primeira consulta?', 'Leve um documento com foto e, se o atendimento for por convênio, a carteirinha. Se tiver radiografias ou exames anteriores, leve também.'),
 ('Posso marcar para outra pessoa?', 'Pode. Informe o nome do paciente no formulário e use a descrição para contar a necessidade.'),
 ('Como remarco ou cancelo um horário?', 'Pelo WhatsApp da unidade onde você agendou, com antecedência, para que o horário seja liberado para outro paciente.'),
]

def home(pre, full):
    m = open('main_body.html').read()
    m = m.replace('<main id="conteudo">\n', '').replace('</main>\n', '').replace('</main>', '')
    # H1 com palavras de busca; a frase da marca vira o título visual
    a = m.index('<h1>'); b = m.index('</h1>') + 5
    m = m[:a] + ('<h1 class="hero-eyebrow rv" style="--d:.05s">Clínica odontológica em Ipatinga · desde 2001</h1>'
                 '<p class="tagline" aria-hidden="false"><span class="ln"><span style="--d:.15s">O seu sorriso</span></span><span class="ln"><span style="--d:.27s">é a sua <span class="it">marca</span></span></span><span class="ln"><span style="--d:.39s"><span class="it">registrada</span></span></span></p>') + m[b:]
    m = m.replace('<p class="sub rv" style="--d:.55s">Odontologia completa em Ipatinga, com especialistas, convênios e atendimento humanizado desde 2001.</p>',
                  f'<p class="sub rv" style="--d:.55s">Dentistas especialistas, convênios e atendimento humanizado no Canaã e no Centro. {HOURS}.</p>')
    # cards levam às páginas das especialidades
    for s in SPECS:
        m = re.sub(r'href="#agendar" data-service="' + re.escape(s['svc']) + '"', f'href="{pre}especialidades/{s["slug"]}.html"', m)
    # unidades: endereço com bairro e CEP, telefone confirmado, horário
    for k, u in U.items():
        old = re.search(r'<div class="inner">.*?<div class="row">.*?</div></div>', m[m.index('Unidade ' + u['nome']):], re.S).group(0)
        new = (f'<div class="inner"><p>{addr(u)}</p><p>Telefone e WhatsApp <a href="tel:{u["tel"]}">{u["fone"]}</a></p><p class="hours" style="margin-top:6px">{HOURS}</p>'
               f'<div class="row"><a class="btn btn-e btn-sm" data-unit="{k}" href="#agendar">Agendar nesta unidade</a><a class="btn btn-o btn-sm" href="{maps(u)}" target="_blank" rel="noopener">Ver no mapa</a></div></div>')
        m = m.replace(old, new, 1)
    # formulário sem horário
    a = m.index('<section class="cta light"'); b = m.index('</section>', a) + 10
    m = m[:a] + cta() + m[b:]
    conv = [('LumarMetals', ''), ('AAPI', ''), ('Novo Oriente', 'plano de assistência familiar'), ('Cenibra', ''), ('Postal Saúde', 'Correios'), ('COPASS Saúde', ''), ('Rede UNNA', 'Bradesco · Unimed · OdontoPrev')]
    logos = ''.join(f'<div>{n}{f"<small>{s}</small>" if s else ""}</div>' for n, s in conv)
    people = [('Dra. Helena Marques', 'Ortodontia', 'Canaã', 'seg, qua e sex', 'canaa', 'd1'), ('Dr. Rafael Moreira', 'Implantes e cirurgias', 'Centro', 'ter e qui', 'centro', 'd2'),
              ('Dra. Camila Torres', 'Estética, dentística e prótese', 'Canaã', 'seg a qui', 'canaa', 'd3'), ('Dr. Lucas Ferreira', 'Endodontia e periodontia', 'Centro', 'seg, qua e sex', 'centro', 'd4')]
    tabs = tc = ''
    for i, (n, e, u, d, uk, im) in enumerate(people):
        tabs += f'<button class="tab" role="tab" id="tab{i}" aria-selected="{"true" if i == 0 else "false"}" aria-controls="tc{i}" tabindex="{0 if i == 0 else -1}" type="button">{n}</button>'
        tc += (f'<div class="tcard" role="tabpanel" id="tc{i}" aria-labelledby="tab{i}"{"" if i == 0 else " hidden"}><div class="av"><img src="{pre}img/{im}.jpg" alt="Foto ilustrativa de {n}" loading="lazy"></div>'
               f'<div class="body"><p class="meta">{e}</p><h3>{n}</h3><dl><dt>Registro</dt><dd>CRO-MG 00000 <em>(fictício)</em></dd><dt>Unidade</dt><dd>{u}</dd><dt>Atendimento</dt><dd>{d}</dd></dl>'
               f'<a class="btn btn-b" href="#agendar" data-unit="{uk}">Agendar com {n.split()[0]} {n.split()[1]} {AR}</a></div></div>')
    rep = dict(tooth_big='<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M7.57,43.25 C 3.04,26.35 19.18,14.78 35.95,17.53 C 39.40,18.42 43.39,17.35 45.93,14.86 C 59.08,4.09 78.84,6.04 83.37,22.94 C 87.45,38.15 79.28,47.59 79.60,64.72 C 81.00,77.93 76.83,86.29 70.84,87.90 C 64.86,89.50 59.24,76.51 54.98,68.59 C 55.25,77.58 56.88,91.64 50.90,93.24 C 44.91,94.84 37.12,89.69 31.73,77.54 C 23.43,62.55 11.65,58.46 7.57,43.25Z"/></svg>', ar=AR, logos=logos, logos_dup=logos.replace('<div>', '<div aria-hidden="true">'), tabs=tabs, tcards=tc, wa=WA, navinner=nav(pre, True), faq_html=faq_html(HOME_FAQ))
    m = re.sub(r'\{\{img:(\w+)\}\}', lambda x: f'{pre}img/{x.group(1)}.jpg', m)
    for k, v in rep.items(): m = m.replace('{{' + k + '}}', v)
    m = m.replace('<div class="meta rv" style="--d:.8s"><div><b>25 anos</b>em Ipatinga</div>', '<div class="meta rv" style="--d:.8s"><div><b>25 anos</b>em Ipatinga</div>')
    assert '{{' not in m, re.findall(r'\{\{\w+', m)[:5]
    ld = ld_units() + [ld_faq(HOME_FAQ)]
    body = shell(pre, True, m) + f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    return page('Dentista em Ipatinga | OdontoCenter, clínica odontológica desde 2001',
                'Clínica odontológica em Ipatinga há 25 anos: ortodontia, implantes, estética, bruxismo e mais. Unidades Canaã e Centro, segunda a sexta das 8h às 18h. Agende pelo WhatsApp.',
                pre, body, '', full)

# ------------------------------------------------------------ especialidades
def spec_page(s):
    pre = '../'
    others = ''.join(f'<a href="{o["slug"]}.html">{o["name"]} {AR}</a>' for o in SPECS if o is not s)
    signs = ''.join(f'<div class="sign rv" style="--d:{i * 0.05:.2f}s"><i>{i + 1:02d}</i><p>{t}</p></div>' for i, t in enumerate(s['signs']))
    steps = ''.join(f'<li class="rv" style="--d:{i * 0.08:.2f}s"><b>{i + 1:02d}</b><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(s['steps']))
    main = f'''<header class="hero sub-hero" id="topo">
  <div class="hero-bg"><img class="photo-grade" src="{pre}img/{s["img"]}.jpg" alt="" fetchpriority="high"></div>
  <div class="navcard">{nav(pre, False)}</div>
  <div class="hero-copy">
    <a class="back rv" href="{pre}index.html">{AR} Voltar para a página inicial</a>
    <p class="hero-eyebrow rv" style="--d:.05s">Especialidade · OdontoCenter Ipatinga</p>
    <h1><span class="ln"><span style="--d:.15s">{s["h1"].replace(" em Ipatinga", "")}</span></span><span class="ln"><span style="--d:.27s">em <span class="it">Ipatinga</span></span></span></h1>
    <p class="sub rv" style="--d:.45s">{s["sub"]}</p>
    <div class="row rv" style="--d:.58s"><a class="btn btn-e" href="#agendar">Agendar avaliação {AR}</a><a class="btn btn-o" href="#como-funciona">Como funciona</a></div>
  </div>
</header>

<section class="sec" aria-labelledby="h-about"><div class="wrap"><div class="about">
  <div><span class="eyebrow rv">{s["name"]}</span><h2 class="rv" id="h-about" style="--d:.08s">{s["about_t"]}</h2>{"".join(f'<p class="rv" style="--d:.16s">{p}</p>' for p in s["about"])}
    <div class="row rv" style="margin-top:32px;--d:.22s"><a class="btn btn-e" href="#agendar">Agendar avaliação {AR}</a></div></div>
  <div class="ph rv-img"><img class="photo-grade" data-par src="{pre}img/{s["img"]}.jpg" alt="" loading="lazy"></div>
</div></div></section>

<section class="panel light" aria-labelledby="h-signs">
  <div class="panel-head"><div><span class="eyebrow rv">Quando procurar</span><h2 class="rv" id="h-signs" style="--d:.08s;margin-top:20px">Sinais de que é hora de <span class="it">agendar</span></h2></div><p class="intro rv" style="--d:.16s">Se você se identificou com algum destes sinais, uma avaliação ajuda a entender o seu caso e as opções de tratamento.</p></div>
  <div class="signs">{signs}</div>
</section>

<section class="sec" id="como-funciona" aria-labelledby="h-steps"><div class="wrap">
  <div class="sec-head"><span class="eyebrow rv">Como funciona</span><h2 class="rv" id="h-steps" style="--d:.08s">O tratamento, <span class="it">etapa por etapa</span></h2><p class="rv" style="--d:.16s">O dentista explica cada etapa antes de começar, junto com as formas de pagamento e a cobertura do seu convênio.</p></div>
  <ol class="journey journey-wrap" style="--n:{len(s["steps"])}">{steps}</ol>
</div></section>

<section class="sec" style="padding-top:0" aria-labelledby="h-fq"><div class="wrap"><div class="faqs">
  <div><span class="eyebrow rv">Dúvidas</span><h2 class="rv" id="h-fq" style="--d:.08s">Perguntas sobre <span class="it">{s["lower"]}</span></h2><p class="intro rv" style="--d:.16s">A avaliação responde às dúvidas específicas do seu caso.</p></div>
  <div class="rv" style="--d:.1s">{faq_html(s["faq"])}</div>
</div></div></section>

{cta(s)}

<section class="sec" aria-labelledby="h-oth"><div class="wrap">
  <div class="sec-head"><span class="eyebrow rv">Outras especialidades</span><h2 class="rv" id="h-oth" style="--d:.08s;font-size:clamp(30px,3.4vw,48px)">Cuidado completo em um só <span class="it">lugar</span></h2></div>
  <div class="others rv">{others}</div>
</div></section>'''
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE_URL + "/"},
        {"@type": "ListItem", "position": 2, "name": s['name'], "item": f"{SITE_URL}/especialidades/{s['slug']}"}]}
    ld = [ld_faq(s['faq']), crumbs] + ld_units()
    body = shell(pre, False, main) + f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    return page(f'{s["h1"]} | OdontoCenter', f'{s["sub"]} Unidades Canaã e Centro, {HOURS.lower()}. Agende pelo WhatsApp.', pre, body, f'especialidades/{s["slug"]}.html', og=f'og-{s["slug"]}.jpg', og_alt=f'{s["h1"]} na OdontoCenter')

# ------------------------------------------------------------ política de privacidade
def privacy():
    pre = ''
    main = f'''<header class="doc-hero" id="topo"><div class="navcard" style="position:absolute;left:50%;top:14px;transform:translateX(-50%);width:min(1180px,calc(100% - 28px));z-index:4">{nav(pre, False)}</div>
  <div class="wrap"><a class="back" href="index.html">{AR} Voltar para a página inicial</a><br><span class="eyebrow">LGPD</span><h1>Política de privacidade e <span class="it">cookies</span></h1><p>Última atualização: novembro de 2026 · versão proposta, a validar com o jurídico da clínica.</p></div></header>
<section class="doc-body light"><div class="prose">
<p>Esta política explica como a OdontoCenter (Centro Odontológico Especializado Ltda, CNPJ 04.598.376/0001-09) trata os dados pessoais de quem visita este site, em conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018).</p>
<h2>1. Quais dados coletamos</h2>
<p>Este site não armazena em servidor os dados digitados no formulário de agendamento. Quando você preenche o formulário e toca em "Enviar para o WhatsApp", as informações (unidade, serviço, tipo de atendimento, convênio, nome do paciente e descrição opcional) são montadas no seu próprio navegador e enviadas por você, pelo WhatsApp, para a unidade escolhida.</p>
<p>Na conversa pelo WhatsApp e no atendimento presencial, a clínica pode tratar dados de identificação, contato, convênio e dados de saúde necessários para o atendimento odontológico.</p>
<h2>2. Para que usamos os dados</h2>
<ul><li>Agendar, confirmar, remarcar ou cancelar consultas;</li><li>Prestar o atendimento odontológico e manter o prontuário, como exige a legislação;</li><li>Verificar a cobertura do seu convênio;</li><li>Responder às suas dúvidas.</li></ul>
<h2>3. Base legal</h2>
<p>O tratamento se baseia na execução do atendimento solicitado por você, no cumprimento de obrigações legais e regulatórias (como a guarda do prontuário) e, para dados de saúde, na tutela da saúde, conforme os artigos 7º e 11 da LGPD.</p>
<h2>4. Compartilhamento</h2>
<p>Os dados podem ser compartilhados com o seu convênio, para autorização de procedimentos, e com laboratórios de prótese, quando o tratamento exigir. A conversa pelo WhatsApp também está sujeita à política de privacidade do WhatsApp (Meta).</p>
<h2>5. Cookies e armazenamento no navegador</h2>
<p>Este site usa apenas o armazenamento local do navegador para lembrar a sua escolha no aviso de privacidade. Não usamos cookies de publicidade. Se, no futuro, forem instaladas ferramentas de medição de audiência (como o Google Analytics), elas só serão ativadas com o seu consentimento e esta política será atualizada.</p>
<h2>6. Seus direitos</h2>
<p>Você pode solicitar a confirmação do tratamento, o acesso, a correção, a portabilidade ou a eliminação dos seus dados, além de revogar consentimentos, nos limites da lei. Dados do prontuário são mantidos pelo prazo legal.</p>
<h2>7. Contato</h2>
<p>Para exercer seus direitos ou tirar dúvidas, fale com a clínica pelo WhatsApp da unidade Canaã, {U["canaa"]["fone"]}, ou da unidade Centro, {U["centro"]["fone"]}, {HOURS.lower()}. Encarregado de dados (DPO): <em>[a definir pela clínica]</em>.</p>
</div></section>'''
    body = shell(pre, False, main).replace('href="#agendar"', 'href="index.html#agendar"')
    return page('Política de privacidade e cookies | OdontoCenter', 'Como a OdontoCenter trata os dados pessoais de quem visita o site e agenda pelo WhatsApp, conforme a LGPD.', pre, body, 'politica-de-privacidade.html', og='og-privacidade.jpg', og_alt='Política de privacidade da OdontoCenter')

if __name__ == '__main__':
    open('index.html', 'w').write(home('', True))
    open('artifact.html', 'w').write(home('', False))
    for s in SPECS:
        open(f'especialidades/{s["slug"]}.html', 'w').write(spec_page(s))
    open('politica-de-privacidade.html', 'w').write(privacy())
    urls = [''] + [f'especialidades/{s["slug"]}' for s in SPECS] + ['politica-de-privacidade']
    open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE_URL}/{u}</loc><changefreq>monthly</changefreq><priority>{"1.0" if not u else "0.8"}</priority></url>\n' for u in urls) + '</urlset>\n')
    open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    print('ok', len(SPECS), 'especialidades')
