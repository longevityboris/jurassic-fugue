#!/usr/bin/env python3
"""Jev calibration probe on The Neighbour's own data.

Question: which composition-kit decisions can TypeSafe's Jev (System One model) own,
which need a confidence gate, and which it should not touch?

Run (key comes from the macOS Keychain, never from this file):
    akm run --only TYPESAFE_API_KEY -- python3 docs/kit/jev_probe.py [--tasks t1,t2,t3,t4]

Tasks
  t1  before/after revision pairs of ricercar/score/sections/*.ly (git history, comments stripped;
      reviewers accepted the later version). Choice of the better version, both orders, two
      state representations (raw LilyPond, grid.py sonority table).
  t2  corrupted variants of real passages: parallel fifths against the bass, a semitone clash on a
      strong beat, a wrong note in a subject entry. Each corruption is validated with check.py
      (parallels / unjustified count must rise). Pairwise Choice (both orders, both representations)
      and single-passage Noul (original vs corrupted).
  t3  review-finding triage from the workflow journals: severity (major/minor) on full text and on
      a redacted first sentence, routing (notes vs performance), section lookup (vs a regex).
  t4  the four design proposals' DESIGN.md, pairwise, vs the judges' totals.

Writes every raw answer to docs/kit/jev_probe_results.jsonl and a summary to
docs/kit/jev_probe_summary.json.
"""
import glob
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RIC = os.path.join(ROOT, 'ricercar')
sys.path.insert(0, os.path.join(RIC, 'tools'))
from lyparse import TOK, _dur  # noqa: E402

OUT = os.path.join(ROOT, 'docs', 'kit')
RESULTS = os.path.join(OUT, 'jev_probe_results.jsonl')
MODEL = 'jev-1.13.0'
PRICE_PER_TOKEN = 0.042 / 1e6
URL = 'https://api.typesafe.ai/v1/systemone'
JOURNALS = os.path.expanduser('~/.claude/projects/-Users-biobook-Music-llm-music-fugue-jp/*/subagents/workflows/*/journal.jsonl')
VOICES = ['soprano', 'alto', 'tenor', 'bass']
SECTIONS = [('sec01_expo', 1, 12, 'exposition'), ('sec02_entry4_episode', 13, 19, 'fourth entry and episode'),
            ('sec03_stretto_liquidation', 20, 29, 'stretto, liquidation, Climax I'),
            ('sec04_arioso', 30, 34, 'arioso'), ('sec05_inversa', 35, 45, 'fuga inversa'),
            ('sec06_pedal_climax', 46, 54, 'pedal and Climax II'),
            ('sec07_apotheosis_coda', 55, 66, 'apotheosis and coda')]
rng = random.Random(20260925)
_log_lock = __import__('threading').Lock()


# ---------------------------------------------------------------- API
def ask(task, item, state, questions, meta=None):
    body = json.dumps({'state': state, 'model': MODEL, 'questions': questions}).encode()
    key = os.environ['TYPESAFE_API_KEY']
    for attempt in range(5):
        req = urllib.request.Request(URL, data=body, headers={
            'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 4:
                time.sleep(float(e.headers.get('retry-after') or 2 ** attempt))
                continue
            raise
    lat = time.time() - t0
    rec = {'task': task, 'item': item, 'model': resp.get('model'), 'latency_s': round(lat, 3),
           'input_tokens': resp['usage']['input_tokens'], 'answers': resp['answers'], 'meta': meta or {}}
    with _log_lock:
        with open(RESULTS, 'a') as f:
            f.write(json.dumps(rec) + '\n')
    return rec


def run_all(jobs, workers=8):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda j: ask(*j), jobs))


# ---------------------------------------------------------------- LilyPond helpers
def strip_comments(src):
    return '\n'.join(re.sub(r'%.*', '', ln).rstrip() for ln in src.splitlines() if re.sub(r'%.*', '', ln).strip())


def voice_span(src, name):
    m = re.search(r'(?m)^' + name + r'\s*=\s*\\absolute\s*\{(.*?)^\}', src, re.S)
    return m.span(1) if m else None


def voice_bars(src, name):
    sp = voice_span(src, name)
    body = re.sub(r'%.*', '', src[sp[0]:sp[1]])
    bars = [b.strip() for b in body.split('|')]
    return [b for b in bars if b]


