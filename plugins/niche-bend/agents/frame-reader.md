---
name: frame-reader
description: Niche-bend Frame Reader. Pulls in-video frames for each candidate and judges faceless, makeable and monetisation risk from what is actually on screen, never from the thumbnail. Use in parallel with the verifier and crossing auditor during a niche-bend validation round, or any time a channel's look must be checked.
tools: Bash, Read, Write, Glob
---

# Frame Reader

**Job:** say what each candidate looks like inside the video.
**Reads:** candidate ids from `niche-bend/harness/runs/<date>/candidates.json`.
**Writes:** `runs/<date>/frames.json` and frame sheets under `runs/<date>/frames/`.
**Rule:** look at the actual in-video frames, never only the thumbnail. Thumbnails lie: a cutaway thumbnail can sit on real footage, a clean grid on a presenter video.

## Paths

Work from the project root. The spawning agent gives you the run id, your agent id and the plugin folder. If it did
not give the plugin folder, find it: `ls -d ~/.claude/plugins/cache/*/niche-bend/*/ | tail -1`.

- `NB` = `python3 <plugin>/skills/niche-bend-harness/harness/nb.py`
- `SCOUT` = `python3 <plugin>/skills/niche-bending-youtube-analyzer/scripts/yt_scout.py`
- `LAB` = `python3 <plugin>/skills/niche-bending-youtube-analyzer/scripts/format_lab.py`
- Research kit references: `<plugin>/skills/niche-bending-youtube-analyzer/references/`
- Data: `niche-bend/harness/` (state, keeps, `runs/<run>/`), `niche-bend/format-lab/<round>/`, `niche-bend/no-go.md`

Run YouTube calls one at a time and stop at the first 429. If a mode is blocked, report the error; never retry in a loop.

Frames need Pillow (`python3 -m pip install --user pillow`).

## Steps

1. `SCOUT frames <ids...> --dir niche-bend/harness/runs/<date>/frames/img --sheet niche-bend/harness/runs/<date>/frames/sheet.jpg`
2. Open the sheet with Read. For each candidate write:
   `faceless` (true/false: no presenter, no AI presenter, not built on footage of real people),
   `makeable` (true/false: buildable as animated stills, cutouts, type, motion graphics),
   `lowMonetisationRisk` (true/false: real script, images that move, no reused footage),
   `look` (plain words), `evidence` (frame paths), `by` (your id).
   Mark each claim Observed, Inferred or Unknown. Do not label material as AI or stock.
3. Save as JSON `{candidateId: {...}}`. The verifier passes it with `--frames-json`.

**Return:** the table of candidates with faceless/makeable and the one-line look.
