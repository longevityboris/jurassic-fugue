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
  c''8 d'' bes'4 g'4. c''16 ees'' |
  % 10-11 episode 1: circle of fifths (theme bar 5 cell)
  d''8. bes'16 g'8 ees''16 c'' ees''2 ~ |
  ees''4. d''8 ~ d''4 r4 |
  % 12-13 subject in E-flat major
  ees''4. ees''16 d'' ees''4. ees''16 d'' |
  ees''8. f''16 f''8. aes''16 aes''4. g''16 ees'' ~ |
  % 14-15 episode 2: chain of 7-6 suspensions (theme bar 7 rhythm)
  ees''4. d''8 ~ d''4. c''8 ~ |
  c''4. bes'8 ~ bes'4. a'8 |
  % 16-17 countersubject (G minor, above tenor)
  r8 bes' ees'' d''16 c'' bes'8 g' a'4 |
  bes'4 c'' d''8 c''16 bes' a'8 g'16 bes' |
  % 18-19 episode 3, manuals only: theme bars 5-8 (diminished, C minor)
  d''8. b'16 g'8 ees''16 c'' d''4. g''16 c'' |
  f''8. ees''16 ees''8. d''16 d''2 |
  % 20-21 free
  g'4 aes' g'4. f'8 |
  g'4 d'' b'4. c''8 |
  R1*16 |
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
  % 10-11
  d'4 ees'8 f' g'4. f'8 |
  a'4. bes'8 f'8. d'16 bes8 g'16 ees' |
  % 12-13 countersubject (E-flat version)
  r8 g' c'' bes'16 aes' g'8 ees' f'4 |
  g'4 aes' bes'8 aes'16 g' f'8 ees'16 g' |
  % 14-15 (countersubject figure and subject-head neighbour motif)
  c''8 bes'16 a' g'8 f'16 a' g'4. g'16 f' |
  a'8 g'16 f' ees'8 d'16 f' ees'4 d'8. fis'16 |
  % 16-17 free
  g'8 d' ees'4 d'4 ees'8 d' |
  d'8 ees'4 g'8 fis'4. g'8 |
  % 18-19
  d'4 ees' d' b8 d' |
  c'2 b4 r4 |
  % 20-21 subject in C minor (manuals only)
  c'4. c'16 b c'4. c'16 b |
  c'8. d'16 d'8. f'16 f'4. ees'16 c' |
  R1*16 |
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
  % 10-11
  bes4. bes16 a g8. ees16 c8 a16 f |
  c'8. a16 f8 d'16 bes aes4. g8 |
  % 12-13
  g4 aes8 c' bes2 |
  bes4 c' d' bes |
  R1*2 |
  % 16-17 subject in G minor
  g4. g16 fis g4. g16 fis |
  g8. a16 a8. c'16 c'4. bes16 g |
  % 18-19 (bass of the manuals-only passage)
  g,4 ees8 c g, b, g,4 |
  aes,4 f, g, g8 f |
  % 20-21 countersubject (C minor, below alto)
  r8 ees aes g16 f ees8 c d4 |
  ees4 f g8 f16 ees d8 c16 ees |
  R1*16 |
}

%% PEDAL
pedal = \absolute {
  R1*7 |
  % 8-9 answer (F)
  f,4. f,16 e, f,4. f,16 e, |
  f,8. g,16 g,8. bes,16 bes,4. a,16 f, |
  % 10-11
  g,4 g c c, |
  f,2 bes,2 |
  % 12-13
  ees4 aes, ees bes, |
  ees4 aes, f, d8 ees |
  % 14-15
  f2 ees |
  d2 c |
  % 16-17
  bes,4 c8 d g,4 c8 d |
  g,4 ees d4. g,8 |
  % 18-21 manuals only
  R1*4 |
  R1*16 |
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
