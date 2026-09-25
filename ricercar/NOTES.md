# The Neighbour: a listener's guide

*Ricercar a 4 on John Williams's Theme from Jurassic Park.* B-flat minor to B-flat major, 66 bars, about
four minutes. Four voices (soprano, alto, tenor, bass), written once and performed five ways.

Score: [`score/music-voices.ly`](score/music-voices.ly), assembled from [`score/sections/`](score/sections/),
whose comments explain every entry and device. Printed piano and string-quartet scores:
`score/out/piano.pdf` and `score/out/quartet.pdf` (engraved locally, see the README). Full design and proofs:
[`design/BLUEPRINT.md`](design/BLUEPRINT.md).

## The idea

The tune starts on a held B-flat, dips a semitone to A and comes back: a lower neighbour note. The piece
builds everything from that one gesture, at five scales:

1. **A note.** The subject states it twice in its first two bars.
2. **A line.** The first countersubject, the *lament*, chains the step into a slow chromatic fall
   (D-flat C B-flat A A-flat G-flat F). The second, the *motor*, is the same cell in running eighths.
3. **A mirror.** Turned upside down, the lower step B-flat to A becomes the upper step F to G-flat. The
   subject moves from tonic to dominant; its inversion (bar 35) moves from dominant back to tonic.
4. **A chord.** At the first climax all four voices hold a diminished seventh and then slide down a
   semitone together (28:4.5), a neighbour motion made by a whole chord.
5. **A key.** The middle of the piece sits in A minor, a semitone below the home key, and leaves it by
   E rising to F. The whole piece moves B-flat, A, B-flat: the subject's first three notes.

The tune is held back. Its first half is the fugue subject; its second half is the melody of the slow
arioso; the two halves sound together at bar 48; the whole tune is heard only at bar 55, untouched, in
B-flat major. The film's tune ends open, on C over the dominant. Here that C finally rises to D (bar 63),
the note that turns the minor into the major.

The shape follows the finale of Beethoven's Sonata Op. 110: fugue, collapse, *arioso dolente*, the fugue
inverted, a return to the light.

## Form

Timings are from the solo-piano render (`performance/beethoven_piano/`), including its 0.3 s lead-in. The
other versions differ by a few seconds; their own timings are in the next section. Bar:beat, 4/4.

| time | bars | part | what happens |
|---|---|---|---|
| 0:00 | 1-4 | **I Fugue**, entry 1 | The tune's first half alone, soprano, at its own pitch, in B-flat minor. |
| 0:13 | 5-8 | entry 2 | The answer at the fifth (alto, F minor); the lament enters above it. Two voices. |
| 0:25 | 9-12 | entry 3 | The subject in the bass, lament and motor above it: all three lines at once. |
| 0:37 | 13-17 | entry 4 | The answer in the tenor; the lament falls to low C in the bass; first four-voice writing; half close on C7 (17). |
| 0:53 | 18-19 | episode | A fragment of the tune in sequence over a bass falling in fifths, toward D-flat. |
| 0:59 | 20-26 | stretto, "false dawn" | The subject in D-flat major (tenor), then in G-flat major (soprano, 22:1, 1:05) before the first has finished. For the first time the tune sounds major, but it darkens (A-flat minor 24:4, C-flat 25) and sinks. |
| 1:18 | 26:3-29 | liquidation, **Climax I** | Four subject heads enter one by one on E, G, B-flat, D-flat until they form one diminished seventh (complete 28:1, 1:23); all four slide down a semitone (1:26); fermata; silence. |
| 1:34 | 30-34 | **II Arioso dolente** | The tune's second half, slow, over pulsing chords. Peak at 32:1 (1:44). The dominant seventh is reheard as a German sixth and the music turns to A minor (33-34). |
| 2:00 | 35-45 | **III Fuga inversa** | The subject upside down, alone in the bass; a second entry at the fifth overlaps it (37:1, 2:08); a third in the soprano (41:1, 2:22); a full cadence in A minor (45:3, 2:37). Its dominant, E major, resolves not to A but to F. |
| 2:39 | 46-47 | **IV Pedal** | The inversion in double note values in the bass becomes a long held F, the home dominant; the tenor's lament alone above it. |
| 2:46 | 48-49 | combination | Both halves of the tune together: the first in the tenor, the second in the alto. |
| 2:54 | 50-53 | **Climax II** | Subject heads at double speed climb F, G-flat, A, C (soprano) over the subject at normal speed and the inversion at half speed. C major at 52:1 (2:58); the peak, a full C7 at fff, at 53:1 (3:02); fermata on the dominant (3:05). |
| 3:08 | 54 | hinge | No break after the fermata: the dominant harmony continues while the soprano falls A F E-flat C A, and that A (the leading note) resolves to the tune's first B-flat. |
| 3:13 | 55-62 | **V Apotheosis** | The whole tune in B-flat major, untouched, over the lament and the motor turned major; its second half over the answer in the bass (59:1, 3:26); peak at 60:4 (3:33). |
| 3:41 | 63-64 | | C rises to D over a real V7-I; the inversion's head, now major, in the alto. |
| 3:49 | 65-66 | coda | The subject's B-flat A B-flat, last time, in the tenor over a tolling low B-flat, while the soprano sings D E-flat D, the same gesture upside down. Final chord 3:56; the file ends at 4:04. |

