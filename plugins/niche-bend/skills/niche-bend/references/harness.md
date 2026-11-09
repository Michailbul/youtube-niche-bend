# The harness: niche bending as a runnable loop

An optional tool. The method is the 16 rules in `SKILL.md`; on 22 Oct Michael dropped the harness *as the method* and kept it as a tool (`decisions.md`). Use it when a round should leave files a killed session can resume from, or when points belong on the 3D opportunity board. The full evidence (every step, threshold, error, with file and session line numbers) is the harness skill's `references/INVESTIGATION.md`. This page is the short version.

## Where the code lives

In this plugin: the `niche-bend-harness` skill. Code in its `harness/` folder, data in your project's `niche-bend/` folder (the plugin folder is replaced on every update).

| Thing | Path |
|---|---|
| CLI runner, stdlib only | `<niche-bend-harness>/harness/nb.py` (below: `nb.py`) |
| MCP stdio server | `<niche-bend-harness>/harness/mcp_server.py` |
| 3D opportunity board | `<niche-bend-harness>/harness/board/server.py --by <name>` (port 8810), or `/niche-bend:board` |
| Agent briefs | the plugin's subagents: `scout`, `frame-reader`, `verifier`, `crossing-auditor`, `critic-reconciler`, `packager` |
| How each axis is computed | `<niche-bend-harness>/references/axes.md` |
| Evidence and lessons | `<niche-bend-harness>/references/INVESTIGATION.md` |
| Tests | `<niche-bend-harness>/harness/tests/` (19) |
| Run state (points, mode status, run pointer) | `niche-bend/harness/state.json` (project) |
| Keeps gate | `niche-bend/harness/keeps.json` (project) |
| Run ledgers and artifacts | `niche-bend/harness/runs/<run>/` (project) |

## The four modes and rails

Every command appends to `runs/<run>/ledger.json`: queries, limits, errors, what was dropped and why, artifact status. Read the ledger before saying a run worked.

| Mode | Command (from the project root) | Reads | Writes |
|---|---|---|---|
| status | `nb.py status` | state, keeps | nothing (prints JSON) |
| ingest | `nb.py ingest niche-bend/format-lab/<round>` | the round's `lab.json`, `checks.json` | `runs/<round>-ingest/`, `state.points` |
| **DISCOVER** | `nb.py discover --dry-run`, then `nb.py discover [--seeds F] [--top 12] [--recheck W …]` | `watch_seeds.json`, `no-go.md`, every earlier round | `runs/<date>/formulas.json`, `candidates.json` |
| **VALIDATE** (verifier) | `nb.py validate [--ids a,b] --verifier <id> [--channels-json F] [--frames-json F]` | last complete `candidates.json` | `verdicts.json`, status `awaiting-reconciler` |
| **VALIDATE** (reconciler) | `nb.py validate --reconcile decisions.json --reconciler <id>` | `verdicts.json` | reconciled verdicts |
| keeps gate | `nb.py keep <ids> --note "why" --by <owner>` | state, candidates | `keeps.json` |
| **ADAPT** | `nb.py adapt` | `keeps.json`, status `kept` only | `runs/<date>/packages.json` skeleton |
| **DELIVER** | `nb.py deliver` | `packages.json`, keeps | `runs/<run>/delivery/BRIEF-<id>.md` |
| board data | `nb.py points --json [--round R] [--verdict V]` | `state.points` | nothing (prints `points[]`) |
| **RAILS** | `nb.py rails --dry-run` | as DISCOVER | discover + scorecards, then stops at the gate |

DISCOVER, VALIDATE with channel reads, and RAILS call YouTube through `yt_scout.py`. Run the dry run first. The crossing numbers for each target still come from the format-lab path: write `<round>/spec.json`, run `format_lab.py check` and `build`, then `nb.py ingest`.

Rails proposes a cadence of every three days at 09:00 Europe/Prague. **Nobody has approved it. The plugin installs no scheduler**; the owners decide. Rails never keeps, adapts or publishes.

## Six agents, one artifact each

`Scout → Frame Reader + Verifier + Crossing Auditor (in parallel, blind to each other) → Critic/Reconciler → an owner keeps → Packager`

| Agent | Writes |
|---|---|
| Scout | `candidates.json`, through `nb.py discover` |
| Frame Reader | `frames.json` + frame sheets. Faceless and makeable are frame judgments; no script computes them. |
| Verifier | scorecard rows in `verdicts.json`, through `nb.py validate --verifier` |
| Crossing Auditor | `spec.json` + `checks.json` through `format_lab.py`, then `nb.py ingest` |
| Critic/Reconciler | `decisions.json`, then `nb.py validate --reconcile` |
| Packager | fills `packages.json` for kept ids, then `nb.py deliver` |