def lily_window(src, a, b):
    """Voices' LilyPond text for section-relative bars a..b (inclusive)."""
    lines = []
    for v in VOICES:
        bars = voice_bars(src, v)
        lines.append(f'{v}: ' + ' | '.join(bars[a - 1:b]) + ' |')
    return 'Four voices, LilyPond absolute pitch (c\' = middle C), 4/4, one line per voice:\n' + '\n'.join(lines)


def grid_window(src, a, b):
    with tempfile.NamedTemporaryFile('w', suffix='.ly', delete=False) as f:
        f.write(src)
    out = subprocess.run([sys.executable, os.path.join(RIC, 'design', 'final-lab', 'grid.py'), f.name,
                          '--bars', f'{a}-{b}'], capture_output=True, text=True).stdout
    os.unlink(f.name)
    return ('Sonority grid, one row per eighth note: position (bar:beat), soprano alto tenor bass '
            "(pitch; '.' = held, '-' = rest), chord name.\n" + out)


def check_counts(src):
    with tempfile.NamedTemporaryFile('w', suffix='.ly', delete=False) as f:
        f.write(src)
    out = subprocess.run([sys.executable, os.path.join(RIC, 'tools', 'check.py'), f.name, '--quiet'],
                         capture_output=True, text=True).stdout
    os.unlink(f.name)
    m = re.search(r'errors (\d+), parallels (\d+), beat-par (\d+), unjustified (\d+)', out)
    return tuple(int(x) for x in m.groups()) if m else None


NAMES = {0: 'c', 1: 'des', 2: 'd', 3: 'ees', 4: 'e', 5: 'f', 6: 'ges', 7: 'g', 8: 'aes', 9: 'a', 10: 'bes', 11: 'b'}
SHARPS = {0: 'c', 1: 'cis', 2: 'd', 3: 'dis', 4: 'e', 5: 'f', 6: 'fis', 7: 'g', 8: 'gis', 9: 'a', 10: 'ais', 11: 'b'}


def lily_name(midi, sharp=False):
    # spell like the surrounding section so the altered note does not give itself away by its spelling
    o = midi // 12 - 4
    return (SHARPS if sharp else NAMES)[midi % 12] + ("'" * o if o > 0 else ',' * -o)


def chains(src, name):
    """Notes of one voice with token spans: [{start, end, midi, spans:[(a,b)]}] (ties merged)."""
    off = voice_span(src, name)[0]
    body = src[off:voice_span(src, name)[1]]
    body_nc = re.sub(r'%[^\n]*', lambda m: ' ' * len(m.group(0)), body)
    t, dur, out, tie, pos = F(0), F(1, 4), [], False, 0
    while pos < len(body_nc):
        if body_nc[pos].isspace() or body_nc[pos] in '{}':
            pos += 1
            continue
        mt = TOK.match(body_nc, pos)
        if not mt:
            pos += 1
            continue
        pos = mt.end()
        g = mt.groupdict()
        if g['note']:
            n = g['note']
            acc = n[1:].rstrip("',")
            midi = 12 * (4 + n.count("'") - n.count(',')) + dict(c=0, d=2, e=4, f=5, g=7, a=9, b=11)[n[0]] + \
                {'': 0, 'is': 1, 'es': -1, 'isis': 2, 'eses': -2}[acc]
            if g['dur']:
                dur = _dur(g['dur'], g['dot'])
            span = (off + mt.start('note'), off + mt.end('note'))
            if tie and out and out[-1]['midi'] == midi and out[-1]['end'] == t:
                out[-1]['end'] += dur
                out[-1]['spans'].append(span)
            else:
                out.append({'start': t, 'end': t + dur, 'midi': midi, 'spans': [span]})
            t += dur
            tie = bool(g['tie'])
        elif g['rest']:
            if g['rdur']:
                dur = _dur(g['rdur'], g['rdot'])
            t += dur * (int(g['mult']) if g['mult'] else 1)
            tie = False
        elif g['tie2']:
            tie = True
    return out


