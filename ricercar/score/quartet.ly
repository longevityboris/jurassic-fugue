\version "2.24.0"
%% String-quartet score of the same music.
\include "music-global.ly"
\include "music-voices.ly"

\header {
  title = "Ricercar on the Theme from Jurassic Park"
  subtitle = "Double fugue a 4 in B-flat minor (string quartet)"
  composer = "Theme: John Williams (1993)"
  tagline = ##f
}
\paper { #(set-paper-size "a4") ragged-last-bottom = ##t }

\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = "Violin I" } << \global \marks \soprano \dynamicsLine >>
    \new Staff \with { instrumentName = "Violin II" } << \global \alto \dynamicsLine >>
    \new Staff \with { instrumentName = "Viola" } << \global \clef alto \tenor \dynamicsLine >>
    \new Staff \with { instrumentName = "Violoncello" } << \global \clef bass \bass \dynamicsLine >>
  >>
  \layout {
    \context { \Score
      barNumberVisibility = #all-bar-numbers-visible
      \override BarNumber.break-visibility = #end-of-line-invisible
      \override BarNumber.font-size = #-2 }
  }
}