**The proposer never certifies its own idea.** `nb.py` refuses (exit 2) when the verifier is the proposer, or the reconciler is the proposer or the verifier. Give every agent a distinct id. If only one agent is available, write that in the ledger and leave the verdict Untested: four headings in one agent is not independent verification. Where an independent critic did run (Unknown Frequencies, 9 Oct; opportunities, 12 Oct) it overturned the proposer both times.

## The keeps gate

- Only an owner keeps (Michael or Stas; `--by` records which). An agent's pick is a **proposal**, stored with status `proposed`, and never counts.
- `nb.py keep` is the only writer of `keeps.json`. A call from a real terminal, or a click on the 3D board (per-start token the agents never see), records `kept`. Anything with `NB_AGENT` set, or with no terminal, records `proposed`.
- Every entry carries `by`, `at`, `note` and how it arrived. A proposal never overwrites a human keep.
- ADAPT and DELIVER read `kept` only. In Michael's October rounds nothing was kept; six ids from the 21 Oct round-1 triage were agent proposals.

## Failure modes as rules

From the 18 failures in the harness skill's `references/INVESTIGATION.md` §4.

1. **Write a file before the next step starts.** Server restarts and usage limits killed sessions mid-plan; resume from the last complete artifact.
2. **A round without a keep is unjudged, not approved.** Show the queue age at the gate (round 1 waited 17 days).
3. **Agent picks are proposals.** The round-1 triage was written straight into `keeps.json` once; never again.
4. **Keeps carry an author and are never replaced wholesale.** The old board's `POST /save` replaced the file; a merge listed in `KEEPS-NOTE.md` vanished from `keeps.json`, and reloads lost clicks.
5. **Generated board files must not clobber the server.** `format_lab.py build` overwrote `server.py` and broke routing. Generated and hand-edited files live apart.
6. **Empty is not zero.** `yt_scout.py` turns a 429 into an empty list with exit 0. Each query records ok / empty / error; a run with errors is `partial`.
7. **No parallel YouTube calls. Stop at the first 429.** A parallel `spread` loop wrote six empty files; the sequential rerun worked.
8. **The proposer's verdict is `proposedVerdict`.** Only a separate critic writes the verdict. 8 of 12 "Open" targets in round 2 had a contested or crowded script reading.
9. **Resolve paths from the repo root.** 34 stale `/Users/michael/…` paths broke launches.
10. **One port registry.** The Danilov board moved to 8792 because 8791 was taken.
11. **Research outside git has no history.** Commit the project's `niche-bend/` (keeps, no-go, rounds) after each round; on Michael's repo it was gitignored and 3,600 images had to be re-fetched.
12. **Reference images by path, never copy them.** The snapshot folder reached 69 GB.
13. **Stop cleanly with a partial artifact** when a usage limit hits.
14. **Re-check a channel before reuse.** Two had been deleted by 21 Oct.
15. **Numbers carry their query and date.** CityEons read 1.41K subscribers on 12 Oct and 3,100 on 21 Oct. Every point stores `query`, `source.checkedAt`, `axes.readOn`.
16. **A flag needs n ≥ 3.** `notOneHit` came out true for a channel with one video.
17. **Rank target niches by evidence.** Car niches by default (9 Nov 2026); another niche when the request names it.
18. **Saturation is title-matched.** The script's topic reading and the exact crossing measure different things; the `cross` list is an unmatched search and is not used in the number.

Missing numbers stay `null` with a reason. A failed mode writes `blocked` with the error and does not retry in a loop.

## MCP server

One command, from the project root: `python3 <niche-bend-harness>/harness/mcp_server.py`. Stdlib, JSON-RPC over stdio (`initialize`, `tools/list`, `tools/call`). It does not call YouTube, a paid API or `launchd`, and it does not run a mode.

| Tool | Input | Returns | Rule |
|---|---|---|---|
| `niche_status` | none | `nb.py status` JSON: run, modes, points, gate, next action | read-only |
| `niche_points` | `verdict?`, `round?` | `nb.py points --json`: `points[]` for the 3D board | read-only |
| `niche_keep` | `ids`, `note`, `by` | `nb.py keep` result | **Refused** unless the server was started with `NB_HUMAN=1`. Even then nb.py decides: over stdio there is no terminal, so the entry is a proposal. Owners keep in a terminal or on the board. |
| `niche_discover` | none | the exact `nb.py discover` commands + mode status | does not run; DISCOVER calls YouTube |
| `niche_validate` | none | the verifier and reconciler commands + mode status | does not run |
| `niche_adapt` | none | `nb.py adapt` + mode status | does not run; needs a human keep |
| `niche_deliver` | none | `nb.py deliver` + mode status | does not run |

There is no "run everything" tool, and none that spends money or publishes.

## Tests

`cd <niche-bend-harness>/harness && python3 -m unittest discover -s tests -v` (19 tests). Every test works in a temp data folder; the bundled example rounds are read, never written.
