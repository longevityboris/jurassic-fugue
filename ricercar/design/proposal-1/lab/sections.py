"""Section drafts of proposal-1 as LilyPond voice strings (\\absolute, 2/2).

python3 sections.py [NAME ...]  -> writes lab/<NAME>.ly for each section draft and
runs tools/check.py (with the fixed ranges) + the strict stile-antico filter.
Bar numbers in comments are GLOBAL bar numbers of the planned piece.
"""
import sys
from ricer import *

SEC = {}

# --------------------------------------------------------------------------
# E1  Exposition, bars 1-18 (+ joint bar 19:1).  B-flat minor -> G7 (V7 of C).
#   1-4  S  S1 (b-flat')                      solo, p
#   5-8  A  A1 real answer (f')    S  CS1 (answer level, elided from S1's c'')
#   9-10 codetta S+A: G - C/E - F - F/C -> b-flat (circle of fifths)
#  11-14 T  S1 (b-flat)            A  CS1         S  CS2 (bes' replaces its rest)
#  15-18 B  A1 (f)                 T  CS1 (ans)   A  CS2 (ans)   S free, enters 16:3
#  19:1  C minor 6/4 over G (B g = I1 begins; T c' tied = IC1 begins, resolves c'-b;
#        A ees' tied; S rests = IC2's opening rest) -> mirror section
SEC['E1_exposition'] = dict(title='E1 exposition bars 1-19', soprano="""
bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' |
c''2 des''2 | d''4. ees''8 f''4. g''8 | f''2. ees''4~ | ees''4 d''4 des''4 c''4 |
b'2 c''2~ | c''4 bes'4 a'2 |
bes'4 f''4 ees''4 des''8 c''8 | bes'4 c''4 des''4 ees''4 | des''4 c''4 ees''4. des''8 | c''2 bes'4. aes'8~ |
aes'4 r4 r2 | r2 c''2~ | c''4 bes'4 ees''2~ | ees''2 des''4 f''4 |
r2
""", alto="""
R1*4 |
f'2. f'8 e' | f'2. f'8 e' | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f' |
g'2 e'2 | f'2 c'2 |
f'2 ges'2 | g'4. aes'8 bes'4. c''8 | bes'2. aes'4~ | aes'4 g'4 ges'4 f'4 |
r4 c''4 bes'4 aes'8 g'8 | f'4 g'4 aes'4 bes'4 | aes'4 g'4 bes'4. aes'8 | g'2 f'4. ees'8~ |
ees'2
""", tenor="""
R1*10 |
bes2. bes8 a | bes2. bes8 a | bes4. c'8 c'4. ees'8 | ees'2. des'8 bes |
c'2 des'2 | d'4. ees'8 f'4. g'8 | f'2. ees'4~ | ees'4 d'4 des'4 c'4~ |
c'2
""", bass="""
R1*14 |
f2. f8 e | f2. f8 e | f4. g8 g4. bes8 | bes2. aes8 f |
g2
""")


def build(name):
    d = SEC[name]
    p = lab(name + '.ly', {v: d[v] for v in ('soprano', 'alto', 'tenor', 'bass') if v in d}, d['title'])
    out = check(p)
    cnt, strong, tot = summary(out)
    st = strict(out)
    print(f"{name}: {tot}  strict={len(st)}")
    for l in out.splitlines():
        if l[:4] in ('PAR!', 'BEAT', 'DIS!', 'D4? ', 'ERR ', 'DIR ', 'CROS', 'MEL '):
            print('   ' + l)
    for l in st:
        print('   strict: ' + l)
    return out


if __name__ == '__main__':
    for n in (sys.argv[1:] or SEC):
        build(n)