def apply(src, edits):
    """edits: list of (chain, new_midi). Replace every tied token of each chain."""
    body = re.sub(r'%.*', '', src)
    sharp = len(re.findall(r'\b[a-g]is', body)) > len(re.findall(r'\b[a-g]es|\bas\b', body))
    reps = []
    for ch, m in edits:
        for a, b in ch['spans']:
            reps.append((a, b, lily_name(m, sharp)))
    for a, b, s in sorted(reps, reverse=True):
        src = src[:a] + s + src[b:]
    return src


def bar_of(t):
    return int(t) + 1  # whole-note units, 4/4


# ---------------------------------------------------------------- T1 revision pairs
def t1_items():
    shas = subprocess.run(['git', '-C', ROOT, 'log', '--format=%H', '--', 'ricercar/score/sections/'],
                          capture_output=True, text=True).stdout.split()
    items = []
    for sha in shas:
        files = subprocess.run(['git', '-C', ROOT, 'show', '--name-only', '--format=', sha, '--',
                                'ricercar/score/sections/'], capture_output=True, text=True).stdout.split()
        for fp in files:
            before = subprocess.run(['git', '-C', ROOT, 'show', f'{sha}^:{fp}'], capture_output=True, text=True)
            after = subprocess.run(['git', '-C', ROOT, 'show', f'{sha}:{fp}'], capture_output=True, text=True)
            if before.returncode or after.returncode:
                continue
            b, a = strip_comments(before.stdout), strip_comments(after.stdout)
            if b == a:
                continue
            try:
                bb = {v: voice_bars(b, v) for v in VOICES}
                ab = {v: voice_bars(a, v) for v in VOICES}
            except Exception:
                continue
            n = len(ab['soprano'])
            if any(len(bb[v]) != n or len(ab[v]) != n for v in VOICES):
                continue
            diff = [i + 1 for i in range(n) if any(bb[v][i].split() != ab[v][i].split() for v in VOICES)]
            if not diff:
                continue
            items.append({'sha': sha[:7], 'file': os.path.basename(fp), 'before': b, 'after': a,
                          'bars': (min(diff), max(diff)), 'n_diff_bars': len(diff)})
    return items


T1_Q = ('Two versions of the same passage of a four-voice fugue (Bach style) differ in some notes. '
        'Which version is the better-written counterpoint: smoother and more independent lines, dissonances '
        'properly prepared and resolved, no parallel or hidden perfect fifths/octaves, fuller harmony, '
        'and more rhythmic independence between voices?')


def t1_jobs(items):
    jobs = []
    for i, it in enumerate(items):
        a0, a1 = it['bars']
        for rep in ('lily', 'grid'):
            fn = lily_window if rep == 'lily' else grid_window
            txt = {'before': fn(it['before'], a0, a1), 'after': fn(it['after'], a0, a1)}
            for order in (('before', 'after'), ('after', 'before')):
                state = {'version_1': txt[order[0]], 'version_2': txt[order[1]]}
                truth = 'version_1' if order[0] == 'after' else 'version_2'
                q = {'better': {'type': 'choice', 'instructions': T1_Q,
                                'criteria': {'version_1': 'version_1 is better', 'version_2': 'version_2 is better'}}}
                jobs.append(('t1', f"{it['sha']}:{it['file']}:{rep}:{order[0]}", state, q,
                             {'truth': truth, 'rep': rep, 'pair': f"{it['sha']}:{it['file']}", 'slot_after': truth,
                              'bars': it['bars']}))
    return jobs


# ---------------------------------------------------------------- T2 corruptions
SUBJECT_ENTRIES = [('sec01_expo', 'soprano', 1, 4, 'subject'), ('sec01_expo', 'alto', 5, 8, 'answer'),
                   ('sec01_expo', 'bass', 9, 12, 'subject'), ('sec02_entry4_episode', 'tenor', 1, 4, 'answer')]


