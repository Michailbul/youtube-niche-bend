# SPEC — Niche-Bend Harness / Opportunity Engine

> **History.** Written on Michael's machine during the October 2026 build. Paths are relative to his explainers repo and session ids point to his logs; the plugin layout is in `../SKILL.md`.

**Status:** proposed, not built. Everything below is the build target agreed at seq 986–997 of `ses_ea1be2fa8ffeBEyi0Ob1Iff6hO`.

## 1. Shape

One project skill, one state file, one board, one runner. The existing skill stays the knowledge base; the harness is the machine around it.

```
niche-bend/harness/
  README.md  TASK.md  SPEC.md  LINKS.md  STATE.md
  state.json                 # the single source of truth for the current run
  runs/2026-10-25/           # one folder per run: ledger, candidates, verdicts, artifacts
  board/                     # the 3D opportunity space (HTML + Three.js)
  skill/SKILL.md             # the project skill; a thin global pointer points here
```

The global skill (`~/.claude/skills/` or `.agents/skills/`) only says: “For niche-bend work, read `niche-bend/harness/skill/SKILL.md`.” The detailed instructions live with the project, so they evolve with the data.

## 2. The modes

Each mode is a function with a typed input and one artifact. A mode can be run alone; the runner chains them.

### DISCOVER
**Input:** watch seeds, the no-go list, the last run’s ledger.
**Does:** formula watch (`formulas`), spread on survivors (`spread`), this-month search by views, channel checks; drops anything on the no-go list or already in a previous round.
**Output:** `candidates.json` — source video, format formula, niche, proof numbers, freshness, `sourceThumb`, `sourceFrames`.

### VALIDATE
**Input:** `candidates.json`.
**Does:** scorecard (median, not-one-hit, fresh, still posting, views above size, faceless, makeable, monetisation risk); then demand/saturation/fit; then three independent scouts + a separate reconciler.
**Output:** `verdicts.json` — `Proven` / `Format only` / `Pass`, with the evidence and the contradiction notes. The proposer never writes this verdict.

### ADAPT
**Input:** the kept formats + target niches.
**Does:** bend / restyle / merge. Writes our title under the source title, the thumbnail layout, the structure, the tension line, the urgency line, the first 30 seconds, and the facts to check.
**Output:** `packages.json` — one packaged idea per crossing, with `sourceTitle`, `ourTitle`, `thumbnail`, `tension`, `urgency`, `adaptation`, `previousAttempts`.

### DELIVER
**Input:** `packages.json` + the kept packages.
**Does:** builds the packaging board, the feed mock, the first-30-seconds brief, and the production handoff.
**Output:** `delivery/` — board HTML, feed mock, a `BRIEF.md` per kept idea, and the links to the evidence.

### RAILS
**Input:** a cadence (default every three days) and the keeps gate.
**Does:** runs DISCOVER → VALIDATE unattended, writes the ledger, dedupes, and stops. It never writes a keep. It can spawn the agent team (Scout, Frame Reader, Verifier, Crossing Auditor, Critic, Packager) with one artifact per agent.
**Output:** `runs/<date>/ledger.json`, the next-round queue, and a status line for the board.

## 3. The agents

| Agent | Reads | Writes | Rule |
|---|---|---|---|
| **Scout** | seeds, previous ledger, no-go | `candidates.json` | no candidate without a source video and a dated view count |
| **Frame Reader** | candidate IDs | `frames/` + a look description | must look at the actual in-video frames, not the thumbnail |
| **Verifier** | candidates + channel data | scorecard rows | one failed check is enough to demote |
| **Crossing Auditor** | target + exact query | demand / saturation / fit numbers | same wording and period for every target |
| **Critic/Reconciler** | all of the above | `verdicts.json` | cannot be the same agent that proposed the idea |
| **Packager** | kept verdicts | `packages.json` + delivery | title, thumbnail and first 30 seconds must tell the same promise |

A failed agent leaves its artifact missing; the runner resumes from the last complete artifact. Nothing is accumulated in memory only.

## 4. The 3D opportunity space

The board is a real scatter, not a decorative cloud.

**Axes**
- **X — demand:** the target topic’s top-view numbers, same search wording and period for every point. Normalise 0–100.
- **Y — saturation:** how many channels already serve the exact crossing, weighted by whether their copies succeed. 0 = empty, 100 = many successful copies.
- **Z — fit:** can we make it (faceless, 2D-animatable) × does the target audience already watch a close look. 0–100, with the evidence behind it.

