# Automatic research · 5 October 2026

> **Michael's setup only.** This describes the cloud schedule on Michael's own accounts (paused, never verified). It is reference for how a scheduled round should behave. With this plugin, run rounds by hand or with `nb.py rails`; see the `niche-bend` skill's `references/setup.md`.

Michael explicitly authorized recurring research, Gallery saves/updates and adding
the official vidIQ connector. The Gallery is the main dashboard. Reuse `/youtube`,
its Niche bend theme, thumbnail wall, channels, detail pages and existing tokens.
Do not build another board or redesign the UI for this workflow.

## Read at every run

Read the project `CLAUDE.md`, this skill, `references/format-lab.md`,
`references/no-go.md`, `references/cross-verification.md`, and
`video-idea-proposals/SKILL.md`. Read adopted technique
keeps and `DIRECTION.md`; query the Gallery for existing packaging and owner likes
and notes. Explicit feedback from Michael overrides older rules. Read the Gallery
skill and `references/video-refs.md`; worlds are outside this research.

## Scope and evidence

Focus on narrated long-form **2D animation and motion design**: illustrated
explainers, whiteboard, cutouts, maps, diagrams, collage, type and layered stills.
Cars are the first target; business, brands, science, history and other subjects
are eligible when their demand and audience fit earn it. Show many chronological inside frames for visual review. Material origin is not
relevant: do not infer or write stock/AI/model labels or source-material diagnosis.
Explain which packaging or structure gene is borrowed; keep our proposed 2D
treatment separate from the observed frames.

Search across niches using `scripts/watch_seeds.json`, recent outliers and title
formula sweeps. Packaging sources are at most 30 days old; craft references at
most 6 months. Established channels over 100K subscribers prove no emerging
opportunity. Validate the latest long-form median (50K minimum), repeated hits,
first upload under 6 months, last upload within 14 days, views over size,
faceless status and makeability. Unknown checks stay unknown. A one-hit, old or
cooled channel can be **Format only** for a qualifying packaging outlier; never
label it Proven. Exclude Shorts-only, presenters and existing rejections as models.

Start with other-niche title/thumbnail packaging. Look at the thumbnail and a chronological frame sequence spanning each source;
three fixed stills are only fallback evidence. Compare a channel's top three recent
videos; save those that independently meet the reference rules. Show the source
title next to each bent title. Preserve the source formula, recognized nouns,
human tension and urgency; mark unverified facts with brackets.

Check format spread, target demand and the exact topic/format crossing. Read
results for relevance. Use the same `history` and `explained` queries, month and
year, to compare target subjects. Prefer the biggest fitting subject with an
open crossing. Distinguish failed low-view copies from successful competition.
Cross-check demand outside YouTube with Wikipedia pageviews or Google Trends.
vidIQ search volume and competition remain separate metrics; no blended score.
An empty crossing is an experiment, not proof of success.

## Target niches, titles and independent verification

Every run proposes **target niches together with concrete titles**. The source
format is the starting evidence, not the final opportunity. Name target niche,
content job, language, exact topic/formula/format crossing and the one-variable
change; show original and proposed title/thumbnail lineage beside each other.

Use `cross-verification.md`: three independent scouts investigate (1) topic
demand, language and urgency, (2) actual target-audience visual/structural fit,
and (3) exact-crossing competitors and prior successful/failed attempts. A
fourth independent critical reconciler examines the raw findings afterward,
seeking the strongest reason the transfer fails. The proposer does not certify
their draft. Run a later review wave when concurrency is limited. If cloud
agent capability is unavailable, disclose that gate as unverified and keep
the candidate Untested; one agent writing several role headings is not enough.

Inspect 8–12 unique, on-topic target long-form videos from 3–5 channels, with
each surveyed channel's top three relevant recent videos and chronological
frames. Fewer usable sources means insufficient coverage, not permission to
pad the sample. Big or presenter channels may establish target demand,
conventions or competition only; they remain ineligible as emerging proof or
our faceless execution model. Fitness → women-focused yoga requires reviewing
actual yoga videos, not assuming visual transfer or viewer demographics.

