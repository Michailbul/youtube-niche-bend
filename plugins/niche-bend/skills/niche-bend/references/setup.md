# Running the niche-bend plugin

Read this once on a new machine. Every skill in this plugin was written while Michael ran the research on his own setup (an iMac, the laniameda Gallery, his agent fleet). The plugin works without any of that; this page says how.

## Who decides

The channel has **owners**: Michael and his co-owner. Wherever a rule says "Michael keeps", "Michael's keep is the only gate" or "show Michael", read **an owner**. Either owner's keep counts, and every keep records who made it (`--by <name>` in the harness, the name on the board). Agent picks stay proposals.

Michael's quotes in `michael-said.md`, `decisions.md` and `how-we-got-here.md` stay as he said them. They are the history behind each rule. When the co-owner gives feedback, rule 16 still applies: write it down the same day, with his name and the date.

## Where the work goes

All research data lives in the project you run Claude Code from, in one folder:

```
<your project>/niche-bend/
  no-go.md                 your living no-go list (copied from the plugin on first setup, then grows)
  format-lab/<date>/       one research round: spec.json, checks.json, lab.json, img/
  format-lab/index.html    the format-lab board (written by format_lab.py build)
  format-lab/keeps.json    keeps clicked on that board
  harness/                 optional harness: state.json, keeps.json, runs/<run>/
  research/rounds/         raw collections from research_round.py
  <slug>/                  idea boards and thumbnail boards for kept ideas
```

Create it with `/niche-bend:setup`, or run `python3 <plugin>/skills/niche-bend-harness/harness/nb.py init --examples` from the project root. `--examples` loads Michael's two October 2026 rounds (46 scored ideas), so the boards are not empty on day one. Put the project in git and commit `niche-bend/` after each round: the keeps and the no-go list are the memory of the method. Setup writes `niche-bend/.gitignore` so images and the board's per-start secret stay out of git.

Never write research data into the plugin folder. Plugin updates replace it.

**Paths in the skill text.** `niche-bend/...` means the project data folder above. `scripts/...`, `references/...` and `assets/...` mean the folder of the skill you are reading (Claude Code shows it as the skill's base directory when the skill loads). A path that names `.agents/skills/...` or `.claude/skills/...` means the same skill inside this plugin. Folders named in worked examples (`niche-bend/tim-danilov-58-niches/`, `2d-animations/...`, `art-of-yt-top-100/`) are from Michael's machine and are not shipped; the lessons from them are already written into the skills.

## With or without the laniameda Gallery

The skills say "save to the Gallery", "the Gallery `/youtube` dashboard", "`youtube-niche-bend` label". That is Michael's private database, reached through the `laniameda-gallery` MCP server.

- **Gallery connected** (the MCP tools `list_video_refs`, `save_video_refs` answer): follow the skills as written.
- **No Gallery**: everything goes to local HTML boards in `niche-bend/`, and keeps go to `keeps.json` beside each board:
  - research round → the **format-lab board** (`format_lab.py build`, served by `niche-bend/format-lab/server.py` on port 8793);
  - proposals → the **ideas board** (`video-idea-proposals/assets/ideas-board/`);
  - a kept idea's packaging → the **thumbnail board with the YouTube feed mock** (`video-idea-proposals/assets/thumb-board/`);
  - the harness's scored ideas → the **3D opportunity board** (`/niche-bend:board`).
  The "packaging library" (titles and thumbnails that work) becomes `niche-bend/library.json`: one record per video with the same fields the skills list for a Gallery save (`titlePattern`, `thumbnailPattern`, `format`, `whyItWorks`, `checkedAt` …). Read it before searching YouTube, the way the skills say to read the Gallery.

## What you need

| Need | Why | Check |
|---|---|---|
| Python 3.9+ | every script | `python3 --version` |
| Pillow | contact sheets and in-video frames (`yt_scout.py sheet`, `frames`, `styles`) | `python3 -m pip install --user pillow` |
| certifi (macOS, optional) | HTTPS certificates for python.org builds; the scripts fall back to the system bundle | `python3 -m pip install --user certifi` |
| A browser pane or Chrome control (optional) | Google Trends, a channel's Oldest tab, reading frames at full size | Claude Code's browser tools |
| Subagents | the independent check (rule 12): three scouts and a critic | the plugin ships them: `scout`, `frame-reader`, `verifier`, `crossing-auditor`, `critic-reconciler`, `packager` |

No API key is needed. `yt_scout.py` reads public YouTube pages and RSS. YouTube answers 429 after a few hundred reads from one IP: run searches one at a time and stop at the first 429.

Optional connectors the skills mention: vidIQ (keyword volume), `theartofyt` (paid packaging data), Supadata (transcripts, for analysing someone else's "niches" video). Use them when they are connected; when not, say so once and carry on.

## Only on Michael's setup

These parts describe his machines and stay as reference: the paused cloud schedule in `automatic-research.md` and `cloud-research-prompt.md`, OpenClaw and `cc-task` agent spawning, launch configs and preview ports, and the Gallery collections named `channel-europe-self-sabotage` and `youtube-style-map`. Do not try to recreate them; use the plugin's subagents and local boards.