def t2_items(n_par=10, n_dis=10):
    items = []
    secs = {s: open(os.path.join(RIC, 'score', 'sections', s + '.ly')).read() for s, *_ in SECTIONS}
    base = {s: check_counts(src) for s, src in secs.items()}
    # parallel fifths against the bass
    cands = []
    for s, src in secs.items():
        bass = [c for c in chains(src, 'bass')]
        for v in ('soprano', 'alto', 'tenor'):
            vc = chains(src, v)
            by_start = {c['start']: k for k, c in enumerate(vc)}
            for b1, b2 in zip(bass, bass[1:]):
                if b1['midi'] == b2['midi'] or b1['end'] != b2['start']:
                    continue
                k1, k2 = by_start.get(b1['start']), by_start.get(b2['start'])
                if k1 is None or k2 != (k1 + 1 if k1 is not None else None):
                    continue
                x1, x2 = vc[k1], vc[k2]
                opts = [m for m in range(b1['midi'] + 7, 100, 12) if abs(m - x1['midi']) <= 5]
                if not opts:
                    continue
                n1 = min(opts, key=lambda m: abs(m - x1['midi']))
                n2 = n1 + (b2['midi'] - b1['midi'])
                if abs(n2 - x2['midi']) > 5 or (n1 == x1['midi'] and n2 == x2['midi']):
                    continue
                cands.append((s, v, x1, x2, n1, n2))
    rng.shuffle(cands)
    used = set()
    for s, v, x1, x2, n1, n2 in cands:
        if sum(1 for it in items if it['kind'] == 'parallel5') >= n_par:
            break
        key = (s, bar_of(x1['start']))
        if key in used:
            continue
        new = apply(secs[s], [(x1, n1), (x2, n2)])
        c = check_counts(new)
        if c and c[1] > base[s][1]:
            used.add(key)
            b = bar_of(x1['start'])
            a0, a1 = (b, b + 1) if bar_of(x2['start']) > b or b < len(voice_bars(secs[s], 'soprano')) else (b - 1, b)
            a1 = min(a1, len(voice_bars(secs[s], 'soprano')))
            items.append({'kind': 'parallel5', 'section': s, 'voice': v, 'orig': secs[s], 'bad': new,
                          'bars': (a0, max(a1, bar_of(x2['start']))), 'check': (base[s], c)})
    # strong-beat semitone clash that check.py calls unjustified
    cands = []
    for s, src in secs.items():
        for v in ('soprano', 'alto', 'tenor'):
            for ch in chains(src, v):
                beat = (ch['start'] - int(ch['start'])) * 4
                if beat in (0, 2):
                    cands.append((s, v, ch, rng.choice([1, -1])))
    rng.shuffle(cands)
    for s, v, ch, d in cands:
        if sum(1 for it in items if it['kind'] == 'clash') >= n_dis:
            break
        key = (s, bar_of(ch['start']))
        if key in used:
            continue
        new = apply(secs[s], [(ch, ch['midi'] + d)])
        c = check_counts(new)
        if c and c[3] > base[s][3] and c[1] == base[s][1]:
            used.add(key)
            b = bar_of(ch['start'])
            n = len(voice_bars(secs[s], 'soprano'))
            a0, a1 = (b, b + 1) if b < n else (b - 1, b)
            items.append({'kind': 'clash', 'section': s, 'voice': v, 'orig': secs[s], 'bad': new,
                          'bars': (a0, a1), 'check': (base[s], c)})
    # wrong note in a subject entry (tone up or down, never the first note)
    for s, v, a0, a1, form in SUBJECT_ENTRIES:
        src = secs[s]
        entry = [c for c in chains(src, v) if a0 <= bar_of(c['start']) <= a1]
        for k in rng.sample(range(2, len(entry)), 2):
            d = rng.choice([2, -2])
            items.append({'kind': 'subject_note', 'section': s, 'voice': v, 'form': form,
                          'orig': src, 'bad': apply(src, [(entry[k], entry[k]['midi'] + d)]), 'bars': (a0, a1)})
    return items


SUBJECT_TXT = ("bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'8 | "
               "(B-flat minor; the answer is the same line a fifth higher or a fourth lower, starting on F)")


