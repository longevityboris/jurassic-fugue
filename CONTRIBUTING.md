# Contributing

Ideas, corrections and alternative realisations are welcome.

- Counterpoint changes must pass the checkers before review: `python3 ricercar/tools/check.py FILE.ly --voices soprano,alto,tenor,bass` reports 0 PAR!, 0 BEAT and 0 DIS!, and section files pass `ricercar/design/final-lab/splice_check.py`.
- Do not commit audio renders or sample libraries; the setup scripts fetch samples.
- One change per pull request, with a message that says what it fixes and why.
