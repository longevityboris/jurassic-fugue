"""The whole ricercar skeleton, section by section: the single source of SK_final.ly and plan.json.

Every position inside a section (roles, keep items, tempo, dynamics, fermatas, breaths, pedal) is
section-relative "bar:beat" (bar 1 = the section's first bar); build_sk.py converts to absolute bars.
Voices: one 4/4 bar per "|", \\absolute LilyPond (notes, rests, ties).
roles: (voice, at, until, role[, landing_from]); role = subject | answer | cf | cs | free.
keep: (voice, at, until, what): free notes the blueprint requires composers to keep (splice_check).
"""

SECTIONS = [
    dict(id='sec01_expo', title='Exposition, entries 1-3', bars=12,
         soprano='''bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'8 |
            c''4. a'8 f'4 c''4 | aes''2. g''4 | f''4 e''4 ees''2 | des''2. c''4 |
            e''4. g''8 c''4 r4 | bes'8 a'8 bes'8 c''8 des''8 c''8 ees''8 ges'8 | des''4 c''8 f''8~ f''2 | ees''8 f''8 ees''8 des''8 ces''4 des''4''',
         alto='''r1 | r1 | r1 | r1 |
            f'2. f'8 e'8 | f'2. f'8 e'8 | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f'8 |
            g'4. e'8 c'4 f4 | des'2. c'4 | bes4 a4 aes2 | ges2. f4''',
         tenor='''r1 | r1 | r1 | r1 |
            r1 | r1 | r1 | r1 |
            r1 | r1 | r1 | r1''',
         bass='''r1 | r1 | r1 | r1 |
            r1 | r1 | r1 | r1 |
            bes,2. bes,8 a,8 | bes,2. bes,8 a,8 | bes,4. c8 c4. ees8 | ees2. des8 bes,8''',
         roles=[('soprano', '1:1', '5:4', 'subject'),
                ('alto', '5:1', '9:4', 'answer'),
                ('soprano', '5:4', '9:4', 'cs'),
                ('bass', '9:1', '13:4', 'subject'),
                ('alto', '9:4', '13:4', 'cs'),
                ('soprano', '10:1', '13:1', 'cs')],
         tempo=[{'at': '1:1', 'bpm': 74}],
         dynamics=[{'at': '1:1', 'level': 'p'}, {'at': '5:1', 'until': '13:1', 'to': 'mp'}],
         fermatas=[],
         breaths=[],
         pedal=[],
    ),
    dict(id='sec02_entry4_episode', title='Exposition entry 4 and Episode 1', bars=7,
         soprano='''f''2. r4 | r4 c''2 des''4 | c''2 r2 | r4 des''2 f''4 |
            e''2. d''4 | c''4. des''8 des''4. f''8 | ges''4. f''8 f''4. ees''8''',
         alto='''a4. c'8 a4 r4 | f'8 e'8 f'8 g'8 aes'8 g'8 bes'8 des'8 | aes'4 g'8 c''8~ c''2 | bes'8 c''8 bes'8 aes'8 ges'4 aes'4 |
            c''1 | aes'2 bes'2 | bes'2 a'2''',
         tenor='''f2. f8 e8 | f2. f8 e8 | f4. g8 g4. bes8 | bes2. aes8 f8 |
            g4. e8 c4 e4 | f2 des'2 | ees'2 c'2''',
         bass='''c4. a,8 f,4 c,4 | aes,2. g,4 | f,4 e,4 ees,2 | des,2. c,4 |
            e,4. g,8 c,4 c4 | f,2 bes,2 | ees,2 f,2''',
         roles=[('tenor', '1:1', '5:4', 'answer'),
                ('bass', '1:4', '5:4', 'cs'),
                ('alto', '2:1', '5:1', 'cs')],
         tempo=[],
         dynamics=[{'at': '1:1', 'until': '5:3', 'to': 'mf'}, {'at': '6:1', 'level': 'mp'}],
         fermatas=[],
         breaths=[],
         pedal=[],
    ),
    dict(id='sec03_stretto_liquidation', title='Stretto, liquidation, Climax I', bars=10,
         soprano='''des''4 r2. | r1 | ees''2. ees''8 d''8 | ees''2. ees''8 d''8 |
            ees''4. f''8 f''4. aes''8 | aes''2. ges''8 ees''8 | f''4. des''8 bes'4 r4 | r1 |
            des''2. des''8 c''8 | c''1''',
         alto='''f'1 | des''2. c''4 | bes'4 a'4 aes'2 | ges'2. f'4 |
            aes'4. c''8 f'4 f'4 | f'2 bes'2 | bes'2 g'2 ~ | g'2 bes'2 ~ |
            bes'4 bes'8 a'8 ~ a'2 ~ | a'1''',
         tenor='''bes4 r2. | bes8 a8 bes8 c'8 des'8 c'8 ees'8 ges8 | des'4 c'8 f'8 ~ f'2 | ees'8 f'8 ees'8 des'8 ces'4 aes4 |
            ees'2 aes2 | aes2 bes2 | bes1 | g2. g8 ges8 |
            ges1 ~ | ges1''',
         bass='''bes,2. bes,8 a,8 | bes,2. bes,8 a,8 | bes,4. c8 c4. ees8 | ees2. des8 bes,8 |
            c4. aes,8 f,4 ees,4 | des,2. c,4 | f,2 e,2 ~ | e,4 e,8 ees,8 ~ ees,2 ~ |
            ees,1 ~ | ees,1''',
         roles=[('bass', '1:1', '5:4', 'subject'),
                ('alto', '1:4', '5:4', 'cs'),
                ('tenor', '2:1', '4:4', 'cs'),
                ('soprano', '3:1', '7:4', 'subject'),
                ('bass', '7:3', '10:1', 'subject'),
                ('tenor', '8:1', '10:1', 'subject'),
                ('alto', '8:3', '10:1', 'subject'),
                ('soprano', '9:1', '10:1', 'subject')],
         tempo=[{'at': '9:1', 'until': '10:1', 'to_bpm': 66}],
         dynamics=[{'at': '1:1', 'until': '7:1', 'to': 'f'}, {'at': '7:3', 'until': '9:4', 'to': 'ff'}, {'at': '10:1', 'level': 'ff'}],
         fermatas=[{'at': '10:1', 'extra_beats': 3}],
         breaths=[],
         pedal=[],
    ),
    dict(id='sec04_arioso', title='Arioso dolente and the German-sixth pivot', bars=5,
         soprano='''c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1 |
            c''2 b'2''',
         alto='''c'8 c'8 c'8 c'8 c'8 c'8 des'8 des'8 | ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 f'8 f'8 | ges'8 ges'8 ges'8 ges'8 ees'8 ees'8 ees'8 ees'8 | ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 |
            e'8 e'8 e'8 e'8 e'8 e'8 e'8 e'8''',
         tenor='''f8 f8 f8 f8 a8 a8 bes8 bes8 | ges8 ges8 ges8 ges8 ges8 ges8 f8 f8 | bes8 bes8 bes8 bes8 a8 a8 a8 a8 | a8 a8 a8 a8 a8 a8 a8 a8 |
            gis8 gis8 gis8 gis8 gis8 gis8 gis8 gis8''',
         bass='''f,1 | ees,2. d,4 | ges,2 f,2 | f,1 |
            e,1''',
         roles=[('soprano', '1:1', '6:1', 'subject')],
         tempo=[{'at': '1:1', 'bpm': 52}],
         dynamics=[{'at': '1:1', 'level': 'pp'}, {'at': '2:1', 'until': '3:1', 'to': 'p'}, {'at': '3:1', 'until': '5:1', 'to': 'pp'}],
         fermatas=[],
         breaths=[{'at': '1:1', 'ms': 1400}],
         pedal=[{'at': '1:1', 'until': '6:1', 'every': 'harmony'}],
    ),
    dict(id='sec05_inversa', title='Fuga inversa: three entries, A minor established, deceptive link to F', bars=11,
         soprano='''r1 | e''8 f''8 e''8 d''8 c''8 d''8 b'8 g''8 | c''4 d''8 a'8 ~ a'4 b'4 | b'8 a'8 b'8 c''8 d''4 c''4 |
            f''2 e''4 d''4 | dis''2. r4 | e''2. e''8 f''8 | e''2. e''8 f''8 |
            e''4. d''8 d''4. b'8 | b'2. c''8 e''8 | d''4. f''8 a''4 r4''',
         alto='''r2. a'4 | c'2. d'4 | e'4 f'4 fis'2 | gis'2. a'4 |
            f'4. d'8 c'4 b4 | fis'2. e'4 | c''4 a'4 gis'4 r4 | e'8 f'8 e'8 d'8 c'8 d'8 b8 g'8 |
            c'4 d'8 a8 ~ a4 b4 | b8 a8 b8 c'8 d'4 c'4 | a'4. f'8 e'4 gis'4''',
         tenor='''r1 | r1 | b2. b8 c'8 | b2. b8 c'8 |
            b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4 r4 | r1 |
            r1 | r1 | a4. a8 c'4 b4''',
         bass='''e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 |
            d4. f8 a,4 b,4 | b,2. e4 ~ | e2. a,4 | c2. d4 |
            e4 f4 fis2 | gis2. a4 | f4. d8 a,4 e,4''',
         roles=[('bass', '1:1', '5:4', 'subject'),
                ('alto', '1:4', '5:4', 'cs', '5:3'),
                ('soprano', '2:1', '5:1', 'cs'),
                ('tenor', '3:1', '7:4', 'answer'),
                ('soprano', '7:1', '11:4', 'subject'),
                ('bass', '7:4', '11:1', 'cs'),
                ('alto', '8:1', '11:1', 'cs', '10:4')],
         tempo=[{'at': '1:1', 'bpm': 60}, {'at': '1:1', 'until': '12:1', 'to_bpm': 76}],
         dynamics=[{'at': '1:1', 'level': 'pp'}, {'at': '1:1', 'until': '11:3', 'to': 'mf'}],
         fermatas=[],
         breaths=[{'at': '1:1', 'ms': 300}],
         pedal=[],
    ),
    dict(id='sec06_pedal_climax', title='Dominant pedal, combination, Climax II, plagal turn', bars=9,
         soprano='''r1 | r1 | f''2. f''8 ges''8 | f''1 |
            f''1~ | f''2. ges''4 ~ | ges''2 g''2 | bes''2 bes''4 a''4 |
            bes''1''',
         alto='''c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1 |
            des''2 c''2 | a'2 c''4 ees''4 | ees''2 e''2 | e''2. c''4 |
            ees'2. ees'4''',
         tenor='''bes2 a2 | aes2 g4 ges4 | bes2. bes8 a8 | bes2. bes8 a8 |
            bes4. c'8 c'4. ees'8 | ees'2. des'8 bes8 | c'4. a8 bes2 ~ | bes2. c'4 |
            g2. ges4''',
         bass='''f,1 | f,2 f,4 ges,4 | f,1 | f,2 f,4 ges,4 |
            f,2. ees,4 | ees,2. c,4 | c,1 | c,2 des,4 f,4 |
            ees,2. ges,4''',
         roles=[('bass', '1:1', '10:1', 'cf'),
                ('alto', '1:1', '5:1', 'subject'),
                ('tenor', '3:1', '7:4', 'subject'),
                ('soprano', '3:1', '4:1', 'answer')],
         tempo=[{'at': '1:1', 'bpm': 76}, {'at': '8:1', 'until': '9:1', 'to_bpm': 68}, {'at': '9:1', 'bpm': 56}],
         dynamics=[{'at': '1:1', 'level': 'p'}, {'at': '3:1', 'until': '5:1', 'to': 'mp'}, {'at': '5:1', 'until': '7:1', 'to': 'f'}, {'at': '7:1', 'until': '8:4', 'to': 'fff'}, {'at': '9:1', 'level': 'pp'}],
         fermatas=[{'at': '8:4', 'extra_beats': 3}],
         breaths=[{'at': '1:1', 'ms': 250}, {'at': '9:1', 'ms': 700}],
         pedal=[],
    ),
    dict(id='sec07_apotheosis_coda', title='Apotheosis (cantus firmus) and coda', bars=12,
         soprano='''bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes'8 |
            c''4. a'8 f'4 d''8 bes'8 | c''2. f''8 bes'8 | ees''4. d''8 d''4. c''8 | c''1 |
            d''1~ | d''1 | d''2 c''2 | d''1''',
         alto='''d'4. ees'8 f'4 ees'4 | d'4 f'4 ees'4 f'8 ees'8 | f'4. ees'8 ees'4. f'8 | a'2 g'4 f'4~ |
            f'4 e'4 d'4 e'4~ | e'4 ees'4 f'2 | c''2. bes'4~ | bes'4 a'4 g'2 |
            f'1 | ges'2 f'2 | f'2 ees'2 | d'2 f'2''',
         tenor='''f2 g4 f4 | bes4 aes4 g4 f4 | f4 d'4 c'4. c'8 | c'2. f4 |
            f2. f8 g8 | f2. f8 g8 | f4. e8 e4. c8 | c2. d8 f8 |
            d'1 | ees'2 d'2 | bes2. bes8 a8 | bes1''',
         bass='''bes,2. bes,8 c8 | bes,2. bes,8 c8 | bes,4. a,8 a,4. f,8 | f,2. d,4 |
            f,2. f,8 e,8 | f,2. f,8 e,8 | f,4. g,8 g,4. bes,8 | bes,2. a,8 f,8 |
            bes,1~ | bes,1 | bes,1~ | bes,1''',
         roles=[('soprano', '1:1', '9:1', 'subject'),
                ('bass', '1:1', '9:1', 'cs'),
                ('tenor', '5:1', '9:1', 'cs'),
                ('tenor', '11:1', '12:4', 'subject')],
         tempo=[{'at': '1:1', 'bpm': 69}, {'at': '9:1', 'until': '12:3', 'to_bpm': 56}],
         dynamics=[{'at': '1:1', 'level': 'p'}, {'at': '1:1', 'until': '5:1', 'to': 'mf'}, {'at': '5:1', 'until': '7:1', 'to': 'f'}, {'at': '7:3', 'until': '9:1', 'to': 'mp'}, {'at': '9:1', 'until': '12:3', 'to': 'pp'}],
         fermatas=[{'at': '12:3', 'extra_beats': 3}],
         breaths=[{'at': '1:1', 'ms': 400}],
         pedal=[{'at': '1:1', 'until': '12:4', 'every': 'harmony'}],
    ),
]

GLOBAL = {'voices': ['soprano', 'alto', 'tenor', 'bass'], 'measure': '1', 'humanize': {'ms': 6, 'vel': 2}, 'role_boost': {'subject': 9, 'answer': 9, 'cf': 7, 'cs': 2, 'free': -4}, 'role_level': {'subject': 0.7, 'answer': 0.7, 'cf': 0.5, 'cs': 0.2, 'free': -0.2}}
