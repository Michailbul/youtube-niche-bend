---
description: Run a format-lab research round: what formats are working this month and where else they can go
argument-hint: "[optional focus, e.g. 'history' or 'not cars']"
---

Run a niche-bend format-lab round. Focus from the user: $ARGUMENTS

The plugin folder is `${CLAUDE_PLUGIN_ROOT}` (if that text was not replaced by a path, find it with `ls -d ~/.claude/plugins/cache/*/niche-bend/*/ | tail -1`). Use the `niche-bend` skill (the method and its 16 rules) and the `niche-bending-youtube-analyzer` skill
(`references/format-lab.md` is the routine). Data goes to `niche-bend/` in this project; run `/niche-bend:setup` first if it is missing.

1. Load memory: `niche-bend/no-go.md`, every `keeps.json` under `niche-bend/`, earlier rounds. Never re-propose what was kept or dropped.
2. Format watch: `yt_scout.py formulas`, drop phrases and news bursts, `spread` each survivor (one call at a time).
3. Pick 6 to 8 sources that pass the outlier test, check channels, pull frames, write A/B/C cards.
4. Propose D: three target niches per format (car niches by default; another niche when the user names it), each with our title under the source title.
   Size targets with `compare`. Write `niche-bend/format-lab/<today>/spec.json`, run `format_lab.py check` and `build`.
5. Independent check (rule 12): spawn `niche-bend:frame-reader`, `niche-bend:verifier` and `niche-bend:crossing-auditor`
   in parallel, then `niche-bend:critic-reconciler`. If you cannot run separate agents, leave verdicts Untested and say so.
6. Show the board (`python3 niche-bend/format-lab/server.py`, port 8793) or Gallery cards. Lead with the two or three
   strongest decisions and the strongest objection. Then stop: an owner keeps.
