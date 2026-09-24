\version "2.24.0"

\header {
  title = "Fugue on a Theme from Jurassic Park"
  subtitle = "for organ, in B-flat major"
  composer = "after John Williams (1993)"
  tagline = ##f
}

global = {
  \key bes \major
  \time 4/4
}

%% SOPRANO (upper manual, stems up)
soprano = \absolute {
  % 1-2
  R1*2 |
  % 3-4 answer (F)
  f''4. f''16 e'' f''4. f''16 e'' |
  f''8. g''16 g''8. bes''16 bes''4. a''16 f'' |
  % 5 link (theme bar 7 cell, diminished)
  f''8. ees''16 ees''8. d''16 d''8. c''16 c''8. bes'16 |
  % 6-7 countersubject (B-flat version, above tenor subject)
  r8 d'' g'' f''16 ees'' d''8 bes' c''4 |
  d''4 ees'' f''8 ees''16 d'' c''8 bes'16 d'' |
  % 8-9 free
  f''4 f''8 e''16 d'' c''8 a' bes'8. c''16 |
  c''8 d'' bes'4 g'4. c''8 |
  R1*28 |
}

%% ALTO (upper manual, stems down)
alto = \absolute {
  % 1-2 subject (B-flat)
  bes'4. bes'16 a' bes'4. bes'16 a' |
  bes'8. c''16 c''8. ees''16 ees''4. d''16 bes' |
  % 3-4 countersubject (F version, below answer)
  r8 a' d'' c''16 bes' a'8 f' g'4 |
  a'4 bes' c''8 bes'16 a' g'8 f'16 a' |
  % 5 link
  a'4 c''8 a' f' g' ees'4 |
  % 6-7 free
  d'8 f' g'4 f'4 g'8. f'16 |
  bes'4 g' a'4. f'8 |
  % 8-9 free
  a'2 f'4 d'8. c'16 |
  f'4 d' e'4. f'8 |
  R1*28 |
}

%% TENOR (lower manual)
tenor = \absolute {
  R1*5 |
  % 6-7 subject (B-flat)
  bes4. bes16 a bes4. bes16 a |
  bes8. c'16 c'8. ees'16 ees'4. d'16 bes |
  % 8-9 countersubject (F version, above pedal answer)
  r8 a d' c'16 bes a8 f g4 |
  a4 bes c'8 bes16 a g8 f16 a |
  R1*28 |
}

%% PEDAL
pedal = \absolute {
  R1*7 |
  % 8-9 answer (F)
  f,4. f,16 e, f,4. f,16 e, |
  f,8. g,16 g,8. bes,16 bes,4. a,16 f, |
  R1*28 |
}

marks = {
  \tempo "Maestoso" 4 = 66
  s1*37
}

tenorClefs = {
  \clef bass
  s1*37
}

\score {
  <<
    \new PianoStaff \with { instrumentName = "Manuals" } <<
      \new Staff = "upper" \with { midiInstrument = "church organ" } <<
        \global \marks
        \new Voice = "soprano" { \voiceOne \soprano }
        \new Voice = "alto" { \voiceTwo \alto }
      >>
      \new Staff = "lower" \with { midiInstrument = "church organ" } <<
        \global \tenorClefs
        \new Voice = "tenor" { \tenor }
      >>
    >>
    \new Staff = "pedal" \with {
      instrumentName = "Pedal"
      midiInstrument = "church organ"
    } <<
      \global \clef bass
      \new Voice = "pedal" { \pedal }
    >>
  >>
  \layout { }
  \midi { }
}
