import json,re,base64,sys
p=json.load(open('parts.json'))
t=open('template.html').read()
mode=sys.argv[1]
def src(n):
    return f'img/{n}.jpg' if mode=='repo' else 'data:image/jpeg;base64,'+base64.b64encode(open(f'img/{n}.jpg','rb').read()).decode()
wa=p['wa']
ar='<svg class="ar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
navinner=f'<a href="#topo" aria-label="OdontoCenter, ir ao início">{p["logo_nav"]}</a><nav aria-label="Principal"><a href="#especialidades">Especialidades</a><a href="#unidades">Unidades</a><a href="#convenios">Convênios</a><a href="#equipe">Equipe</a><a href="#duvidas">Dúvidas</a></nav><div class="end"><a class="tel btn btn-ob" href="tel:+553138277739">(31) 3827-7739</a><a class="btn btn-b" href="#agendar">Agendar avaliação</a></div>'
conv=[('LumarMetals',''),('AAPI',''),('Novo Oriente','plano de assistência familiar'),('Cenibra',''),('Postal Saúde','Correios'),('COPASS Saúde',''),('Rede UNNA','Bradesco · Unimed · OdontoPrev')]
logos=''.join(f'<div>{n}{f"<small>{s}</small>" if s else ""}</div>' for n,s in conv)
people=[('Dra. Helena Marques','Ortodontia','Canaã','seg, qua e sex','canaa','Ortodontia (aparelho)','d1'),
('Dr. Rafael Moreira','Implantes e cirurgias','Centro','ter e qui','centro','Implantes dentários','d2'),
('Dra. Camila Torres','Estética, dentística e prótese','Canaã','seg a qui','canaa','Clareamento e estética','d3'),
('Dr. Lucas Ferreira','Endodontia e periodontia','Centro','seg, qua e sex','centro','Endodontia (canal)','d4')]
tabs='';tcards=''
for i,(n,e,u,d,uk,sv,im) in enumerate(people):
    tabs+=f'<button class="tab" role="tab" id="tab{i}" aria-selected="{"true" if i==0 else "false"}" aria-controls="tc{i}" tabindex="{0 if i==0 else -1}" type="button">{n}</button>'
    tcards+=f'<div class="tcard" role="tabpanel" id="tc{i}" aria-labelledby="tab{i}"{"" if i==0 else " hidden"}><div class="av"><img src="{src(im)}" alt="Foto ilustrativa de {n}" loading="lazy"></div><div class="body"><p class="meta">{e}</p><h3>{n}</h3><dl><dt>Registro</dt><dd>CRO-MG 00000 <em>(fictício)</em></dd><dt>Unidade</dt><dd>{u}</dd><dt>Atendimento</dt><dd>{d}</dd></dl><a class="btn btn-b" href="#agendar" data-unit="{uk}" data-service="{sv}">Agendar com {n.split()[0]} {n.split()[1]} {ar}</a></div></div>'
t=re.sub(r'\{\{img:(\w+)\}\}',lambda m:src(m.group(1)),t)
rep=dict(navinner=navinner,ar=ar,logos=logos,logos_dup=logos.replace('<div>','<div aria-hidden="true">'),tabs=tabs,tcards=tcards,wa=wa,logo_foot=p['logo_foot'].replace('class="logo foot"','class="foot"'),faq_html=p['faq_html'],svc_opts=p['svc_opts'],conv_opts=p['conv_opts'],ld=p['ld'])
for k,v in rep.items(): t=t.replace('{{'+k+'}}',v)
assert '{{' not in t,[l[:80] for l in t.split('\n') if '{{' in l][:3]
if mode=='artifact':
    open('artifact.html','w').write(t)
else:
    title='<title>Dentista em Ipatinga | OdontoCenter, desde 2001</title>'
    t=t.replace('<title>OdontoCenter Ipatinga</title>\n','').replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
    head,body=t.split('<a class="skip"',1)
    open('index.html','w').write('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="description" content="Clínica odontológica em Ipatinga há 25 anos: ortodontia, implantes, estética e mais. Duas unidades, Canaã e Centro. Agende pelo WhatsApp.">\n'+title+'\n'+head+'<style>html,body{margin:0}:root{color-scheme:dark}</style>\n</head>\n<body>\n<a class="skip"'+body+'\n</body>\n</html>\n')
print(mode,len(t)//1024,'KB')
