---
name: niche-bend-harness
description: Run the niche-bend research loop as one harness. DISCOVER -> VALIDATE -> (keeps gate) -> ADAPT -> DELIVER, plus RAILS for unattended discovery, with a run ledger, a 3D opportunity board and the six research subagents. Use for "run the loop", "update the board", "show the opportunity space", keeping or briefing an idea through nb.py, ingesting a format-lab round, or spawning the research agent team. Optional tool; the method itself is the niche-bend skill.
---

# Niche-bend harness

The machine around the method. The method lives in the `niche-bend` skill (16 rules) and its research kit
`niche-bending-youtube-analyzer` (scorecards, freshness windows, bend/restyle/merge, title rules). Read those
first. This file says how to run the loop. On 22 Oct 2026 Michael kept the harness as an optional tool, not the
method: use it when a round should leave files a killed session can resume from, or when ideas belong on the
3D opportunity board.

## Where things are

- Code (in this skill's folder): `harness/nb.py` (CLI, stdlib only), `harness/mcp_server.py`, `harness/board/`
  (3D board), `harness/tests/`, `harness/examples/format-lab/` (Michael's two October 2026 rounds).
- Data (in your project, never in the plugin): `niche-bend/harness/state.json`, `keeps.json`, `runs/<run>/`;
  rounds in `niche-bend/format-lab/<date>/`; the project's no-go list `niche-bend/no-go.md`.
  Override with `NB_WORK=<folder>` (data root) or `NB_HOME` (harness state only).

Run every command from the **project root**. Below, `NB` means
`python3 <this skill's base directory>/harness/nb.py`.

First time: `NB init --examples` (or `/niche-bend:setup`). It creates the data folder, copies the no-go list
into the project, and ingests the two example rounds: 46 ideas, 42 with all three axes. Safe to re-run.

## The flow

| Mode | Command | Reads | Writes |
|---|---|---|---|
| init | `NB init [--examples]` | plugin no-go list, example rounds | `niche-bend/` folder, own `no-go.md`, `keeps.json` |
| status | `NB status` | state, keeps | run pointer, modes, gate, next action |
| ingest | `NB ingest niche-bend/format-lab/<round>` | lab.json, checks.json, img/ | runs/<round>-ingest/{candidates,verdicts,ledger}.json, state.points |
| DISCOVER | `NB discover [--seeds F] [--top 12] [--recheck W ...] [--dry-run]` | watch_seeds.json, no-go.md, all previous rounds, state | runs/<date>/formulas.json, candidates.json |
| VALIDATE (verifier) | `NB validate [--ids a,b] --verifier ID [--channels-json F] [--frames-json F]` | last complete candidates.json | runs/<run>/verdicts.json, status awaiting-reconciler |
| VALIDATE (reconciler) | `NB validate --reconcile decisions.json --reconciler ID` | verdicts.json | decisions, reconciled points |
| keeps gate | `NB keep <ids> --note "why" --by <owner name>` | state, candidates | keeps.json (the only writer) |
| ADAPT | `NB adapt` | keeps.json (kept only) | runs/<date>/packages.json skeleton |
| DELIVER | `NB deliver` | packages.json, keeps | runs/<run>/delivery/BRIEF-<id>.md |
| board data | `NB points [--json] [--round R] [--verdict V]` | state.points | points[] for the 3D board |
| RAILS | `NB rails [--dry-run]` | as DISCOVER | discover + scorecards, then stops at the gate |

Every command appends to `runs/<run>/ledger.json`: queries, limits, errors, dropped items with the reason,
artifact status. Read it before claiming a run worked.

### Crossing numbers (demand / saturation / fit)

Discovery finds formats; the demand and saturation of each target crossing still come from the format-lab
path: write `niche-bend/format-lab/<round>/spec.json` (shape in the analyzer's `references/format-lab.md`), run
`python3 <analyzer>/scripts/format_lab.py check niche-bend/format-lab/<round>/spec.json` and `build`, then
`NB ingest niche-bend/format-lab/<round>`. How each axis is computed, and what is missing: `references/axes.md`.

## The 3D opportunity board

`python3 <this skill's base directory>/harness/board/server.py --by <owner name>` from the project root, then open
http://127.0.0.1:8810. X = demand, Y = saturation, Z = fit; point size = freshness, colour = verdict confidence.
Hover shows the source thumbnail, our title and the evidence. The Keep button writes a human keep signed with
the `--by` name (default `NB_OWNER`, then the login name). Until `state.json` exists it shows sample data, and
sample points cannot be kept.

## Rules the CLI enforces

1. **Keeps gate.** `keep` is the only writer of `keeps.json`. A call from a terminal with no `NB_AGENT` set is a
   human keep (`kept`), and so is a click on the board. Any other call is recorded as `proposed`. An agent never
   overwrites a human keep. ADAPT and DELIVER read `kept` only. Agents set `NB_AGENT=<their id>` before calling
   nb.py. Either channel owner may keep; `--by` records which one.
2. **No self-certification.** The verifier can not be the proposer. The reconciler can not be the proposer
   or the verifier. The CLI refuses (exit 2). This is the rule in the analyzer's `references/cross-verification.md`.
3. **One failed check demotes.** Unknown checks (faceless, makeable, monetisation before the Frame Reader)
   keep a source Untested. Proven needs every check true.
4. **Missing numbers stay null** with the reason in `axes` and in the ledger `missing` list.
5. **Failures stop.** A failed mode writes `blocked` with the error. No retry loop. Fix the cause, run the
   mode again; it resumes from the last complete artifact.
6. **Dated numbers.** Every point carries `source.checkedAt`, `query` and `axes.readOn`.
7. No paid APIs from the harness. yt_scout reads public pages and RSS. One YouTube call at a time; stop at
   the first 429.
8. Never copy evidence images into runs/. Points reference `niche-bend/format-lab/<round>/img/<id>.jpg`
   or `https://i.ytimg.com/vi/<id>/hqdefault.jpg`.

## The agent team

The plugin ships the six roles as Claude Code subagents (`agents/` in the plugin). Each writes one artifact.

| Agent | Writes |
|---|---|
| `scout` | runs/<date>/candidates.json (via nb.py discover) |
| `frame-reader` | runs/<date>/frames.json + frame sheets |
| `verifier` | verdicts.json scorecard rows (via nb.py validate) |
| `crossing-auditor` | niche-bend/format-lab/<round>/spec.json + checks.json, then nb.py ingest |
| `critic-reconciler` | runs/<date>/decisions.json, then nb.py validate --reconcile |
| `packager` | fills packages.json, then nb.py deliver |

Order: scout -> frame-reader + verifier + crossing-auditor (in parallel, none sees another's verdict) ->
critic-reconciler -> **an owner keeps** -> packager.

### Spawning

Use the Agent tool with the role as `subagent_type` (for example `niche-bend:scout`). Give each one the run id,
a distinct agent id (`scout-1`, `verifier-1` …: the CLI checks them), the project root, and how to verify
(`NB status`, the ledger). Spawn the three checkers in one message so they run in parallel; spawn the
reconciler only after all three return. If only one agent is available, say so in the ledger note and leave
verdicts Untested. Four headings in one agent is not independent verification.

## Rails

`NB rails` runs DISCOVER then the mechanical scorecard and stops with status `stopped at keeps gate`.
It never keeps, adapts or publishes. A schedule is the owners' decision; Michael proposed every three days at
09:00 Europe/Prague and has not approved it. If the owners want one, use Claude Code's scheduled tasks (`/schedule`)
or cron, and keep the gate. After rails, spawn frame-reader, crossing-auditor and critic-reconciler on the new
candidates.

## MCP server (optional)

`python3 <this skill's base directory>/harness/mcp_server.py`, started from the project root. Stdlib,
JSON-RPC over stdio. It never calls YouTube, a paid API or a scheduler, and never runs a mode. To use it, add it
to the project's `.mcp.json` with the absolute path. The skill and CLI are enough without it.

| Tool | Returns | Rule |
|---|---|---|
| niche_status | `nb.py status` JSON | read-only |
| niche_points | `nb.py points --json` (optional `verdict`, `round`) | read-only |
| niche_keep | `nb.py keep` result | refused unless the server was started with `NB_HUMAN=1`; even then nb.py records a proposal (no terminal). Owners keep in a terminal or on the board. |
| niche_discover / niche_validate / niche_adapt / niche_deliver | the exact nb.py command + current mode status | does not run the mode |

Tests: `cd <this skill's base directory>/harness && python3 -m unittest discover -s tests -v` (19 tests).

## Starting state (example rounds)

- Rounds 2026-10-04 and 2026-10-22 (Michael's car-channel research): 46 points, 42 with all three axes.
- No verdict is reconciled: both rounds were written by one agent. Confidence carries a 0.75 factor for that.
- Nothing is kept. In Michael's own setup the round-1 agent triage stayed a proposal and round 2 was undecided.

## Links

- Method: the `niche-bend` skill; setup: its `references/setup.md`
- Research kit: the `niche-bending-youtube-analyzer` skill and its references (`format-lab.md`,
  `cross-verification.md`, `no-go.md`, `title-psychology.md`, `format-families.md`)
- Design and history: `references/SPEC.md`, `references/INVESTIGATION.md` (real steps, thresholds, 18 failure
  modes, 17 lessons; written on Michael's machine, so its paths are his)
- Axes: `references/axes.md`
