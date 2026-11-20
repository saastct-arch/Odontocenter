import json,re,base64,sys
p=json.load(open('parts.json'))
TOOTH=p['tooth_sym']
t=open('template.html').read()
tooth=f'<svg class="tooth" viewBox="12 2 76 96" aria-hidden="true"><path d="{TOOTH}"/></svg>'
wa=p['wa']
wa_big=wa.replace('width="22" height="22"','width="34" height="34"')
arrow='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ring='<svg viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="95" fill="none" stroke="#D2E6F5" stroke-width="7"/></svg>'
# avatars
people=[('Dra. Helena Marques','Ortodontia','Canaã','seg, qua e sex','Canaã','Ortodontia (aparelho)','#E9BE98','#2A1A11','f'),
('Dr. Rafael Moreira','Implantes e cirurgias','Centro','ter e qui','Centro','Implantes dentários','#B97A4B','#1C1411','m'),
('Dra. Camila Torres','Estética, dentística e prótese','Canaã','seg a qui','Canaã','Clareamento e estética','#7A4A2E','#120D0B','f'),
('Dr. Lucas Ferreira','Endodontia e periodontia','Centro','seg, qua e sex','Centro','Endodontia (canal)','#D9A67A','#5A3720','m')]
def avatar(s,h,k):
    cx,cy=150,150;top=cy+52
    back=f'<path d="M{cx-44},{cy+6} C{cx-50},{cy-52} {cx+50},{cy-52} {cx+44},{cy+6} L{cx+48},{cy+86} L{cx-48},{cy+86}Z" fill="{h}"/>' if k=='f' else ''
    hair=f'<path d="M{cx-40},{cy-6} C{cx-44},{cy-50} {cx+44},{cy-50} {cx+40},{cy-6} C{cx+30},{cy-26} {cx-30},{cy-26} {cx-40},{cy-6}Z" fill="{h}"/>'
    return f'''<svg viewBox="0 0 300 340" role="img" aria-label="Ilustração de dentista (imagem fictícia)"><rect width="300" height="340" fill="#E6F2FB"/><g fill="#2FA4D8" opacity=".25"><g transform="translate(20 20) rotate(-28) scale(.7)"><path d="{TOOTH}"/></g><g transform="translate(240 30) rotate(30) scale(.5)"><path d="{TOOTH}"/></g></g>{back}<path d="M{cx-92},340 L{cx-92},{top+60} Q{cx-92},{top+6} {cx-34},{top-2} L{cx+34},{top-2} Q{cx+92},{top+6} {cx+92},{top+60} L{cx+92},340Z" fill="#fff"/><path d="M{cx-26},{top-2} L{cx},{top+52} L{cx+26},{top-2}Z" fill="#2FA4D8"/><rect x="{cx-14}" y="{cy+28}" width="28" height="{top-cy-24}" rx="10" fill="{s}"/><circle cx="{cx}" cy="{cy}" r="40" fill="{s}"/>{hair}<circle cx="{cx-14}" cy="{cy+2}" r="3.2" fill="#1b1b1b"/><circle cx="{cx+14}" cy="{cy+2}" r="3.2" fill="#1b1b1b"/><path d="M{cx-14},{cy+16} Q{cx},{cy+30} {cx+14},{cy+16}" fill="#fff" stroke="#7a3b2e" stroke-width="2.2" stroke-linejoin="round"/></svg>'''
tabs='';tcards=''
for i,(n,e,u,d,un,sv,s,h,k) in enumerate(people):
    sel='true' if i==0 else 'false'
    tabs+=f'<button class="tab" role="tab" id="tab{i}" aria-selected="{sel}" aria-controls="tc{i}" tabindex="{0 if i==0 else -1}" type="button">{n}</button>'
    tcards+=f'<div class="tcard" role="tabpanel" id="tc{i}" aria-labelledby="tab{i}"{"" if i==0 else " hidden"}><div class="av">{avatar(s,h,k)}</div><div><p class="meta">{e}</p><h3>{n}</h3><dl><dt>CRO</dt><dd>CRO-MG 00000 <em>(fictício)</em></dd><dt>Unidade</dt><dd>{u}</dd><dt>Dias</dt><dd>{d}</dd></dl><a class="btn btn-b" href="#agendar" data-unit="{un}" data-service="{sv}">Agendar com {n.split()[0]} {n.split()[1]}</a></div></div>'
faq_html=p['faq_html']
mode=sys.argv[1]
def img(m):
    n=m.group(1)
    if mode=='repo': return f'img/{n}.jpg'
    return 'data:image/jpeg;base64,'+base64.b64encode(open(f'img/{n}.jpg','rb').read()).decode()
t=re.sub(r'\{\{img:(\w+)\}\}',img,t)
rep=dict(logo_nav=p['logo_nav'],logo_foot=p['logo_foot'].replace('logo foot','foot'),tooth=tooth,wa=wa,wa_big=wa_big,arrow=arrow,ring=ring,tabs=tabs,tcards=tcards,faq_html=faq_html,svc_opts=p['svc_opts'],conv_opts=p['conv_opts'],ld=p['ld'])
for k,v in rep.items(): t=t.replace('{{'+k+'}}',v)
assert '{{' not in t,[l[:80] for l in t.split('\n') if '{{' in l][:3]
if mode=='artifact':
    open('artifact.html','w').write(t)
else:
    t2=t.replace('<title>OdontoCenter Ipatinga</title>','<title>Dentista em Ipatinga | OdontoCenter, desde 2001</title>',1).replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
    i=t2.index('<link rel="stylesheet"')
    head='<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="description" content="Clínica odontológica em Ipatinga há 25 anos: ortodontia, implantes, estética e mais. Duas unidades, Canaã e Centro. Agende pelo WhatsApp.">\n'
    j=t2.index('<title>'); title=t2[j:t2.index('</title>')+8]
    body=t2.replace(title+'\n','',1)
    open('index.html','w').write(head+title+'\n'+body.split('<a class="skip"')[0]+'<style>html,body{margin:0}:root{color-scheme:light}</style>\n</head>\n<body>\n<a class="skip"'+body.split('<a class="skip"',1)[1]+'\n</body>\n</html>\n')
print(mode,len(t))
