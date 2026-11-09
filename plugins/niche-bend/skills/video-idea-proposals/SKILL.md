---
name: video-idea-proposals
description: Propose target niches and concrete titles for our faceless animated YouTube channels, with independently checked audience demand, visual fit, competition and packaging evidence in the existing Laniameda Gallery. Then develop the thumbnail and title of a kept idea at feed size. Use this whenever Michael asks what to make next, wants video ideas or angles for a subject or niche, wants ideas "from other niches", wants a title or thumbnail proposed, improved or tested, says "propose ideas", "more ideas", "brainstorm the next video", "design the thumbnail", "how would it look in the feed", or gives feedback on a proposed title or idea. It carries the proposal structure and Michael's rules for tension, recognisable names, urgency, source lineage and visible evidence, even for a quick brainstorm.
---

# Video idea proposals

This skill is the proposal step: turning research into a short list of videos Michael can say yes or no to, and then into a thumbnail and title he can judge at feed size. It was built on 4 Oct 2026 from one working session on the car channel; `references/how-we-got-here.md` has the full record of what was tried, what Michael rejected and why. Read it once before your first round.

The research engine is the sister skill **`niche-bending-youtube-analyzer`** (search, channel checks, demand, frames, the gallery library). This skill decides what is proposed in the existing Gallery and how it is written.

**Running it:** owners, the `niche-bend/` data folder and Gallery-or-local-boards are in the `niche-bend` skill's `references/setup.md`. Where this file says Michael, read "an owner". Where it says "existing Gallery" and the Gallery MCP is not connected, use the local ideas board and thumbnail board described at the end ("Local boards").

When an owner takes a kept idea into video production, read [video production phases](references/video-production.md). Follow the script approval and critic gates, voiceover, visual-DNA branch, scouting and first-minute V1 approval. A kept idea or packaging approval does not approve its script.

## Target niches and independent review · 5 October 2026

Read the analyzer's `references/cross-verification.md` for every new proposal. A source hit establishes a source opportunity; it does not establish that the same style or title will work in a new target niche. Propose **both a target niche and an actual title**, not just a source channel or a broad topic. Name the target language and narrower viewer intent, distinguishing observed targeting from inferred audience characteristics.

Each surviving crossing needs three independent scouts: (1) topic demand and urgency, (2) target-video visual conventions and transferable style, (3) exact-crossing competition and earlier attempts. A fourth independent critical reconciler checks their evidence and contradictions. Schedule independent work in waves when concurrency is limited; the proposer cannot approve its own research. Scouts receive the hypothesis and shared scope, not a predetermined green verdict.

Collect **8–12 on-topic longform target videos across 3–5 channels**. Show each surveyed channel's top three fitting recent videos with titles, thumbnails, dated views and chronological frame sequences. The analytical sample may overlap these strips. Inspect the actual target niche: bending a fitness format into women-focused yoga requires watching yoga videos, inspecting their thumbnails and hooks, and checking practice versus explanation intent. Do not infer gender, age, country, retention or click-through rate from views or a channel name.

Small-channel performance can establish emerging proof under the analyzer's rules. Large channels and presenter videos can establish topic demand, competition or audience conventions; they cannot establish that a small faceless 2D channel succeeds in that crossing. Label style and audience fit **Observed / Inferred / Unknown**, backed by frame timestamps. Do not write inferred AI-versus-stock or model-provenance labels.

Log wording, language, topic, format, duration and month/year windows, sort, provider, limits/pagination, check time, exclusions and errors. Compare samples under the same scopes. Search-result counts are sampled coverage, not market share, a census or search volume. Show successful and low-performing comparable attempts; their age, channel baseline and evidence limits matter. An empty crossing is **Untested**, not automatically promising. Missing evidence stays **Unknown/Untested**; negative comparable evidence means **Weak/reject** until the adaptation explains the failure credibly.

