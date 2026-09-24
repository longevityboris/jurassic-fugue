\version "2.24.0"
% bars 42-50
% Section 6: Dominant pedal, combination, Climax II, plagal turn. Starter = the verified skeleton; enrich per BLUEPRINT.md
% and verify with: python3 ../splice_check.py sec6_pedal_climax.ly
soprano = \absolute {
  % 42
  r1 | r1 | f''2. f''8 ges''8 | f''1 |
  % 46
  f''1~ | f''2. ges''4 ~ | ges''2 g''2 | bes''2 bes''4 a''4 |
  % 50
  bes''1 |
}
alto = \absolute {
  % 42
  c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1 |
  % 46
  des''2 c''2 | a'2 c''4 ees''4 | ees''2 e''2 | e''2. c''4 |
  % 50
  ees'2. ees'4 |
}
tenor = \absolute {
  % 42
  bes2 a2 | aes2 g4 ges4 | bes2. bes8 a8 | bes2. bes8 a8 |
  % 46
  bes4. c'8 c'4. ees'8 | ees'2. des'8 bes8 | c'4. a8 bes2 ~ | bes2. c'4 |
  % 50
  g2. ges4 |
}
bass = \absolute {
  % 42
  f,1 | f,2 f,4 ges,4 | f,1 | f,2 f,4 ges,4 |
  % 46
  f,2. ees,4 | ees,2. c,4 | c,1 | c,2 des,4 f,4 |
  % 50
  ees,2. ges,4 |
}