Label visible evidence Observed, transfer reasoning Inferred and unavailable
checks Unknown. Publish frame-backed instructions for what to retain/change
in subject visibility, demonstration, title/thumbnail, opening, pace and layout.
Preserve adopted visual vocabulary. Log matched language/topic/formula/format,
month/year windows, query wording, sorting, result limits, exclusions and errors.
Counts describe searched coverage, not market share or exhaustive competitors.
Keep topic demand, format spread, exact competition, failed attempts and the
external signal separate. Negative or missing evidence cannot become an
automatic green result: Untested/Weak or rejection is valid, as is zero ideas.
Public views do not prove audience gender, age, country, CTR or retention.

The final card includes the niche/title pair, source lineage, target evidence,
the separate scout findings and critic's objection/decision, urgency, explicit
adaptation instructions, source opening versus our three opening beats, and
the next falsifiable check. Keep the source verdict separate from target fit.

For an opening analysis, obtain timestamped captions with Supadata, YouTube's
transcript or vidIQ Video Watch, and inspect the opening itself. The three
auto-captured inside frames occur around 25/50/75% and **do not verify the first
30 seconds**. Record an unavailable source opening honestly in `hook`. Put our
proposed 0–5s promise, 5–15s tension/context and 15–30s payoff/open loop in the
proposal. Public views never prove CTR or audience retention; those require
authorized creator analytics and are otherwise unknown. Keep observation,
inference and our proposal distinct.

## Tools and cost

Use Gallery MCP `check_connection`, `list_video_refs`, `get_video_ref` and
`save_video_refs`. vidIQ: `https://mcp.vidiq.com/mcp`, registered in Codex and
authorized on 5 October 2026. Tools may appear only on a subsequent session.
Check its free credit/status tools first. Use already available credits for a
small shortlist, max **5 credits per scheduled run** and only if balance/prices are known;
use free research when they are unavailable. Never buy credits or generate media
as part of research. If vidIQ cannot be called, mark that connection/data check
unverified and keep researching via the existing scout/RSS and external demand.
The five-credit ceiling is shared by all scouts and the reconciler in the run;
the orchestrator assigns any paid calls to avoid duplicated spending.

`scripts/research_round.py collect` reuses `yt_scout.py`, rotates broad queries,
records raw searches/channel checks in `research/rounds/`, and reports provider
errors explicitly. These are candidates, not recommendations. Inspect the best
sources semantically and visually, then create a Gallery payload. Run
`research_round.py validate <payload.json>` before saving. No auto-invented ideas.

## Existing Gallery contract

Use existing theme **youtube-niche-bend**, and **youtube-style-map** for style
references. Source records retain language, checkedAt, publication date, recent channel stats
and actual thumbnail/frames. Omit inferred `productionStyle` and material-origin
`styleDescription` in new research saves; older classifications remain legacy.
Reuse existing tags, such as `niche-bend`, `packaging`, `has-bend`, `drawn`, and
`passes-filters` only when every required check passed. Do not change Michael's
likes, notes or previous keeps. Re-saving a video updates it and merges labels.
Save up to 12 per call, then read every record back and verify media, metadata
and the proposal. Do not declare success on a tool response alone.

Keep our own channel/project's ideas, scripts, facts and reusable references in
its dedicated Gallery collection using existing supported records/artifacts.
`channel-europe-self-sabotage` is the configured Europe/Germany research
collection, verified by creation and readback. Its draft ideas do not establish
a launched channel or audience. Each execution context verifies its access. Add source
role associations with `reference-packaging`, `reference-hook`,
`reference-format`, `reference-style`, `reference-facts`, `reference-script` and
explain the link to the idea. Preserve global reference memberships, owner
notes/likes and keeps. Role tags do not change source-proof eligibility.

