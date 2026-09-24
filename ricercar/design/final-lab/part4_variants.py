# Search record: Part IV enrichment variants, checked on bars 41-50 (x1 adopted in build_sk.py).
# Bars 41-50 of the proposal-2 skeleton equal those of SK_final before the patch.
import sys; sys.path.insert(0, '.')
import fl
sk = fl.read('../proposal-2/lab/L11_full_skeleton.ly')
cands = {
 'x1': dict(tenor={42:"bes2 a2", 43:"aes2 g4 ges4"}, soprano={44:"f''2. f''8 ges''8", 45:"f''1", 46:"f''1~"}),
 'x2': dict(tenor={42:"bes2 a2", 43:"aes2 g4 ges4"}, soprano={}),
 'x3': dict(tenor={}, soprano={44:"f''2. f''8 ges''8", 45:"f''1", 46:"f''1~"}),
 'x4': dict(tenor={42:"bes2 a2", 43:"aes2 g2"}, soprano={44:"f''2. f''8 ges''8", 45:"f''1", 46:"f''1~"}),
}
for k, ch in cands.items():
    sc = {v: list(sk[v]) for v in fl.VOICES}
    for v, d in ch.items():
        for b, s in d.items(): sc[v][b-1] = s
    fl.write(f'/tmp/p4_{k}.ly', sc)
    lines, sl = fl.check(f'/tmp/p4_{k}.ly', bars='41-50')
    bad = [l for l in lines if l.split()[0] in ('PAR!','BEAT','DIS!','D4?','DIR','MEL','CROS')]
    print(k, lines[-1].split(';')[-1], '|', sl[-1]); [print('   ', b) for b in bad]
    [print('   ', s) for s in sl[:-1] if not s.startswith('ACC ')]