## The versions

All five play the same notes. Audio is rendered locally by each version's script in
`performance/<version>/` and is not in the repository.

**Bach: pipe organ** (`bach_organ/ricercar_bach_organ.m4a`, 4:02 with the church's decay). Norrfjärden
Church organ samples. Each voice has its own keyboard and stops (soprano Hauptwerck, alto Oberwerck, tenor
Rückpositief, bass Pedal), so the four lines differ in colour and position. Loudness changes in steps, by
adding stops at section joins, never by a swell; in Part I only the entering voice's keyboard steps up
at an entry. The tempo is steadier than in the other versions: one tempo per section. Listen for: the arioso's
Krummhorn solo (1:37); the augmented inversion in the pedal from 2:37, gaining reeds as Climax II builds;
the Posaune 16' and the full choruses at Climax II (2:57), kept back until then so it outweighs Climax I
(1:21); the hinge stepping down in three terraces (3:05); the tune on a single Principal over flutes (3:09),
then on the full Hauptwerck with its trumpet stop (3:23); the last chord on the softest stops (3:48).

**Beethoven: solo piano** (`beethoven_piano/ricercar_beethoven_piano.m4a`, 4:04). The main reading and the
source of the form table. Listen for: sudden drops to soft at 18, 24:3, 30 and 46 after each build; the
rubato arioso, easing into its 7-6 peak (1:44) and slowing to 40 at the pivot; the fuga inversa gathering
speed from 60 to 76 ("poi a poi di nuovo vivente"); one unbroken crescendo from 46 to the fff chord at 3:02,
the loudest moment of the piece; the apotheosis held to f, a glow rather than a third climax. Every
entry is voiced forward, and the voice it overlaps steps back.

**Beethoven: string quartet** (bonus, `beethoven_quartet/ricercar_beethoven_quartet.m4a`, 4:05). The piano
version's timing and dynamics on four solo strings; entries come forward by bow pressure, not by accent.
Listen for: the viola taking over the alto's lament at 9:4 (0:27), where it goes below violin II's range; the four players
lifting together into the silence before the arioso (about 1:33); the arioso's pulse bowed note by note (1:34);
Climax II (about 3:00) 2.3 LU louder than Climax I (about 1:30); the cello's tolling low B-flat under the last
entry (from 3:41).

**Symphonic: orchestra** (`symphonic/ricercar_symphonic.m4a`, 3:54). Colours change at phrase joins, as in
Webern's orchestration of Bach's six-part Ricercar. Every subject, answer and inversion entry starts in the strings; the lament walks down
the reeds (oboe 5:4, clarinet 9:4, bassoons 13:4). Listen for: the major-key stretto doubled by clarinet,
then oboe (0:59); Climax I built head by head in the brass, from low trombones and timpani up to the trumpet (from
1:19); the arioso as a woodwind choir with a solo horn (1:35); the fuga inversa in the strings (1:58); horns
holding the dominant F (2:36); trumpets on the double-speed heads of Climax II (from 2:50); the whole tune
on four horns (3:07), joined by violins, flute and trumpet at 3:21; timpani tolling the tonic and a solo
horn playing the last B-flat A B-flat (from 3:34).

**Ensemble: piano quintet** (`quintet/ricercar_quintet.m4a`, 3:54). After the fugue of Shostakovich's Piano
Quintet Op. 57. Strings alone through the exposition, the false dawn, Climax I and the arioso; the piano
enters with the fuga inversa (1:58) and carries it, the viola bringing the second entry. The cello returns
with the augmented inversion (2:36), violin II with the tune's second half, violin I with the double-speed
heads. Climax II and the apotheosis (3:07) are tutti with the piano in octaves; the coda thins to violin I's
D over the piano's tolling octaves.

## The learned devices, and where to hear them

| device | where (bar:beat) | what to listen for |
|---|---|---|
| real answer at the fifth | 5:1 alto, 13:1 tenor | The subject a fifth higher, its F-E-F neighbour kept intact. |
| triple invertible counterpoint | 9-12, 13-17, 55-58 | Subject, lament and motor fit in any vertical order (all six proven). Three orders are heard: subject at the bottom (9), in the middle (13), on top as the whole tune, with the other two in major (55). |
| Neapolitan chord | 12:3, 16:3; 25 as a key area | The chord on the flattened second degree (C-flat in B-flat minor, G-flat in F minor), a dark lift. |
| stretto at the fourth (plus an octave), in the relative major | 20:1 tenor (D-flat), 22:1 soprano (G-flat) | The subject overlapping itself, two bars apart. |
| liquidation into one chord | 26:3 E, 27:1 G, 27:3 B-flat, 28:1 D-flat; slide 28:4.5 | Heads pile up into a diminished seventh, which then slides a semitone into A dim7. |
| chain of suspensions | 18-19 (episode, tenor and alto) | Tied notes that clash with the new bass and resolve down one by one. |
| imitation of the second subject | 30:2 bass | The arioso's first three notes echoed two octaves down, a beat later, like a continuo bass in a Bach aria. |
| 7-6 and 4-3 suspensions | 32:1 alto, 33:3 tenor | The arioso's peak, and its arrival on the dominant seventh. |
| German-sixth pivot | 33-34 | The same four notes heard first as B-flat minor's dominant seventh, then as a chord pulling to A minor. |
| inversion (tonal mirror) | 35:1 bass | The subject upside down: B-flat A B-flat becomes F G-flat F, here in A minor E F E. |
| mirrored triple counterpoint | 35-39, 41-45 | The lament and motor inverted too; the lament now rises (bass, 41:4). |
| stretto of the inversion at the fifth | 37:1 tenor | The second inverted entry, two bars after the first. |
| deceptive cadence | 45:4 to 46:1 | E major (dominant of A minor) goes to F instead of A: E-F, the inversion's own step. |
| augmentation | 46:1 to 55:1 bass | The inversion in double note values: the long F is its repeated opening note, the G-flats its neighbours. |
| pedal points | 46-50 (dominant F), 63-66 (tonic B-flat, re-struck each bar) | A held bass under moving harmony. |
| combination of the two subjects | 48:1 tenor and alto | The tune's first and second halves at once. |
| diminution | 50:3 F, 51:1 G-flat, 51:3 A, 52:3 C (soprano); 52:1, 53:1 E (alto) | The subject's head at double speed: the piece's first sixteenth notes. |
| three speeds at once | 50-53 | Diminution (soprano), normal speed (tenor), augmentation (bass). |
| the tune as cantus firmus | 55:1 to 63:1 soprano | The whole tune over the fugue's own counterpoint turned major. |
| answer against its mirror | 61-62 bass and tenor | The answer and its inversion in contrary motion into the cadence. |
| inversion's head in major | 63 alto | Under the held D: F F G F; in 64, F G-flat F, a last glance at the minor. |
| the neighbour both ways | 65-66 | Tenor B-flat A B-flat (lower neighbour) against soprano D E-flat D (upper neighbour). |

## The tune tweaks, and why

| where | tweak | why |
|---|---|---|
| 1-54 | D becomes D-flat | B-flat minor. Only the third degree changes, and the tune's first three bars have none, so it stays recognisable. |
| the subject | the tune's bars 1 to 5:3, ending on F | Ends on the fifth, so the next entry can start where it stops. |
| 20-26 | the subject in D-flat major and G-flat major | The false dawn: the tune's major shape, heard early and in the wrong keys, before it collapses. |
| 34 | the arioso's last C held over E, then falling to B | A sighing minor sixth that turns the music to A minor. |
| 52 | the tenor's subject breaks off: its tail C-A-F becomes C-A-B-flat | The break opens onto C7, "the light" before the peak. |
| 55-62 | none | The whole tune, as Williams wrote it, in B-flat major. |
| 63 | the tune's last note, C, rises to D | The film leaves the tune open on the dominant; here it closes on the major third. |
| tempo | quarter = 78 in the fugue and 72 in the apotheosis (the film: 108) | Weight and gravity, while staying fast enough for the dotted rhythm to sound like the tune. |

Not the tune: three notes of the inverted motor (36-38) were changed to avoid augmented seconds.

## How it was checked

The assembled score passes `tools/check.py` (0 errors, 0 parallel fifths or octaves, 0 unjustified
dissonances) and `design/final-lab/strict.py` (0 clashes); every section is proven against the verified
skeleton by `splice_check.py`. `suspensions.py` counts 18 suspensions on strong beats and 13 on
weak beats.