def t2_jobs(items):
    jobs = []
    for i, it in enumerate(items):
        a0, a1 = it['bars']
        for rep in ('lily', 'grid'):
            fn = lily_window if rep == 'lily' else grid_window
            txt = {'orig': fn(it['orig'], a0, a1), 'bad': fn(it['bad'], a0, a1)}
            if it['kind'] == 'subject_note':
                instr = {'subject': SUBJECT_TXT,
                         'question': f"One version has one altered note in the {it['voice']}'s entry of `subject`. "
                                     'Which version states the subject (or its answer) exactly as written?'}
            else:
                instr = ('One of these two versions of a passage from a four-voice fugue contains an inserted '
                         'voice-leading error (for example parallel fifths or an unprepared, unresolved dissonance). '
                         'Which version is the original, correctly written one?')
            for order in (('orig', 'bad'), ('bad', 'orig')):
                state = {'version_1': txt[order[0]], 'version_2': txt[order[1]]}
                truth = 'version_1' if order[0] == 'orig' else 'version_2'
                q = {'correct': {'type': 'choice', 'instructions': instr,
                                 'criteria': {'version_1': 'version_1 is the correct original',
                                              'version_2': 'version_2 is the correct original'}}}
                jobs.append(('t2_pair', f"{i}:{it['kind']}:{rep}:{order[0]}", state, q,
                             {'truth': truth, 'rep': rep, 'kind': it['kind'], 'item': i}))
            if it['kind'] != 'subject_note':
                for which in ('orig', 'bad'):
                    q = {'error': {'type': 'noul',
                                   'instructions': 'Does this passage of four-voice counterpoint contain a voice-leading '
                                                   'error: parallel perfect fifths or octaves between two voices, or a '
                                                   'dissonance on a strong beat that is neither prepared nor resolved by step?'}}
                    jobs.append(('t2_single', f"{i}:{it['kind']}:{rep}:{which}", txt[which], q,
                                 {'truth': which == 'bad', 'rep': rep, 'kind': it['kind'], 'item': i}))
    return jobs


# ---------------------------------------------------------------- T3 review triage
REDACT = r'\b(major|minor|serious|seriously|weakest|optional|critical|important|broken|breaks|worst|must|rule \d+|rule)\b'


def section_of_bar(bar):
    for s, lo, hi, _ in SECTIONS:
        if lo <= bar <= hi:
            return s
    return None


def t3_items(max_items=100):
    out = []
    for jf in glob.glob(JOURNALS):
        labels = {}
        for line in open(jf):
            d = json.loads(line)
            if d.get('type') == 'started':
                labels[d['key']] = d.get('label') or ''
            if d.get('type') == 'result' and isinstance(d.get('result'), dict) and d['result'].get('issues'):
                lab = labels.get(d['key'], '')
                src = 'listen' if lab.startswith('listen') else 'panel' if lab.startswith('panel') else 'review'
                for iss in d['result']['issues']:
                    if iss.get('severity') not in ('major', 'minor'):
                        continue
                    where = iss.get('where', '')
                    m = re.search(r'sec0\d_[a-z0-9_]+', where)
                    sec = m.group(0) if m else None
                    if not sec:
                        mb = re.search(r'\b(\d{1,2}):\d', where) or re.search(r'[Bb]ars? (\d{1,2})', where)
                        sec = section_of_bar(int(mb.group(1))) if mb else None
                    out.append({'label': lab, 'source': src, 'severity': iss['severity'], 'section': sec,
                                'issue': iss.get('issue', ''), 'fix': iss.get('fix', ''), 'where': where})
    listen = [o for o in out if o['source'] == 'listen']
    other = [o for o in out if o['source'] != 'listen']
    rng.shuffle(other)
    return listen + other[:max_items - len(listen)], len(out)


def first_sentence(txt):
    s = re.split(r'(?<=[.!?])\s+', txt.strip())[0]
    return re.sub(REDACT, '[..]', s, flags=re.I)


def regex_section(txt):
    m = re.search(r'\b(\d{1,2}):\d', txt) or re.search(r'\b[Bb]ars? (\d{1,2})', txt)
    return section_of_bar(int(m.group(1))) if m else None


SEV_Q = {'type': 'choice', 'instructions': 'How severe is this review finding about a composed fugue or its recording?',
         'criteria': {'major': 'major: a real defect a listener or expert would notice, or a broken rule of the style; must be fixed',
                      'minor': 'minor: a nuance, polish item, or optional improvement'}}
ROUTE_Q = {'type': 'choice', 'instructions': 'Who has to act on this finding?',
           'criteria': {'notes': 'the composer: change the written notes, voice leading or harmony in the score',
                        'performance': 'the performance/audio engineer: change dynamics, articulation, instrument '
                                       'rendering, mixing or the audio file'}}


