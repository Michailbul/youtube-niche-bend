---
description: Open the research boards: the 3D opportunity board and the format-lab board
argument-hint: "[3d | lab]"
---

Open the niche-bend boards for this project. Which: $ARGUMENTS (default both).

The plugin folder is `${CLAUDE_PLUGIN_ROOT}` (if that text was not replaced by a path, find it with `ls -d ~/.claude/plugins/cache/*/niche-bend/*/ | tail -1`). Run from the project root, as background processes:
- 3D opportunity board: `python3 <plugin>/skills/niche-bend-harness/harness/board/server.py --by <owner name>` -> http://127.0.0.1:8810.
  If 8810 is taken, add `--port 8811` (or any free port).
  Ask the user which owner is clicking if you do not know; the name signs their keeps.
- Format-lab board: `python3 niche-bend/format-lab/server.py` -> http://127.0.0.1:8793 (fixed port; exists after the first `format_lab.py build` or `/niche-bend:setup`'s examples have been built).
If `niche-bend/` does not exist, run `/niche-bend:setup` first. Open the URLs in the browser pane when one is available,
and give the user the URLs. Then show `nb.py status` in a short summary: points, verdicts, what is kept.
