# Search record: candidate soprano descants for exposition entry 4 (bars 13-17); "h" was adopted in build_sk.py.
import fl
base = fl.read('SK_final.ly')
cands = {
 'g': ("f''2. r4 | r4 c''2 des''4 | c''2 r2 | r4 des''2 f''4 | e''2. d''4", "c''2 bes'2"),
 'h': ("f''2. r4 | r4 c''2 des''4 | c''2 r2 | r4 des''2 f''4 | e''2. d''4", "c''1"),
 'i': ("f''2. r4 | r4 c''2 des''4 | c''2 r4 g''4~ | g''4 des''2 f''4 | e''2. d''4", "c''2 bes'2"),
 'j': ("f''2. r4 | r4 c''2 des''4 | c''2 r4 ees''4 | des''2. f''4 | e''2. d''4", "c''2 bes'2"),
}
first = base['soprano'][:12]
for k, (d, a17) in cands.items():
    sc = {v: list(base[v]) for v in fl.VOICES}; sc['soprano'] = first + [b.strip() for b in d.split('|')]
    sc['alto'][16] = a17
    fl.write(f'/tmp/ds_{k}.ly', sc)
    lines, sl = fl.check(f'/tmp/ds_{k}.ly', bars='12-17')
    bad = [l for l in lines if l.split()[0] in ('PAR!','BEAT','DIS!','D4?','DIR','MEL','CROS')]
    print(k, lines[-1].split(';')[-1], '|', sl[-1]); [print('   ', b) for b in bad]
    [print('   ', s) for s in sl[:-1] if not s.startswith('ACC ')]