def t3_jobs(items):
    table = '; '.join(f'{s}: bars {lo}-{hi} ({d})' for s, lo, hi, d in SECTIONS)
    sec_q = {'type': 'choice',
             'instructions': {'sections': table,
                              'question': 'Which section of the piece does this finding refer to? Use the bar numbers '
                                          '(bar:beat) in the finding and the bar ranges in `sections`.'},
             'criteria': {s: f'bars {lo}-{hi}' for s, lo, hi, _ in SECTIONS}}
    jobs = []
    for i, it in enumerate(items):
        full = it['issue'] + ('\nSuggested fix: ' + it['fix'] if it['fix'] else '')
        meta = {'severity': it['severity'], 'section': it['section'], 'source': it['source'],
                'route': 'performance' if it['source'] == 'listen' else 'notes',
                'regex_section': regex_section(it['issue'])}
        jobs.append(('t3_full', f'{i}', full, {'severity': SEV_Q, 'route': ROUTE_Q, 'section': sec_q}, meta))
        jobs.append(('t3_redacted', f'{i}', first_sentence(it['issue']), {'severity': SEV_Q}, meta))
    return jobs


# ---------------------------------------------------------------- T4 proposals
JUDGES = {'proposal-1': 22.5, 'proposal-2': 23, 'proposal-3': 21.5, 'proposal-4': 18}


def t4_jobs(chars=6000):
    docs = {p: open(os.path.join(RIC, 'design', p, 'DESIGN.md')).read()[:chars] for p in JUDGES}
    jobs = []
    ps = sorted(JUDGES)
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            for a, b in ((ps[i], ps[j]), (ps[j], ps[i])):
                q = {'better': {'type': 'choice',
                                'instructions': 'Two design proposals for a four-voice double fugue on the same tune. '
                                                'Which design promises the more intellectually rich and musically '
                                                'convincing piece (quality of subject and countersubjects, invertible '
                                                'counterpoint, stretto, form, and a credible plan to realise it)?',
                                'criteria': {'proposal_A': None, 'proposal_B': None}}}
                truth = 'proposal_A' if JUDGES[a] > JUDGES[b] else 'proposal_B'
                jobs.append(('t4', f'{a}>{b}', {'proposal_A': docs[a], 'proposal_B': docs[b]}, q,
                             {'truth': truth, 'a': a, 'b': b}))
    return jobs


# ---------------------------------------------------------------- analysis
def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** .5 / d
    return (round(c - h, 3), round(c + h, 3))


