---
name: niche-bend
description: Michael's niche-bending method, how the channel decides what YouTube video to make and how to package it. Entry point for "niche bend this", "is this format occupied", "find a niche / hidden opportunity", "what video should we make", "give me 10 more ideas", "title and thumbnail for X", "research competitors", "I have an idea for a video", 3D timelapse topics, or any new-format research for the explainers / animation-yt channels. Read before any YouTube research or idea round.
---

# Niche bend: how Michael decides what to make

This skill carries Michael's decisions as rules. His words behind every rule: `references/michael-said.md`. What he kept and dropped, and why: `references/decisions.md`. First time on a machine: read `references/setup.md` (who keeps, the `niche-bend/` data folder in your project, Gallery or local boards, what to install). The tools sit in two working skills of this plugin:
- `niche-bending-youtube-analyzer`: research scripts (`scripts/yt_scout.py`, `format_lab.py`) and references (no-go, title psychology, cross-verification, format lab, format families, Danilov method).
- `video-idea-proposals`: the proposal board and the feedback history (`references/how-we-got-here.md`).

## The method in one line
We never invent a format. Find a small, fresh, faceless channel whose format took off in the last month, keep the format, swap one variable (subject, universe, country, language). Our niche is cars unless the request says otherwise. Packaging comes first and comes from other niches. Video second.

## The rules
| # | Rule | Set |
|---|---|---|
| 1 | **Title and thumbnail first, video second.** Start every idea from packaging that is winning now, then readapt it. | 4 Oct, 21 Oct |
| 2 | **Packaging comes from other niches, never ours.** The served market is not the target; be first to bring a proven package to our audience. An old story is fine under new packaging. | 4 Oct |
| 3 | **Proven, fresh, small.** Median of latest uploads ≥ 50K, more than one hit, channel under 6 months, still posting, under 100K subscribers. Judge by the median, never one viral video. A 17K video is "a very low amount of views". | 3–9 Oct |
| 4 | **Faceless only.** No presenter, AI presenter, podcaster or footage of real people, even as demand evidence. Check the frames; lists and thumbnails lie. | 3 Oct, 9 Oct |
| 5 | **Not occupied, not overwhelmed, has views.** Demand and saturation are two separate lines with linked thumbnails. Best case: both proven, crossing empty. Many unwatched uploads mean the packaging failed, not that the niche is full. | 4 Oct, 21–22 Oct |
| 6 | **Test every bend before proposing it.** Search it, last month, sorted by views. No views: drop it. A dead crossing (someone tried, nobody watched) goes to no-go. | 4 Oct |
| 7 | **Pick the subject by demand.** Bigger subjects first when the crossing is open (F1 ≈ 7× rally). Rank candidates with `yt_scout.py compare`. | 4 Oct |
| 8 | **Tension between two things people know.** Every noun a name or status the viewer already cares about, the two sides contradict, and it is human. Strong words name a human quality or an extreme. If few people know the subject, tie it to something they do know. | 4 Oct, 21 Oct |
| 9 | **Keep the source's shape.** Our title sits under the source title: same word order, length, capitals, punctuation; unchecked facts in [brackets]. Say why the source worked first; drop the bend if ours loses it. | 4 Oct |
| 10 | **Recognisable but novel.** Slightly modify the style so that audience still recognises it, yet it feels new. Take the mechanism, never the palette or typeface. | 21 Oct |
| 11 | **Fresh evidence.** Sources for titles and angles at most 1 month old, reference channels at most 6 months; numbers re-checked on the day. Old 3D hits count only as labelled historical evidence. | 4 Oct, 12 Oct |
| 12 | **Independent check.** Three scouts work separately; a fourth critic reconciles. The proposer never certifies its own idea. Observed, Inferred and Unknown stay apart. | 5 Oct |
| 13 | **Cars by default.** Our channel's niche is cars: every target niche is a car niche (Formula 1, rally, Le Mans, brands, engines, design …) unless the request names another one. When it does (history, Warhammer, Middle-earth, Star Wars), bend there. Packaging still comes from other niches (rule 2). | 19 Oct, 9 Nov |
| 14 | **Images are the result.** Thumbnails, titles, views and frames from inside each video. Text piles and raw Markdown are unusable. | 4 Oct, 12 Oct |
| 15 | **An owner's keep is the only gate.** Michael or Stas clicks what they like; unclicked is dropped. Never show an owner something already kept. Agent picks are proposals. Every keep records who kept it. | 4 Oct, 19 Oct |
| 16 | **Every piece of feedback becomes a written rule the same day,** in this skill, `no-go.md` or the project CLAUDE.md, with the example that caused it. | 4 Oct |

