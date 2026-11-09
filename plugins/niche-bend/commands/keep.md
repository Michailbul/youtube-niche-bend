---
description: How an owner keeps ideas (the human gate): prints the exact command or points to the board
argument-hint: "<idea ids> [note]"
---

The user wants to keep: $ARGUMENTS

The plugin folder is `${CLAUDE_PLUGIN_ROOT}` (if that text was not replaced by a path, find it with `ls -d ~/.claude/plugins/cache/*/niche-bend/*/ | tail -1`). Keeps are a human decision. A keep you write yourself is recorded as a proposal, not a keep, and that is
intended. Do not try to get around it. Instead:
1. Look the ids up with `python3 <plugin>/skills/niche-bend-harness/harness/nb.py points` from the project root and show
   each one's title, verdict and demand / saturation, so the owner sees what they are keeping.
2. Give the owner the command to run in their own terminal, from the project root, as one copy-paste line:
   `python3 <full plugin path>/skills/niche-bend-harness/harness/nb.py keep <ids> --note "<why>" --by <their name>`
   Or tell them to click Keep on the 3D board (`/niche-bend:board`).
3. After they confirm, run `nb.py status` and report the gate.
Format-lab board keeps are clicks on that board and save to `niche-bend/format-lab/keeps.json`.