def summarize(recs, extra):
    S = {'extra': extra, 'tasks': {}}
    calib = []  # (conf, pmax, correct, task)

    def acc(rows, key, truthf, qn):
        k = n = 0
        for r in rows:
            a = r['answers'][qn]
            ok = a['choice'] == truthf(r)
            k += ok
            n += 1
            calib.append((a['confidence'], max(a['probabilities'].values()), ok, key))
        return {'n': n, 'acc': round(k / n, 3) if n else None, 'ci95': wilson(k, n)}

    by = lambda t: [r for r in recs if r['task'] == t]  # noqa: E731
    # t1
    t1 = by('t1')
    for rep in ('lily', 'grid'):
        rows = [r for r in t1 if r['meta']['rep'] == rep]
        if not rows:
            continue
        d = acc(rows, f't1_{rep}', lambda r: r['meta']['truth'], 'better')
        d['picked_slot1'] = round(sum(r['answers']['better']['choice'] == 'version_1' for r in rows) / len(rows), 3)
        pairs = {}
        for r in rows:
            pairs.setdefault(r['meta']['pair'], []).append(r['answers']['better']['choice'] == r['meta']['truth'])
        d['pairs'] = len(pairs)
        d['consistent_pairs'] = sum(len(v) == 2 and v[0] == v[1] for v in pairs.values())
        d['both_orders_right'] = sum(len(v) == 2 and all(v) for v in pairs.values())
        S['tasks'][f't1_{rep}'] = d
    # t2 pairwise
    t2 = by('t2_pair')
    for rep in ('lily', 'grid'):
        for kind in ('parallel5', 'clash', 'subject_note', None):
            rows = [r for r in t2 if r['meta']['rep'] == rep and (kind is None or r['meta']['kind'] == kind)]
            if not rows:
                continue
            key = f't2_pair_{rep}_{kind or "all"}'
            d = acc(rows, key if kind else f'_{key}', lambda r: r['meta']['truth'], 'correct')
            if kind is None:
                calib[:] = [c for c in calib if c[3] != f'_{key}']
            d['picked_slot1'] = round(sum(r['answers']['correct']['choice'] == 'version_1' for r in rows) / len(rows), 3)
            items = {}
            for r in rows:
                items.setdefault(r['meta']['item'], []).append(r['answers']['correct']['choice'] == r['meta']['truth'])
            d['both_orders_right'] = f"{sum(all(v) and len(v) == 2 for v in items.values())}/{len(items)}"
            S['tasks'][key] = d
    # t2 single (noul)
    t2s = by('t2_single')
    for rep in ('lily', 'grid'):
        rows = [r for r in t2s if r['meta']['rep'] == rep]
        if not rows:
            continue
        p_bad = [r['answers']['error']['noul'] for r in rows if r['meta']['truth']]
        p_ok = [r['answers']['error']['noul'] for r in rows if not r['meta']['truth']]
        auc = sum((b > o) + 0.5 * (b == o) for b in p_bad for o in p_ok) / (len(p_bad) * len(p_ok))
        acc5 = sum((r['answers']['error']['noul'] > .5) == r['meta']['truth'] for r in rows) / len(rows)
        S['tasks'][f't2_single_{rep}'] = {'n': len(rows), 'auc': round(auc, 3), 'acc_at_0.5': round(acc5, 3),
                                          'mean_p_error_corrupted': round(sum(p_bad) / len(p_bad), 3),
                                          'mean_p_error_original': round(sum(p_ok) / len(p_ok), 3)}
    # t3
    t3f, t3r = by('t3_full'), by('t3_redacted')
    if t3f:
        base_major = sum(r['meta']['severity'] == 'major' for r in t3f) / len(t3f)
        S['tasks']['t3_severity_full'] = acc(t3f, 't3_severity_full', lambda r: r['meta']['severity'], 'severity')
        S['tasks']['t3_severity_full']['base_rate_major'] = round(base_major, 3)
        S['tasks']['t3_severity_full']['picked_major'] = round(
            sum(r['answers']['severity']['choice'] == 'major' for r in t3f) / len(t3f), 3)
        S['tasks']['t3_severity_redacted'] = acc(t3r, 't3_severity_redacted', lambda r: r['meta']['severity'], 'severity')
        S['tasks']['t3_severity_redacted']['picked_major'] = round(
            sum(r['answers']['severity']['choice'] == 'major' for r in t3r) / len(t3r), 3)
        S['tasks']['t3_route'] = acc(t3f, 't3_route', lambda r: r['meta']['route'], 'route')
        S['tasks']['t3_route']['base_rate_notes'] = round(sum(r['meta']['route'] == 'notes' for r in t3f) / len(t3f), 3)
        rows = [r for r in t3f if r['meta']['section']]
        S['tasks']['t3_section'] = acc(rows, 't3_section', lambda r: r['meta']['section'], 'section')
        rx = [r for r in rows if r['meta']['regex_section']]
        S['tasks']['t3_section']['regex_coverage'] = f"{len(rx)}/{len(rows)}"
        S['tasks']['t3_section']['regex_acc_when_found'] = round(
            sum(r['meta']['regex_section'] == r['meta']['section'] for r in rx) / max(1, len(rx)), 3)
        S['tasks']['t3_section']['jev_acc_on_regex_covered'] = round(
            sum(r['answers']['section']['choice'] == r['meta']['section'] for r in rx) / max(1, len(rx)), 3)
    # t4
    t4 = by('t4')
    if t4:
        S['tasks']['t4'] = acc(t4, 't4', lambda r: r['meta']['truth'], 'better')
        wins = {p: 0.0 for p in JUDGES}
        for r in t4:
            p = r['answers']['better']['probabilities']
            wins[r['meta']['a']] += p['proposal_A']
            wins[r['meta']['b']] += p['proposal_B']
        S['tasks']['t4']['jev_soft_wins'] = {k: round(v, 2) for k, v in wins.items()}
        S['tasks']['t4']['judges'] = JUDGES
    # calibration (Choice answers only)
    bins = [(0, .25), (.25, .5), (.5, .75), (.75, .9), (.9, 1.01)]
    table = []
    for lo, hi in bins:
        rows = [c for c in calib if lo <= c[0] < hi]
        if rows:
            table.append({'conf': f'{lo:.2f}-{min(hi, 1):.2f}', 'n': len(rows),
                          'acc': round(sum(c[2] for c in rows) / len(rows), 3),
                          'mean_pmax': round(sum(c[1] for c in rows) / len(rows), 3)})
    S['reliability_by_confidence'] = table
    S['ece_pmax'] = round(sum(abs(sum(c[2] for c in g) / len(g) - sum(c[1] for c in g) / len(g)) * len(g)
                              for g in [[c for c in calib if lo <= c[1] < hi] for lo, hi in
                                        [(0, .6), (.6, .7), (.7, .8), (.8, .9), (.9, 1.01)]] if g) / max(1, len(calib)), 3)
    per_task_cal = {}
    for c in calib:
        per_task_cal.setdefault(c[3], []).append(c)
    S['high_conf_acc'] = {k: {'n_conf>=0.75': len([c for c in v if c[0] >= .75]),
                              'acc_conf>=0.75': round(sum(c[2] for c in v if c[0] >= .75) / max(1, len([c for c in v if c[0] >= .75])), 3),
                              'n_conf<0.5': len([c for c in v if c[0] < .5]),
                              'acc_conf<0.5': round(sum(c[2] for c in v if c[0] < .5) / max(1, len([c for c in v if c[0] < .5])), 3)}
                          for k, v in per_task_cal.items()}
    lats = sorted(r['latency_s'] for r in recs)
    toks = sum(r['input_tokens'] for r in recs)
    nq = sum(len(r['answers']) for r in recs)
    S['cost'] = {'requests': len(recs), 'decisions': nq, 'input_tokens': toks,
                 'usd': round(toks * PRICE_PER_TOKEN, 4),
                 'latency_p50_s': lats[len(lats) // 2] if lats else None,
                 'latency_p95_s': lats[int(len(lats) * .95)] if lats else None,
                 'mean_input_tokens': round(toks / max(1, len(recs))),
                 'models': sorted({r['model'] for r in recs})}
    per_task_lat = {}
    for r in recs:
        per_task_lat.setdefault(r['task'], []).append(r['latency_s'])
    S['cost']['latency_p50_by_task'] = {k: sorted(v)[len(v) // 2] for k, v in per_task_lat.items()}
    return S


def main():
    tasks = (sys.argv[sys.argv.index('--tasks') + 1] if '--tasks' in sys.argv else 't1,t2,t3,t4').split(',')
    if '--summarize' not in sys.argv:
        extra = {}
        jobs = []
        if 't3' in tasks:
            items, total = t3_items()
            extra['t3_pool'] = total
            extra['t3_used'] = len(items)
            jobs += t3_jobs(items)
        if 't2' in tasks:
            items = t2_items()
            extra['t2_items'] = [{k: it[k] for k in ('kind', 'section', 'voice', 'bars')} | {'check': it.get('check')}
                                 for it in items]
            jobs += t2_jobs(items)
        if 't1' in tasks:
            items = t1_items()
            extra['t1_items'] = [{k: it[k] for k in ('sha', 'file', 'bars', 'n_diff_bars')} for it in items]
            jobs += t1_jobs(items)
        if 't4' in tasks:
            jobs += t4_jobs()
        print(f'{len(jobs)} requests', file=sys.stderr)
        json.dump(extra, open(os.path.join(OUT, 'jev_probe_items.json'), 'w'), indent=1, default=str)
        run_all(jobs)
    extra = json.load(open(os.path.join(OUT, 'jev_probe_items.json')))
    recs = [json.loads(ln) for ln in open(RESULTS)]
    S = summarize(recs, {k: v for k, v in extra.items() if not k.endswith('_items')} |
                  {'t1_pairs': len(extra.get('t1_items', [])), 't2_items': len(extra.get('t2_items', []))})
    json.dump(S, open(os.path.join(OUT, 'jev_probe_summary.json'), 'w'), indent=1)
    print(json.dumps(S, indent=1))


if __name__ == '__main__':
    main()