**Encoding**
- Point size = freshness (larger = newer).
- Colour = verdict confidence: green = confirmed/open, amber = format only/untested, red = pass/against.
- A **frontier surface** through the high-demand / low-saturation / high-fit region.
- Hover/click: source thumbnail, our title/thumbnail, the proof video, the exact query, the date the numbers were read, the verdict and the contradiction.

**Data schema** (`state.json` → `points[]`)

```json
{
  "id": "you-wouldnt-last-f1",
  "format": "How Long You'd Last in Every [X]",
  "niche": "Formula 1 eras",
  "ourTitle": "How Long You'd Last in Every Era of Formula 1",
  "demand": 72,
  "saturation": 18,
  "fit": 81,
  "freshness": 0.9,
  "verdict": "open",
  "confidence": 0.8,
  "source": {"id": "qrfhhZ-Wvmk", "title": "How Long You'd Last in Every Prehistoric Ocean", "views": 2945558, "checkedAt": "2026-10-22"},
  "proof": {"id": "7ROJfkaewpc", "title": "Evolution of Formula 1 Cars (1950–2026)", "views": 316084},
  "query": "formula 1 history",
  "evidence": ["https://youtu.be/..."],
  "notes": "9 on-topic, 4 over 100K; no F1 video uses the ladder."
}
```

The board reads `state.json`; no separate database. The first version can be a Three.js page served beside the existing format-lab board.

## 5. The rails

- **Cadence:** every three days, 09:00 Europe/Prague. Configurable.
- **Ledger:** every run writes `runs/<date>/ledger.json` with the queries, scopes, limits, errors, dropped candidates and the reason.
- **Dedupe:** a candidate already in a previous round or on the no-go list is skipped, unless the evidence or the wording has changed; the ledger says which.
- **Keeps gate:** the loop stops after VALIDATE. A human (or an explicit `keep` command) writes `keeps.json`; the next ADAPT round only consumes keeps.
- **Failure:** a mode that fails writes a partial artifact and a `blocked` status; the next run resumes from there. No silent retry loop.
- **Survives restarts:** state and artifacts on disk, not in an agent’s context.

## 6. MCP / plugin surface (proposed)

The harness can be a skill first and an MCP second. If exposed as MCP, the tools should be few and stateful:

| Tool | Input | Output |
|---|---|---|
| `niche.status` | — | current run, modes completed, next action, board URL |
| `niche.discover` | seeds?, period? | candidate count + artifact path |
| `niche.validate` | candidate ids | verdicts + evidence |
| `niche.adapt` | kept format ids | packaged ideas |
| `niche.deliver` | package ids | briefs + board |
| `niche.keep` | ids, note | writes `keeps.json` (human gate) |
| `niche.points` | filters | the `points[]` for the 3D board |

Do not expose a single “run everything” tool that can spend money or publish; the gate is explicit.

## 7. Build order

1. **Investigation** — read the skill, the three scripts, the five boards and the nine rounds; write `INVESTIGATION.md` with the real steps, thresholds, errors and lessons.
2. **Skill scaffold** — `skill/SKILL.md` with the four modes, agent contracts and the state schema; thin global pointer.
3. **State + ledger** — `state.json`, `runs/<date>/ledger.json`, a CLI runner that can run one mode at a time.
4. **Discovery/validation runner** — call the existing `yt_scout.py` and `research_round.py`; dedupe; stop at the gate.
5. **3D board** — Three.js scatter from `state.json`; hover evidence; frontier surface.
6. **Adapt/deliver** — packaging board, feed mock, first-30-seconds brief.
7. **Rails** — scheduler + agent spawner; run ledger; restart-safe.
8. **MCP wrapper** — only after the skill and board work locally.

## 8. Existing assets to reuse

- Skill: `../../.agents/skills/niche-bending-youtube-analyzer/` (`yt_scout.py`, `format_lab.py`, `research_round.py`, 9 references).
- Boards: `../format-lab/` (8793), `../tim-danilov-58-niches/` (8792), `../art-of-yt-top-100/` (8797), `../cars-next/` (8794), `history-channel` (8806).
- Rounds: `../format-lab/2026-10-04/`, `../format-lab/2026-10-22/`.
- Keeps: `../format-lab/keeps.json`, `../format-lab/KEEPS-NOTE.md`.
- The existing board styles (`format-lab/index.html`) for the look, not a new design system.
