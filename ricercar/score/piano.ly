\version "2.24.0"
%% Piano score. Music (voices, global, dynamics, marks) comes from the included files.
\include "music-global.ly"
\include "music-voices.ly"

\header {
  title = "Ricercar on the Theme from Jurassic Park"
  subtitle = "Double fugue a 4 in B-flat minor"
  composer = "Theme: John Williams (1993)"
  arranger = "after J. S. Bach and L. van Beethoven"
  tagline = ##f
}
\paper { #(set-paper-size "a4") ragged-last-bottom = ##t }

\score {
  \new PianoStaff \with { instrumentName = "Piano" } <<
    \new Staff = "upper" << \global \marks
      \new Voice = "soprano" { \voiceOne \soprano }
      \new Voice = "alto" { \voiceTwo \alto } >>
    \new Dynamics \dynamicsLine
    \new Staff = "lower" << \global \clef bass
      \new Voice = "tenor" { \voiceOne \tenor }
      \new Voice = "bass" { \voiceTwo \bass } >>
  >>
  \layout {
    \context { \Score
      barNumberVisibility = #all-bar-numbers-visible
      \override BarNumber.break-visibility = #end-of-line-invisible
      \override BarNumber.font-size = #-2 }
  }
}