`hook` describes the **observed source opening**, or states why it is unavailable.
`format`, `titlePattern`, `thumbnailPattern`, `whyItWorks` describe the source
structure and packaging. Source materials are judged from the frames, not written
as AI/stock classifications. Our proposed animation treatment stays in the bend. `bendIdea` holds private JSON conforming to the Gallery's
`lib/youtube-research.ts` schema; it is shown only in the signed-in owner's
session. Maximum **4000 characters**, including JSON: the backend clips longer
strings. Aim for one strong bend per source, up to three concise ones. Never
truncate JSON to fit. Do not overwrite an earlier good bend just to refresh stats.
The compact proposal contains up to three featured evidence links per demand
or saturation field; retain the complete 8–12-video survey as linked ordinary
Gallery source records and full scout/query reports in accessible research
context. Point the proposal to that record set. Do not pretend three featured
links complete the survey or change the schema to bypass the evidence gate.

New proposals require supported `audienceFit` (verdict
`Supported|Partial|Unknown|Mismatch`, summary, up to three featured evidence
links), concrete `adaptation`, and `previousAttempts` (summary and up to three
featured evidence links). Use optional `urgencyEvidence` (summary and HTTPS URL)
for a live/seasonal peg. Older stored v1 cards remain compatible; the new checks
apply to newly researched proposals. Keep full independent reports accessible.

For chronological frames, use the Gallery's hosted storyboard collector when
it is present and verified: `bun scripts/collect-youtube-storyboards.ts --ids <json> --output <snapshots>`,
then the existing Gallery cache writer. Confirm published-cache readback;
local snapshots alone do not prove hosted availability. Stop at the first 429,
preserve good cache, and mark missing coverage. Do not repeat heavy requests or
bypass provider limits to fill gaps.

Shape:

```json
{"v":1,"checkedAt":"2026-10-05T12:00:00Z","sourceVerdict":"Format only",
 "validation":"Every channel check, failures and unknowns; what gene earns reuse.",
 "bends":[{"niche":"cars","title":"Our title","verdict":"Untested",
 "why":"What transfers and what is still an experiment","tension":"Recognized contradiction",
 "urgency":"Evergreen or a linked current peg","thumbnail":"Source layout adapted to our subject",
 "style":"Our existing 2D approach; source style kept separate","format":"Episode structure and pacing",
 "first30":["0–5s promise","5–15s tension","15–30s payoff/open loop"],
 "demand":{"summary":"On-topic, checked numbers","evidence":[{"id":"abcdefghijk","title":"Evidence title","views":100000}]},
 "saturation":{"summary":"Exact crossing, counts and limitations","evidence":[]},
 "audienceFit":{"verdict":"Unknown","summary":"Actual target frames and independent review still needed; full survey linked in research context","evidence":[]},
 "adaptation":"Concrete target-specific changes, with observed versus untested parts explicit",
 "previousAttempts":{"summary":"Successful and weak comparable attempts, or missing coverage stated honestly","evidence":[]},
 "externalDemand":{"source":"Wikipedia pageviews","summary":"Separate external signal or honest failure","url":"https://pageviews.wmcloud.org/"},
 "toCheck":["Facts or missing evidence"]}]}
```

## Run cadence and completion

**Michael's update, 5 Oct 2026:** desired execution is **cloud**, every **three
days at 09:00 Europe/Prague**, and **paused** until he explicitly resumes it.
The initial local heartbeat is paused with that cadence. Cloud setup is not
complete until the hosted task exists, its connectors can authenticate, its
prompt/rules are available without local Mac paths, and status reads back paused.
Do not represent a paused local task as a configured cloud task. Use
`cloud-research-prompt.md` as the portable prompt; keep the local heartbeat paused
after a cloud replacement is verified, so there is no duplicate execution.
Each run checks the previous run and Gallery records, refreshes promising active
channels, collects new candidates and advances the strongest proposals. Up to
three recommendations per run; fewer or zero is valid. Never pad the results.
Record stats snapshots, actual query coverage, connection failures and saved
video IDs locally. Compare successive checked snapshots before claiming growth;
views/day since upload is only average velocity. Read keeps/notes before the next
run, skip rejected sources, and persist explicit new feedback to project rules.

Notify only for a meaningful new opportunity, a material change in an existing
proposal, completion/failure, or required user action. Quiet when unchanged or
non-actionable. Link directly to the existing Gallery slice and source detail.
Report partial research or missing evidence honestly. Connection setup, saving a
record, publishing code, visual review and a verified scheduled run are separate.