Every card links source lineage, target survey, competing and failed attempts, scout findings and the reconciler verdict. It names the thumbnail arrangement, animation/video format, source and target hook, a timed first-30-second draft, concrete adaptations and dated urgency evidence or explicitly evergreen status. The Gallery summary does not replace the complete linked survey.

Use the existing channel/project collection for our own ideas, drafts, facts, scripts and reusable references. `channel-europe-self-sabotage` is a configured **research collection**, verified by creation and readback; this does not mean a channel is launched or has an established audience. Associate reused sources with that collection and their roles: `reference-packaging`, `reference-hook`, `reference-format`, `reference-style`, `reference-facts`, `reference-script`. Keep global research collections reusable. Use existing Gallery UI only; do not build a new board, redesign it or invent schema fields.

New Gallery proposal payloads include the supported fields `audienceFit` (verdict `Supported|Partial|Unknown|Mismatch`, summary and up to three featured evidence links), `adaptation` (concrete instructions), and `previousAttempts` (summary and up to three featured evidence links). Add `urgencyEvidence` (summary and HTTPS URL) for a live or seasonal peg. The three-link limit is a compact summary limit, not permission to omit the 8–12-video survey. Link the full source records and scout/query reports. Older stored cards remain readable; required new evidence applies to new research and proposals.

The recurring research remains cloud-requested, every three days at 09:00 Europe/Prague, **PAUSED**. Cloud execution is still unconfigured and unverified. The five-credit per-run cap is shared across all agents; never spend five per scout.

## The idea in one paragraph

We start from the title and the thumbnail. We inspect this month's successful packaging in other niches and test whether one of our stories fits its sentence and composition. Reframing a familiar story may offer a useful crossing, but that is a hypothesis until target evidence supports it. Every proposal shows the source packaging, our version written as close to it as the facts allow, and separate evidence for topic demand, visual fit and existing comparable attempts. Public views do not prove that the source packaging caused its success.

## The workflow

1. **Read the standing rules**: the analyzer's `references/no-go.md`, `references/title-psychology.md`, `references/cross-verification.md`, and the latest Gallery feedback for this subject. Read historical `keeps.json` only if needed for prior decisions.
2. **Pull what we already hold**: with the Gallery, read `youtube-niche-bend`, `youtube-style-map` and the relevant channel/project collection; without it, read `niche-bend/library.json`, earlier rounds in `niche-bend/format-lab/` and their `keeps.json`. Apply the freshness window: packaging sources at most one month old.
3. **Search other niches, this month, by views.** Use title shapes: `every explained in minutes`, `is worse than you think`, `how long you'd last`, `that shouldn't exist`, `why evolution keeps`, `the most in history explained`. Search in the requested source and target languages using native wording, recording each scope. Drop off-topic drama, vlogs, reactions and news clips from emerging-format evidence; keep 8 to 60 minutes unless the brief specifies another comparable longform window.
4. **Check the channels** (`yt_scout.py channel`). A source counts when the channel is small (under 100K subscribers) and the median is real, or when one video is an outlier at 5× the median or more. Show a chronological frame sequence for every source to skim. Assess makeability/packaging transfer, but do not write inferred AI-versus-stock material labels.
5. **Write the bend** for each source: target niche, target language and our title under theirs. Run the title tests below and drop what fails. Keep every source's contribution explicit.
6. **Independently verify each surviving crossing** under `references/cross-verification.md`: three scouts, 8–12 target videos, 3–5 channel strips, same-scope query logs and a separate critical reconciler. Resolve contradictions before proposing a launch. Unknown and failed evidence must affect the verdict.
7. **Save and read back proposal cards in the existing Gallery**, associated with the intended channel/project. Open the existing Gallery view and report the verified results. Without the Gallery, build the local ideas board in `niche-bend/<slug>/` and open it.
8. **After an owner keeps ideas**: develop thumbnail-and-title variants using existing Gallery presentation and reusable project assets. Feed-size comparisons are packaging artifacts, not a new dashboard.
9. **After every piece of feedback**: update the Gallery record and write the rule into this skill (or the analyzer) and `how-we-got-here.md`. Feedback that is not written down gets repeated.

