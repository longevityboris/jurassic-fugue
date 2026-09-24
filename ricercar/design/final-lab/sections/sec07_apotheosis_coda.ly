\version "2.24.0"
% bars 51-62
% Section 7: Apotheosis (cantus firmus) and coda. Starter = the verified skeleton; enrich per BLUEPRINT.md
% and verify with: python3 ../splice_check.py sec07_apotheosis_coda.ly
soprano = \absolute {
  % 51
  bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes'8 |
  % 55
  c''4. a'8 f'4 d''8 bes'8 | c''2. f''8 bes'8 | ees''4. d''8 d''4. c''8 | c''1 |
  % 59
  d''1~ | d''1 | d''2 c''2 | d''1 |
}
alto = \absolute {
  % 51
  d'4. ees'8 f'4 ees'4 | d'4 f'4 ees'4 f'8 ees'8 | f'4. ees'8 ees'4. f'8 | a'2 g'4 f'4~ |
  % 55
  f'4 e'4 d'4 e'4~ | e'4 ees'4 f'2 | c''2. bes'4~ | bes'4 a'4 g'2 |
  % 59
  f'1 | ges'2 f'2 | f'2 ees'2 | d'2 f'2 |
}
tenor = \absolute {
  % 51
  f2 g4 f4 | bes4 aes4 g4 f4 | f4 d'4 c'4. c'8 | c'2. f4 |
  % 55
  f2. f8 g8 | f2. f8 g8 | f4. e8 e4. c8 | c2. d8 f8 |
  % 59
  d'1 | ees'2 d'2 | bes2. bes8 a8 | bes1 |
}
bass = \absolute {
  % 51
  bes,2. bes,8 c8 | bes,2. bes,8 c8 | bes,4. a,8 a,4. f,8 | f,2. d,4 |
  % 55
  f,2. f,8 e,8 | f,2. f,8 e,8 | f,4. g,8 g,4. bes,8 | bes,2. a,8 f,8 |
  % 59
  bes,1~ | bes,1 | bes,1~ | bes,1 |
}
