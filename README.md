# youtube-niche-bend

A Claude Code plugin for our YouTube channel. It carries the method we use to decide what video to make and how
to package it, the scripts that do the research, and the boards we pick ideas on.

**The method in one line:** we never invent a format. Find a small, fresh, faceless channel whose format took off in
the last month, keep the format, swap one thing (subject, universe, country, language). Title and thumbnail first,
video second.

## Install

You need Claude Code, Python 3.9+, and read access to this repo (it is private; your GitHub login in `gh` or git is
enough). In Claude Code:

```
/plugin install niche-bend --marketplace Michailbul/youtube-niche-bend
```

(On Claude Code older than 2.1.275, use two lines: `/plugin marketplace add Michailbul/youtube-niche-bend`, then
`/plugin install niche-bend@youtube-niche-bend`.)

Restart Claude Code, open the project folder you want the research to live in, and run:

```
/niche-bend:setup
```

It checks Python and Pillow, creates a `niche-bend/` folder in the project, copies the no-go list there, loads
Michael's two October 2026 research rounds as 46 example ideas, and smoke-tests the YouTube scout.

Update later with `/plugin marketplace update youtube-niche-bend`.

## What you can say

| Say | What happens |
|---|---|
| `/niche-bend:round` or "what's working this month?" | A research round: title formulas spreading across niches this month, checked sources, bends into niches with demand, a board to pick from |
| `/niche-bend:bend <channel or video>` | Validate a channel, name its format genes, bend it into other niches |
| `/niche-bend:occupied <idea>` | Is someone already doing it, and does it get views? Demand and crowding as two lines, with thumbnails |
| `/niche-bend:idea <subject>` | Idea first: borrow a proven angle, title and thumbnail from other niches |
| `/niche-bend:titles <topic>` | Titles and thumbnails, tested in a YouTube feed mock |
| `/niche-bend:more` | Ten more ideas, nothing already shown or kept |
| `/niche-bend:board` | Open the 3D opportunity board and the format-lab board |
| `/niche-bend:keep <ids>` | The command for a human keep (agents can only propose) |

Plain requests work too ("niche bend this channel", "find the hidden opportunity", "give me 10 more"): the skills
trigger on them.

## What is inside

| Part | What it is |
|---|---|
| `niche-bend` skill | The method: 16 rules, each with Michael's words and the date behind it, what kills an idea, what to do for each kind of request. Start here. `references/setup.md` explains how it runs on your machine. |
| `niche-bending-youtube-analyzer` skill | The research kit: `yt_scout.py` (reads YouTube without an API key: search, channel scorecards, demand, topic size, title formulas, spread, in-video frames), `format_lab.py`, the no-go list, 15 sourced title rules, the independent-check protocol, format families |
| `video-idea-proposals` skill | Turns research into ideas you can say yes or no to; the five title tests; the ideas board and the thumbnail board with the YouTube feed mock |
| `niche-bend-harness` skill (optional) | The research loop as a CLI with a run ledger: discover, validate, keep, adapt, deliver; a 3D board of ideas by demand, crowding and fit; an MCP server |
| Six subagents | `scout`, `frame-reader`, `verifier`, `crossing-auditor`, `critic-reconciler`, `packager`. The rule: whoever proposes an idea never approves it. |

## The rules everything follows

1. Title and thumbnail first, video second.
2. Packaging comes from other niches, never ours.
3. Proven, fresh, small: median of latest uploads at least 50K, more than one hit, channel under 6 months, still posting, under 100K subscribers.
4. Faceless only. Check the frames inside the video; thumbnails lie.
5. Demand and crowding are two separate lines. Best case: both proven, the crossing empty.
6. Test every bend on YouTube (last month, by views) before proposing it.
7. Pick the subject by demand (Formula 1 is about 7 times rally).
8. Tension between two things people already know.
9. Keep the source title's shape: our title sits under theirs.
10. Recognisable but new: take the mechanism, never the palette.
11. Evidence at most a month old, numbers re-read on the day.
12. Three scouts and a critic. The proposer never approves its own idea.
13. Not only cars.
14. Results are pictures: thumbnails, views, frames.
15. An owner's keep is the only gate. Agent picks are proposals.
16. Every piece of feedback becomes a written rule the same day.

The full text with the reasons is in `plugins/niche-bend/skills/niche-bend/SKILL.md`.

## Where your work goes

Everything a round produces lands in `niche-bend/` inside your project: rounds, boards, keeps, the no-go list,
harness state. Commit it to git after each round: the keeps and the no-go list are the method's memory. The plugin
folder itself is replaced on every update, so nothing is ever written there.

The skills mention Michael's laniameda Gallery (his private research database). Without it, everything works on
local boards; see `setup.md`.

## Tests

```
cd plugins/niche-bend/skills/niche-bend-harness/harness && python3 -m unittest discover -s tests -v
```