## The run
1. **Load memory.** Read `niche-bend/no-go.md` (the project's copy; the plugin's `niche-bending-youtube-analyzer/references/no-go.md` until setup made one), the latest keeps (`niche-bend/format-lab/keeps.json`, `niche-bend/harness/keeps.json`, the Gallery `youtube-niche-bend` label when it is connected) and the last rounds in `niche-bend/format-lab/`. Exclude anything already kept or dropped.
2. **Find.** Pick the entry that matches the request (table below). Discovery: `yt_scout.py formulas` (title formulas shared across this month), `spread` (new, established or past peak), search this month sorted by views, formula gaps (`every _ explained`). Query the packaging library (Gallery, or `niche-bend/library.json` without it) before YouTube.
3. **Validate.** Scorecard per channel with today's numbers (rule 3, 4). Verdict: **Proven**, **Format only** or **Pass**.
4. **Bend.** Change one variable. Rank subjects by demand (rule 7). Test the bend on YouTube (rule 6). Run the three scouts and the critic (`cross-verification.md`).
5. **Package.** One **format card** per find: **A** thumbnail and title, **B** its niche, **C** the format (how it is built, what is on screen), **D** other niches it fits, each with our title. Source packaging beside ours, tension test, urgency (news peg, live season, evergreen), why the source worked, demand and saturation lines with thumbnails.
6. **Show.** A local board (format-lab or ideas board) or Gallery cards: thumbnails at feed size, titles, views, dates, many chronological inside frames, the channel's top three recent videos. Lead with two or three ranked decisions and the strongest objection. Then stop: **an owner keeps.**
7. **After a keep.** Design the thumbnail and title inside a YouTube feed mock next to real videos. Only then propose style alternatives. The kept idea goes to production (script, voiceover, visual DNA, scouting, first 60 s).
8. **Write it down.** Keeps, drops and the owner's words go into `niche-bend/no-go.md` and the project's decision log the same day (Michael's history is in `references/decisions.md` and `references/michael-said.md`; add new lines there only in your own fork of the plugin).

## What an owner asks → what to do
| They say | Do |
|---|---|
| "niche bend this <url / channel>" | Validate the source (rule 3, 4), name its format genes (title formula, thumbnail layout, structure, look), find recent faceless channels on the same format and their niches, then bend into niches that have demand and an empty crossing. Format cards. |
| "is it occupied?" / "find if people already do this" | Search exact crossing and close variants, last months only, faceless only. Report who sits there with thumbnails and views, and any dead attempts. |
| "find the hidden opportunity" | Format-first discovery (step 2) across niches; the style may change. |
| "I have an idea: X" | Idea first: hunt other niches for the proven angle, title and thumbnail to carry X; check demand and occupancy. |
| "give me 10 more" | Same filters, nothing already shown or kept. |
| "title and thumbnail for this video" | Rules 1, 8, 9: source packaging from another niche, tension test, feed mock. |
| "open the researches we did" | Show past rounds visually (boards, Gallery), not production projects. |

## What kills an idea
A presenter or real people on screen · a channel over 100K subscribers or one viral hit as proof · a bend with no views last month · a crossing already tried with no views (see no-go) · a description where a famous name should be · a title without tension · a format older than its freshness window · gaming-knowledge or celebrity-footage channels as models · Shorts-only sources.

## Formats he pointed at (Warhammer round, 9 Oct)
Labelled grid on a white ground ("The Entire Map of … Explained"), "Your life as …" in drawn characters ("this is what I'm talking about"), the crossover "What if [faction] were in [universe]?", "Every [variant] explained", "Timeline explained", the 3D true-scale reveal, and the 3D timelapse of a place through its history (King's Landing, Middle-earth, Carthage).

## Where things live
- **Research data:** `niche-bend/` in the project you work in (`references/setup.md`). Rounds in `niche-bend/format-lab/<date>/`, the project's no-go list in `niche-bend/no-go.md`, idea and thumbnail boards in `niche-bend/<slug>/`. Create it with `/niche-bend:setup`.
- **Gallery (optional):** Michael's `/youtube` dashboard, labels `youtube-niche-bend`, `reference-packaging` …; tools `list_video_refs`, `save_video_refs`. Without it, use the local boards and `niche-bend/library.json`.
- **Scripts:** `yt_scout.py`, `format_lab.py`, `research_round.py` in `niche-bending-youtube-analyzer/scripts/`; `evidence.py`, `wiki_views.py` in `video-idea-proposals/scripts/`. No API key. Install Pillow for frames and sheets.
- **Subagents:** `scout`, `frame-reader`, `verifier`, `crossing-auditor`, `critic-reconciler`, `packager` (this plugin's `agents/`). Use them for rule 12: separate agents, never one agent writing four headings.
- **Harness (optional):** the `niche-bend-harness` skill (nb.py, 3D opportunity board, MCP server). It is a tool, not the method: modes, agents, keeps gate, failure rules and commands in `references/harness.md`.
- **Explainer video:** `video/niche-bend-explained-v1.mp4`, a short film of this method. `index.html` is a readable page of the three skills as Michael wrote them on 22 Oct 2026 (before this plugin's setup notes).
