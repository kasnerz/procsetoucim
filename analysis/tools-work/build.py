import json, csv, re
from collections import Counter, defaultdict, OrderedDict
rows=[r for r in json.load(open('outcomes.json')) if r['sekce']=='okruh']
CAT=OrderedDict([
 ('chat','AI chatbot'),('search','Vyhledávání'),('lang','Překladač a korektor'),
 ('calc','Výpočty a grafy'),('map','Mapy a navigace'),('sense','Měření a určování'),
 ('code','Programování'),('media','Digitální tvorba')])
FINE={'llm':'chat','stt':'chat','search':'search','fact':'search','trans':'lang','spell':'lang','tts':'lang',
 'calc':'calc','solver':'calc','geo':'calc','sheet':'calc','sim':'calc','map':'map','sky':'map',
 'sens':'sense','track':'sense','id':'sense','code':'code','img':'media','media':'media','music':'media','cad':'media','sec':None}
VW={'L':'líp','S':'srovnatelně','N':'zatím ne'}; RANK={'L':3,'S':2,'N':1}
notes={}
for l in open('notes.txt'):
    if not l[0].isupper(): continue
    k,t,u,note=l.rstrip('\n').split(';',3)
    notes[k]=(t,int(u),note)
def short(s,n=110):
    if len(s)<=n: return s
    return s[:n].rsplit(' ',1)[0].rstrip(',;')+'…'
out=[]
for r in rows:
    t,u,note=notes[r['kod']]
    cats={}
    if t!='-':
        for x in t.split(','):
            a,v=x.split('='); c=FINE[a]
            if c is None: continue
            if c not in cats or RANK[v]>RANK[cats[c]]: cats[c]=v
    order=[c for c in CAT if c in cats]
    order.sort(key=lambda c:-RANK[cats[c]])
    out.append(dict(kod=r['kod'],obor=r['obor'],uzel=r['uzel'],zneni=short(r['zneni']),
        badges='|'.join(CAT[c] for c in order) if order else 'žádný nástroj',
        verdicts='|'.join(VW[cats[c]] for c in order),uncertain=u,note=note,_cats=cats))
with open('/home/zdenek/projects/rvp/analysis/tools-coverage.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['kod','obor','uzel','zneni','badges','verdicts','uncertain','note'])
    w.writeheader()
    for o in out: w.writerow({k:v for k,v in o.items() if not k.startswith('_')})
# aggregates
N=len(out)
def best(o): return max([RANK[v] for v in o['_cats'].values()] or [0])
print('N',N)
tot=Counter(best(o) for o in out); print('overall best:',{ {3:'L',2:'S',1:'N',0:'none'}[k]:v for k,v in tot.items()})
print('uncertain',sum(o['uncertain'] for o in out))
print('\nPer subject: n | >=1 líp | best srovn | best zatím ne | žádný | uncertain')
by=defaultdict(list)
for o in out: by[o['obor']].append(o)
subj=[]
for s,l in by.items():
    n=len(l); c=Counter(best(o) for o in l)
    subj.append((c[3]/n,s,n,c[3],c[2],c[1],c[0],sum(o['uncertain'] for o in l)))
for x in sorted(subj,reverse=True): print(f"{x[1]} | {x[2]} | {x[3]} ({x[0]:.0%}) | {x[4]} | {x[5]} | {x[6]} | {x[7]}")
print('\nPer category: outcomes | líp | srovn | zatím ne | only-badge-on-row | subjects')
for c,lab in CAT.items():
    l=[o for o in out if c in o['_cats']]
    cc=Counter(o['_cats'][c] for o in l)
    only=sum(1 for o in l if len(o['_cats'])==1)
    subs=Counter(o['obor'] for o in l).most_common(4)
    print(f"{lab} | {len(l)} | {cc['L']} | {cc['S']} | {cc['N']} | {only} | {subs}")
print('\nBy uzel')
for z in ['ZV5','ZV9']:
    l=[o for o in out if o['uzel']==z]; c=Counter(best(o) for o in l)
    print(z,len(l),'L',c[3],f"{c[3]/len(l):.0%}",'S',c[2],'N',c[1],'none',c[0])
print('\nbadges per row', Counter(len(o['_cats']) for o in out))
json.dump([{k:v for k,v in o.items()} for o in out],open('coverage.json','w'),ensure_ascii=False)