## Where sources come from

- **Targets are car niches by default** (Michael, 9 Nov 2026). Another niche only when the request names it; then a bend can stay in the source's niche with a new subject (history → history) or go anywhere with demand. Rank by evidence.
- **Ideas, titles and thumbnails come from other niches.** Prehistory, space, weapons, football, nature, business, war history. We do not follow what is trending among car channels, because that audience is already being served that way.
- **Channels in our own niche are format sources.** When a car channel has an audience for a format (Rare Car Storys: one engine on black, archive photos, a named man behind it), take the format, visual language or thumbnail layout and put an other-niche idea or title on it. This is a **merge**, and the board labels it and says which source gave which part.
- Rows whose packaging comes from a channel in our own niche go at the bottom, tagged "already served". They are the weakest claim to being first.
- A big channel (over 100K subscribers) may show topic demand, title conventions or competition. Repeated formulas on large channels support a market observation, not emerging proof or evidence that our faceless 2D treatment fits the target niche. Label that limited role.

## The title tests

A proposed title must pass all five. These came from Michael's rejections; the cases are in `how-we-got-here.md`.

1. **Recognisable on both sides.** Every noun that carries the title is something a general viewer can name (Ferrari, the Beetle, Formula 1), rank (world champion, world's first, biggest) or picture (an SUV, a tractor). A job or a description standing in for a name is dead weight: "the mechanic", "a loom maker's son", "the engineer". Use the famous name.
2. **Tension.** The two sides contradict: a champion, yet rejected; called ugly, yet outsold everything; the most loved team, and it cheated. If you cannot say the contradiction in one line, there is none. Write that line on the board as **Tension**.
3. **Human.** People click to watch someone succeed in spite of something, or to see how people differ. An adjective that names a human quality does work ("fearless", "delusional", "greedy"); a neutral descriptor does not.
4. **Urgency.** A news title works because the viewer needs to know now. The same shape on old history has no reason to be clicked today. Every idea states its urgency: a live news peg, a season in progress, a current product, or "evergreen" said plainly. A history video can borrow urgency by opening on this month's news and telling the history as the answer ("Porsche Lost 93% of Its Profit — It Has Been Here Before").
5. **Close to the source.** Swap the subject and leave the word order, length, capitals, punctuation and numbers alone. If the subject forces you to rewrite the sentence, the bend does not fit this formula. A fact not yet checked goes in [brackets]; never invent one.

When a source title works, say why in the terms above before bending it. "The World Champion Formula 1 Rejected" works because of a status everyone understands set against a rejection; a bend has to keep both, and "The Mechanic Toyota Rejected" kept neither.

## Choose the subject by demand: the subject ladder

A format can be filled with many subjects from our niche, and they are not equal: Formula 1 has several times the audience of rally. Before writing bends, rank the candidate subjects, and fill each proven format with the highest subject that fits its facts (Michael, 4 Oct 2026).

How to build the ladder:
1. List the sub-topics of the niche (for cars: Formula 1, rally, Le Mans, NASCAR, each big brand, engines, design, muscle cars, JDM, EVs, Chinese cars).
2. Run `yt_scout.py demand "<sub-topic> history"` and `"<sub-topic> explained"` for each, the same two wordings for all so the numbers compare.
3. Per sub-topic, pool both results and record two readings: **standing demand** (median of the ten best videos within the year, and how many passed 100K) and **heat** (the same for this month).
4. Read the top results of each and discount what is off-topic ("rally" pulls tennis and games; a brand name pulls dealer listings).

How to use it:
- Standing demand ranks the subjects. Heat says what is trending now and supplies the urgency line.
- The month reading is noisy, because YouTube's search returns only a few dozen videos. Trust the year median for ranking and treat the month as a signal only when several videos agree.
- This is a relative ranking from YouTube search results. It is not search volume, and it is YouTube only. **Demand has to be confirmed outside YouTube too** (Michael, 4 Oct 2026). Cross-check the ladder against at least one of:
  - **Google Trends**, through the browser pane: `https://trends.google.com/trends/explore?date=today%2012-m&q=a,b,c,d,e&hl=en` (five terms at most; add `&gprop=youtube` for YouTube search interest). Read the "Average" row with `get_page_text`. Keep one anchor term (e.g. `ferrari`) in every group so groups compare. Go slowly: several loads in a row and the charts come back empty. Watch for words with other meanings ("rally" is also political).
  - **Wikipedia page views**: `scripts/wiki_views.py "Label=Article_title" …`. Free and stable, good for general interest in a name.
  - **vidIQ** (official connector, `https://mcp.vidiq.com/mcp`, works on the free plan and spends vidIQ credits): `vidiq_keyword_research` gives search volume and competition per keyword. Use it when it is connected; if it is not, say so once.
  - The `theartofyt` connector, when authorised.
- When the sources disagree, show all of them and say which you trust for this question. Report them as separate columns, never one blended score.
- Show the ladder on the board, above the ideas, and put each idea's subject rung on its row.
- A high rung does not rescue a title that fails the tests. A strong story in a lower-demand topic may justify a clearly labelled experiment, but an empty crossing alone supplies no success proof. Apply the independent evidence gate before recommending it.

The first ladder (cars, 4 Oct 2026) is in `references/how-we-got-here.md`.

## What an idea row contains

Use these fields, in this order (the template renders them):

| Field | What goes in it |
|---|---|
| Source | Thumbnail, many chronological skim frames, title, views, age, channel, subscribers, niche |
| Tags | Round number · "My pick" (three at most) · "From <niche>" or "From a car channel: already served" · "Merge" · the story type |
| **Target niche** | Narrow target topic, language and viewer intent; observed targeting versus inferred audience |
| **Our title** | The bend, with [brackets] on unchecked facts |
| from: | The source title, so the pair reads as one unit |
| Tension | One line: the two recognised things and how they contradict |
| Urgency | Live, seasonal or evergreen, with the peg |
| Subject | What the video is about, in one sentence |
| Thumbnail | The layout in one or two sentences, written after looking at the source thumbnail: what is in frame, the exact words, where the eye goes |
| Opens on | The question the first 30 seconds raises |
| Structure | How the video is built |
| **Demand** | Do people watch this topic at all, with numbers, **and the linked thumbnails of those videos** |
| **Saturation** | Is someone already serving it our way, **with the linked thumbnails of those uploads** |
| **Audience/style fit** | Observed / Inferred / Unknown; actual target frames and hooks; `audienceFit` verdict and evidence |
| **Adaptation** | What changes in visual devices, narration, pacing, thumbnail and first 30 seconds for this target |
| **Previous attempts** | Successful and weak comparable crossings; dated performance and baseline; why our adaptation differs |
| **Independent verdict** | Three scout reports plus the separate reconciler; contradictions, missing checks and reject/Untested limits |
| Channel and source roles | Our channel/project collection; packaging, hook, format, style, facts and script reference associations |
| To check | The facts the title depends on |
| Reuses | Which of our existing plates and devices carry over |

**Demand and saturation are two lines and mean two things.** Demand: videos on the topic, in any format, that reached 50K to 100K or more. Saturation: channels that already make this the way we would and get views for it. A third case looks like saturation and is not: many recent uploads with no views. That means the plain retelling was tried and YouTube did not show it, which is a warning about packaging. Say which of the three you found. If someone posted nearly our exact title and it died, show it and say so.

Save evidence as Gallery source records and inspect the thumbnails plus chronological frames. An idea with no target evidence and independent verdict is not ready as a validated proposal. Three featured links on a compact card must link to the complete 8–12-video survey and channel strips.

## Local boards: the ideas board

On Michael's setup proposals live in the Gallery and this board is history. **Without the Gallery, this is the output.** Build it in the project:

```bash
SK=<this skill's base directory>          # run from the project root
mkdir -p niche-bend/<slug> && cp $SK/assets/ideas-board/index.html $SK/assets/server.py niche-bend/<slug>/
cp $SK/assets/ideas-board/data.example.js niche-bend/<slug>/data.js      # then replace the contents
python3 $SK/scripts/evidence.py niche-bend/<slug> niche-bend/<slug>/evidence-spec.json
```

- `data.js` holds `window.BOARD = {date, kicker, findings[3], ideasIntro, sources[], ideas[], retitles[]}`. The example file is a real round; keep its field names.
- Images are local: `img/<videoId>.jpg` and `img/<videoId>_1..3.jpg` (from `yt_scout.py frames --dir img` plus the thumbnail from `i.ytimg.com/vi/<id>/maxresdefault.jpg`), evidence in `img/ev/`.
- Serve it with `python3 niche-bend/<slug>/server.py <port>` and open it in the browser pane. One server can serve several boards through subfolders.
- Newest round on top, each row tagged with its round. Three findings boxes at the top: the rule in force, what the research showed, what follows from it.
- Keeps are `ideas`, `channels`, `retitles`, with a note per idea. **Do not reload the page while an owner may have unsaved clicks**; if you must, say so before, not after.
- If there is a finished film waiting for a title, add `retitles`: the same source formulas applied to it.

## Local boards: the thumbnail board (for a kept idea)

With the Gallery, reuse these comparison principles through its views. Without it, build this board in `niche-bend/<slug>/thumbs/`.

One board per kept idea, from `assets/thumb-board/`: `index.html`, `thumbs.js` (start from `thumbs.example.js`), `fonts/`, `img/` with the source thumbnail and eight real neighbour thumbnails from this month's research.

- **Six thumbnails, three titles.** Each thumbnail states its words, why it could work and which source its layout comes from. At least one carries the source's layout over directly. Each is shown large and at 168 px and 96 px wide.
- **The feed mock is the test.** Our thumbnail and title sit as the second card among real videos, on the home grid, the "up next" column and a phone, in dark and light. "View" swaps a design or a title into the feed. The feed uses YouTube's own UI language; the rest of the board uses the Style Scout tokens.
- **Round 1 is layout and words**, drawn in code (SVG silhouettes and type, existing plates). Say so on the board. The kept layout is then redrawn with engraved plates in the film's look, composited in code from separately generated layers, as the Lamborghini round 6 thumbnails were. State the per-image cost before generating.
- Thumbnails follow the project's look: Michroma for display words, Saira for small legends, cream paper and near-black, gold and one spot colour. No colour rectangles behind type, no heavy non-film font. High contrast. No real brand logos: draw a generic badge shape.
- **Style alternatives** (a different visual look for the video itself) are proposed only at this stage, for a kept idea. Never for the whole list.

## Reporting in chat

Keep it to: the verified Gallery location, proposed target niches and titles, how many sources and crossings pass their separate checks, the two or three strongest with numbers, independent verdicts and what remains Unknown/Untested or rejected. Full evidence and scripts stay linked from Gallery. Distinguish a configured draft research collection from a launched channel, and a paused schedule from verified cloud execution.

## Saving what we learn

- A new rule from an owner: write it into the project's `CLAUDE.md` (or a `niche-bend/RULES.md`) with the date, who said it and the case that caused it. In your own fork of the plugin, add it to "The title tests" here and the case to `references/how-we-got-here.md`.
- A rejected family or niche: the project's `niche-bend/no-go.md`.
- A source worth keeping: the gallery, label `youtube-niche-bend`, or `niche-bend/library.json`, when an owner says to save.
- Commit `niche-bend/` (keeps, no-go list, rounds) to the project's git after each round. Anything a skill depends on lives inside the plugin; anything a round produced lives in the project.
