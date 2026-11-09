---
description: Set up niche-bend in this project: data folder, no-go list, example rounds, dependency check
---

Set up the niche-bend plugin for this project. The plugin folder is `${CLAUDE_PLUGIN_ROOT}` (if that text was not replaced by a path, find it with `ls -d ~/.claude/plugins/cache/*/niche-bend/*/ | tail -1`).

1. Read `<plugin>/skills/niche-bend/references/setup.md`.
2. Check `python3 --version` (3.9+) and `python3 -c "import PIL"`. If Pillow is missing, install it with
   `python3 -m pip install --user pillow` (frames and contact sheets need it). On macOS also try
   `python3 -m pip install --user certifi`.
3. From the project root run `python3 <plugin>/skills/niche-bend-harness/harness/nb.py init --examples`.
   It creates `niche-bend/` (harness state, format-lab, the project's own `no-go.md`) and loads Michael's two
   October 2026 rounds as 46 scored example ideas. It never overwrites existing data.
4. Smoke-test the scout: `python3 <plugin>/skills/niche-bending-youtube-analyzer/scripts/yt_scout.py search "every _ explained" --period month --sort views --table`
   and show the first five rows.
5. Check whether the laniameda Gallery MCP tools are connected (`list_video_refs`). Say which output path this
   project will use: Gallery, or local boards plus `niche-bend/library.json`.
6. If the project is a git repo, suggest committing `niche-bend/` (without `img/` folders).

Report what was created, what is missing, and the three commands to try next: `/niche-bend:round`, `/niche-bend:bend <channel>`, `/niche-bend:board`.
