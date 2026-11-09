---
name: niche-bending-youtube-analyzer
description: Research, validate and bend YouTube niches and formats for our faceless animated channels, and turn them into packaged video ideas (title + thumbnail). Niche bending means reusing what is already proven on YouTube, a format, a title formula, a thumbnail layout, a visual style, on a different subject or in a different look. Use this whenever Michael wants to find niches, trending formats or channels to copy from; asks whether a niche, channel, topic or bend is worth entering; wants demand or saturation checked; has a video idea and needs an angle, a title or a thumbnail for it borrowed from another niche; wants proven formats bent, restyled or merged into something new; shares a YouTube channel, a channel list or a "niches" video to analyse; or says "niche bend", "find me niches", "what's trending", "validate this", "find an angle for…", "is this worth copying", "what should we make", "video ideas for…", "scout YouTube for…", even if he never says the word "skill".
---

# Niche bending YouTube analyzer

Michael is building narrated 2D animated YouTube channels in any niche that earns it: history, cars, brands, nature, anything with demand. **Never assume the target is cars** (Michael, 19 Oct 2026: "we dont only want to niche bend into cars!!! this is not always the case"): bend into the source's own niche too, and rank every target by evidence. The rule of the whole operation: **reuse what is already proven.** We do not guess what people click. We find what they clicked last month, take the part that did the work, and apply it to our subject in our look.

The method started from Tim Danilov's stream "I Found 58 Faceless YouTube Niches In An Hour" (22 Sep 2026). When we re-checked his 44 channels two weeks later, 14 had dropped under 10K a video: one viral video had put them on his list. So we keep his search and bend logic and add our own proof standards.

**Running it:** owners, the `niche-bend/` data folder in your project, and Gallery-or-local-boards are in the `niche-bend` skill's `references/setup.md`. Where this file says Michael, read "an owner".

Read when needed:
- `references/cross-verification.md`: required independent topic/language, audience/visual-fit and crossing/counterexample scouts, followed by a separate critical reconciler. Target niches plus titles, checkable evidence cards and own-channel Gallery associations. Read before every proposed transfer or channel direction.
- `references/automatic-research.md` (Michael's setup only): authorized cloud research every three days (currently paused), Gallery dashboard contract, private proposal payload, first-30-second evidence and run verification. Read for every automatic round.
- `references/danilov-method.md`: his checks, search recipes and bends, with reasons.
- `references/format-lab.md`: the routine Michael wants run again and again, its four-part format card, the verdicts and the spec file. Read it before any "what works and where else can it go" round.
- `references/format-families.md`: the looks and structures in plain words, with example channels. Michael is learning the vocabulary: name the thing, show a frame, say who uses it.
- `references/no-go.md`: formats and niches ruled out, and why. The living copy is the project's `niche-bend/no-go.md` (made by `/niche-bend:setup`): read that before every research round and add to it after every keep round.
- Worked examples (on Michael's machine, not shipped): `niche-bend/tim-danilov-58-niches/` and `niche-bend/how-ships-work/`. Their lessons are already in these files.

## Frame review preference · 5 October 2026
Michael wants to judge the video by skimming many frames, not by our material-origin labels. Do not infer or write stock-footage, AI-generated or model classifications from appearance. The material source is not relevant to this research. Keep legacy fields for compatibility, but omit `productionStyle` and source-material `styleDescription` in new research saves. Use neutral visible composition/format names only when useful. Our proposed animation style, title/thumbnail lineage, structure and hook remain required.

With the Gallery, use its hover/scrub sequence with many chronological samples across the video and its opening; without it, use `yt_scout.py frames` sheets on the local board. Three fixed stored frames are fallback evidence, not a full skim. Never claim more coverage when richer frames are unavailable. Handoff the live Gallery URL; label localhost explicitly as development.

## Target-niche research is independently checked · 5 October 2026

Propose **niches with concrete titles**, not only source channels or untitled
subjects. Every transfer must pass `references/cross-verification.md`: three
independent scouts investigate topic demand/language, target audience/visual
fit, and exact-crossing competition/counterexamples; a fourth independent critic
then reconciles their evidence and challenges the idea. The proposer cannot
approve their own draft. Run the critic in a later wave when concurrency is
limited; without independent-agent capability, mark the gate unavailable and
keep the candidate Untested.

Inspect 8–12 relevant target long-form videos across 3–5 channels, plus each
channel's top three relevant recent videos with current numbers and many
chronological frames. Big/presenter channels are eligible only as audience,
demand or competition evidence, not as emerging proof or a faceless model.
Label findings Observed, Inferred or Unknown. Give frame-backed instructions
for what must change in visibility, demonstration, opening, pace and layout.
Fitness → women-focused yoga must inspect actual yoga videos; neither audience
demographics nor visual transfer follows from the target's name.

Preserve matched topic/formula/format/language and month/year search scopes,
queries, exclusions, limits and provider errors. Counts describe the searched
sample, not market share. Unknown evidence stays Untested; repeated comparable
failures or an unsupported title can reject a bend. An empty crossing is an
Untested experiment, not an automatic green recommendation. Public views never
establish gender, geography, CTR or retention. Keep the source's proof verdict
separate from the target's decision.

## Take an outlier apart against the same channel's flops · 19 October 2026

Before crediting a hit's script, structure or thumbnail device, read the transcripts and thumbnails of two or three of the **same channel's** videos that did not take off. What they share is the channel's house style and cannot explain the hit. Case: The Curious Stick's "Why Attacking a Sleeping Roman Army Was a Death Trap" (2.55M, 612× median). Its cold open, early spoiler, one spoken question and looped ending also appear in its Cannae video (5,162 views), which even had a trap thumbnail ("THE PERFECT TRAP"). Only the hit had a title naming a **situation** rather than a battle, a **reversal**, and a thumbnail line that reads like **dialogue** ("THEY'RE AWAKE"). (The worked teardown lives on Michael's machine.) Have an independent critic check the teardown; the first version here scored 6/10.

## A format has four genes

Everything below works on these four parts. A proven video is proof for each of them separately, which is what lets us take one and leave the rest.

| Gene | What it is | Example |
|---|---|---|
| **Title formula** | The sentence with a gap that the upload reuses | "Everyone Called Him an Idiot. He Got Richer Every Time." |
| **Thumbnail layout** | What is in frame, where the text sits, where the eye goes | A cutaway of a machine, one glowing room, a red arrow, two words |
| **Structure** | How the video is built | A tour, a ranked list, a timeline, one question answered |
| **Visual DNA** | The look on screen | Labelled grid, whiteboard, 2D cartoon, archive collage |

Title and thumbnail are the packaging. They decide whether anyone clicks, so they matter most and they are what we borrow first. Structure decides whether people keep watching. Visual DNA is the gene we change most freely, because our look is ours.

## The format card: A, B, C, D

Michael's frame for everything we find (4 Oct 2026). For each video that works, record four things:

- **A. Thumbnail and title.** The packaging that won the click. The most important part.
- **B. The niche** it worked in.
- **C. The format of the video**: how it is built, and what is on screen inside (2D animation, mostly static shots, generated stills, 3D, footage).
- **D. Other niches it could be applied to**, with the title it would ship with. Only niches that are relevant, popular and already getting views, so the work is not in vain. Not limited to cars.

The four genes above are what a card is made of: A is the title formula and the thumbnail layout, C is the structure and the visual DNA. Running this as a repeatable round is the **format lab**: `references/format-lab.md`, `scripts/format_lab.py`, board at `niche-bend/format-lab/` in your project.

## Look inside every video

A thumbnail is packaging. It is drawn to win the click and often shows nothing of how the video looks. When we checked the frames of the Danilov list, the cutaway on How Ships Work's thumbnail turned out to sit on a video made of real footage, Cowball's white grid on gun footage, and SimpleToon had a presenter on camera in every frame.

So for every video that goes on a board or into the gallery: pull its three in-video frames (`yt_scout.py frames`), show them next to the thumbnail, and write the description of the look from them. Say plainly when the inside does not match the packaging: then the packaging is still worth taking and the format is not.

## Freshness windows

YouTube packaging goes stale fast. A thumbnail style that worked a year ago is now what everyone does.

- **Sources for ideas, angles, titles and thumbnails: at most 1 month old.** This is the default of the search tool.
- **Reference channels and videos: at most 6 months old**, ideally 2 to 3. Older counts only as a style name ("legacy"), never as proof.
- Numbers are re-checked on the day. A claim from a video or from the gallery is as old as the day it was saved.
- When pulling references from the gallery's Videos tab, sort by date and say how old each one is. Anything past 6 months is flagged as legacy on the board.

## The tool

`scripts/yt_scout.py` reads YouTube pages and RSS directly. No API key, no yt-dlp (yt-dlp is often bot-blocked).

```bash
S=<this skill's base directory>/scripts/yt_scout.py      # run from the project root; install Pillow for sheet/frames/styles
python3 $S search "every _ explained" --period month --sort views --table   # what worked this month
python3 $S sheet "every _ explained" /tmp/sheet.jpg --max 24                # the same, as a thumbnail contact sheet to look at
python3 $S formulas --table                                                    # the format watch: title wording shared by 3+ channels this month
python3 $S spread "engineers tore down _ what they found" --table              # is a formula new, established or past its peak
python3 $S compare "formula 1|f1|grand prix=Formula One" "rally car|wrc" --table  # size topics against each other, with the small-channel ceiling
python3 $S demand "lamborghini history" --table                             # demand and saturation for a topic
python3 $S frames nAWpLtG-kNs 2ZS01obvQR0 --dir img --sheet /tmp/frames.jpg   # three inside frames per video: the real format
python3 $S styles "car history" "history of ferrari" --out round/cars --top 24      # which looks a niche's audience already watches
python3 $S tally round/cars/survey.json --table                                   # after labelling the styles from the frame sheets
python3 $S channels "Professor Gusty" --table                               # name or cut-off handle → real @handle
python3 $S channel @professorgusty @Cowball44 --thumbs img --table          # channel stats, checks, top thumbnails
```

Drop `--table` for JSON. Things to know:
- `channel` reads the latest 15 uploads from RSS. Median means the median of those, which is the channel today.
- The first-video date is automatic only for channels with 15 videos or fewer. For bigger ones open Videos → Oldest in the browser pane. The account's "Joined" date is not the niche's age: many channels run on old accounts.
- `demand` gives a reading, not a verdict. Sorting by views pulls in loosely related videos. Read the list and discount what is off-topic.
- `sheet` shows the packaging: thumbnail layouts at a glance.
- `frames <id> … --sheet out.jpg` pulls the three stills YouTube captures inside each video and lays them out one row per video. This is how you see the format. Always do it before describing a look.
- Handles read from a frame or screenshot are often cut off. Resolve with `channels`, confirm with `channel`.
- `/watch` pages answer 429 after a few hundred reads from this IP. For exact views, upload dates and lengths of many videos, use the Popular tab (browse endpoint) and `youtubei/v1/player`.

## Two ways in

Work out which one Michael is on.

**Format first** ("find me niches", "what's trending", a channel link). We start from something proven and look for where to apply it. Steps 1 → 2 → 3 → 5.

**Idea first** ("I want to tell how a brand was built", "a billionaire story", "a video about the Countach"). We start from our subject and go looking for the proven packaging and structure to carry it. Steps 4 → 2 → 3 → 5.

## 1. Research: find what is proven right now

The goal is small channels with recent videos far above their size. Big channels prove nothing about a format; their audience shows up anyway.

1. **This month, by views.** `search "<broad word>" --period month --sort views`. Skip channels you know are big, collect the small handles.
2. **Title-formula search.** Search a title with a gap: `every _ explained`, `the true origin of _`, `why _ failed`. One query finds a format across every subject it has spread to. The list of formulas is in `references/format-families.md`.
3. **Look at the sheet.** Run `sheet` on the best queries and read the thumbnails. Repeated layouts are formats.
4. **Neighbours.** Open a hit in the browser pane and read the suggested column. Formats cluster.
5. **What we have.** Check the gallery Videos tab (`list_video_refs`) when connected, `niche-bend/library.json` and `niche-bend/format-lab/` first so we do not rediscover channels. Apply the freshness windows to what comes back.
6. **Paid sources.** If the `theartofyt` connector is authorised, use it. If not, say so once and carry on.

Drop anything on the no-go list. Run `channel` on every remaining handle in one call.

## 2. Validate

Validation has two halves. The first asks whether the source is real proof. The second asks whether our version has room.

### 2a. Is the source proven: the channel scorecard

| Check | Pass when | Why |
|---|---|---|
| Median views | ≥ 50K across the latest uploads | A median shows the format working repeatedly. A top video shows one lucky day. |
| Not one hit | Best recent video ≤ 10× the median, or 3 of the latest 15 over 100K | 14 of Danilov's 44 failed here within two weeks. |
| Fresh | First video under 6 months ago | Older means the niche is taken or the audience is loyal to that channel. |
| Still posting | Upload in the last 14 days | A channel that stopped has usually lost monetisation. |
| Views above size | Best video ≥ 5× subscribers | The algorithm is showing it to strangers, so the format is doing the work. |
| Faceless | No presenter, no AI presenter, not built on footage of real people | Michael's rule. Only the in-video frames show this: `yt_scout.py frames <id>`. |
| Not too big | Under 100K subscribers, no established audience | Michael's rule (4 Oct 2026, The Frosty 1 at 282K): a big channel's views come from its audience and prove nothing about the format. The 100K line is my reading of it. |
| Makeable by us | Buildable as animated stills, cutouts, type and motion graphics | We do not film or edit real footage. |
| Monetisation risk | Real script, images that move, no reused footage | Thin AI-still channels get demonetised. |

Verdict: **Proven**, **Format only** (the channel fails but one gene is worth taking: say which), or **Pass** (say which check killed it).

A single video can be proof for a packaging gene even when its channel is not Proven, as long as it is an outlier: at least 5× its channel's median or 5× its channel's subscribers, and under a month old.

### 2b. Is there room for our version: demand and saturation

We are about to put a proven format on our topic, in our framing. Two questions, and they are different. **Demand**: do people watch this topic at all. **Saturation**: is someone already serving it the way we would.

Check three things, in this order:

1. **Topic demand, any format.** `demand "<our topic in plain search words>"`. Try two or three wordings, the way a viewer would type them.
   - Videos over 100K in the last year: the topic has an audience.
   - Videos over 50K in the last month: it is alive now. Hits a year ago and none this month means it cooled.
   - Small channels (under 100K subscribers) with hits: the topic carries a video without an audience behind it. This is the signal that matters most for a new channel.
   - Views all owned by channels with millions of subscribers: demand exists, but it may belong to those channels and not to the topic.
2. **Format demand, any topic.** `search "<the title formula with a gap>"` and the `sheet`. How many subjects has this format already spread to this month? A format that worked on one channel is one data point. A format that worked on four unrelated subjects travels.
3. **The crossing: our topic in this format.** Search the formula filled with our topic ("every lamborghini explained", "how ferrari actually works"). Read it against 1 and 2:

| Topic demand | Format demand | The crossing | Reading |
|---|---|---|---|
| Yes | Yes | Empty or weak within searched coverage | **Untested experiment.** Topic and formula may have proof; an empty crossing does not verify the audience/style transfer. |
| Yes | Yes | 1–2 small channels with real views | **Confirmed and open.** Someone proved the crossing and has not taken it over. Move fast. |
| Yes | Yes | 3+ channels over 50K, repeatedly | **Saturated.** Enter only with a different visual DNA or a sharper angle, and say what that difference is. |
| Yes | No | – | The format is the risk. Pick another format. |
| No | Yes | – | The topic is the risk. This is how "Japanese psychology" died: 57 and 45 views. Drop it or find the wording people use. |
| Cooled | – | – | It worked within the year and not this month. Treat as no, unless a new event brings it back. |

**Size comes first.** Before weighing one crossing, size the candidate topics against each other with `compare`: the views this month's top videos collected, the best videos from channels under 100K subscribers (the ceiling for us), and Wikipedia interest with its trend. Run it on the plain topic and on our kind of video ("f1 history|f1 story"). Formula 1 is about seven times rally, and its small-channel ceiling in story videos is about three times higher (986K and 373K against 268K and 114K, 4 Oct 2026). A bend into the bigger topic is worth more when the crossing is open, so rank targets by ceiling and say the size on the board.

Two more reads that sharpen the call:
- **Supply against demand.** Many recent uploads with few views means supply is ahead of demand: saturated even if no single channel dominates. Few uploads with high views each means demand is ahead of supply.
- **Our framing.** We are faceless and animated. If every hit on the topic is a presenter in a garage, the topic is proven and the animated version is untested. Say so plainly: it is an open lane and also an unproven one.

Report demand and saturation as two separate lines with the numbers behind them. Never merge them into one score. "People want it" and "it is crowded" are often both true.

### 2c. Will that audience accept it: audience and style fit

A format is watched by someone. When we move it to another niche, or put another look on it, the question is whether the people who watch that niche will sit through it. Michael's test case: "the entire history of [country]" works as a 2D cartoon in history. Would the same cartoon hold for cars? The way to answer is to look at what the car audience already watches.

1. **Survey the target niche.** `styles "<niche words>" … --out <dir>` collects the niche's strongest on-topic videos of the last year with three inside frames each, on sheets.
2. **Read the sheets and label each video's look** in `survey.json` (drawn, cutouts on a canvas, generated stills, 3D, footage narrated, presenter, chart race…). Mark off-topic ones and drop them. Then `tally`.
3. **Read the tally with three questions.**
   - Is our look already in use there, and by small channels? A look used only by a 500K channel proves the channel.
   - If the look is absent: has anyone tried the crossing? Search the bent title. Many attempts with a few hundred views each is evidence against. No attempts at all is an open and unproven lane. Say which.
   - What does that audience reward from small faceless channels? Those are the looks and angles to carry the idea with.
4. **Check the source channel's own experiments.** If it already tried our target niche in the same format, its numbers are the best evidence available.
5. **Think about what the viewer comes for.** A car viewer wants to see the car. A history viewer accepts a cartoon general. A format that hides the thing the audience came to look at will lose them, whatever the title promises.

Verdict lines, with the evidence: **Fits** (the look or a close one already works there on small channels), **Untested** (absent, no failed attempts), **Against the evidence** (absent and the crossing has failed repeatedly), **Fits with a change** (keep the packaging, swap the look or the angle for one that audience already rewards).

On 4 Oct 2026 the car test came out as "fits with a change": no flat cartoon timeline among the 24 strongest car-history videos, a dozen "entire history of [car brand]" attempts under 1K views, while the same audience gave 500K to 900K to a ladder on a white canvas, an inventor story in generated period stills, and a company exposé in illustrated stills, all from channels under 30K subscribers. The round is `niche-bend/format-lab/2026-10-04/`.

## 3. Bend, restyle, merge

Three moves. Each one keeps most genes fixed so the proof still applies.

**Bend the subject.** Keep all four genes, swap what the video is about.
- Same kind of thing: How Ships Work → planes, trains. Every gun mechanism → every gearbox.
- Another audience: tennis news → golf. British ancestry → German.
- Another language: the same videos, dubbed.

**Restyle.** Keep title formula, thumbnail layout and structure, change the visual DNA. This is how a real-footage or presenter format becomes ours: a garage-presenter "how it works" told as a 2D cutaway, a documentary with interviews told as archive collage. Check that the thumbnail still reads the same at small size in the new look, because the thumbnail is what was proven.

**Merge.** Build one format from the genes of two proven sources. For example the "Everyone called him an idiot" title on a brand-founder story, with the labelled-grid thumbnail, told as a cartoon timeline. Rules that keep a merge honest:
- Every gene comes from a source that passed 2a, and the board shows which source gave which gene.
- Two sources at most. Three is a new invention with no proof.
- The title and the thumbnail must tell the same promise. A merge that takes a mystery title and a list thumbnail fights itself.
- The genes must fit the content: a ranked-list structure needs a subject that comes in types, a timeline needs a subject with a history.
- Name the audience. A merge joins a title from one audience with a look from another, so say who would watch the result and show that this audience already watches something close to each half (2c). If the two halves come from audiences that do not overlap, find a third proof or drop the merge.
- Look for anyone who already made this merge. If someone has and it worked, it is confirmed. If someone has and it died, find out why before proposing it.

### Every bend comes with its title

A bend is never proposed as a bare subject ("planes", "volcanoes"). Michael judges a bend by reading the title it would ship with, so each one is shown as a pair: the source video's title and ours underneath.

Write our title by changing as little of the source title as possible. The source title is the proven object: its word order, length, capitals, punctuation, numbers and emotional word did the work. Swap the subject and leave everything else alone.

- Source: "Every Gun With A Strange Mechanism Explained" → ours: "Every Car With A Strange Mechanism Explained"
- Source: "The Flight Hitler Wasn't Supposed to Survive" → ours: "The Race Niki Lauda Wasn't Supposed to Survive"
- Source: "The True Origin of the Spanish Civil War: What Historians Get Wrong" → ours: "The True Origin of the Porsche 911: What Enthusiasts Get Wrong"

**The tension test (Michael, 4 Oct 2026).** A title works when it sets two things the viewer already knows and cares about against each other. "The World Champion Formula 1 Rejected" works because both sides are known and they contradict: a champion, and rejected. "The Mechanic Toyota Rejected" fails: "mechanic" could be anyone, and Toyota means nothing to the viewer here, so there is no tension and no open loop. Before proposing any title, check:
- Every noun that carries the title is recognisable to a general viewer: a famous name (Ferrari, Honda, Lamborghini), a status everyone understands (world champion, richest man), or a thing they have seen (the Beetle, the SUV). A job title or a description standing in for a name ("the mechanic", "a loom maker's son", "the engineer") is dead weight. Use the famous name.
- The two sides pull against each other: success despite something, a rejection of someone who then won, a thing everyone mocked that outsold everything.
- It is human. People click to see someone succeed against something, or to see how people differ. An adjective that names a human quality ("fearless", "delusional", "greedy") does work; a neutral descriptor does not.
- It has urgency (Michael, 4 Oct 2026). "Porsche Lost 93% of Its Profit — Here's WHY" works because it is news: the viewer needs to know now. The same shape on old history ("Lamborghini went bankrupt and changed hands five times") has no reason to be clicked today. Give every idea an urgency line: a live news peg, a season in progress, a current product, or say plainly that it is evergreen. A history video can borrow urgency by opening on this month's news and telling the history as the answer.
- Words do work. "How a Fearless Engineer Built…" gets clicked; "How a Loom Maker's Son Built…" triggers nothing. The sourced rules and the word lists are in `references/title-psychology.md` (4 Oct 2026): read it before writing titles.
- If the swap removes the recognised name or the contradiction, the bend does not fit this formula. Say so and drop it.

When you write demand and saturation on a board, show the thumbnails of the videos you are talking about, each linked to the video.

How to do it well:
- Start from the source channel's best title of the last month or two, the one with the most views over its median. A different bend can use a different source title from the same channel if it fits better.
- Change a second word only when the subject forces it ("Historians" → "Enthusiasts"). If you find yourself rewriting the sentence, the bend does not fit this format: say so and drop it.
- The title must be true. If the formula needs a fact you have not checked (a name, a number, an event), put it in [brackets] and never invent one. A title the video cannot pay off loses the viewer in the first minute.
- A merge follows the same rule with the title gene's source. A restyle keeps the title unchanged.
- On the board, the pair is one clickable unit: bend name, our title, then "from:" and the source title.

**Reuse a served channel's format on a new idea (Michael, 4 Oct 2026).** When a channel inside our own niche already serves an audience (Rare Car Storys with single-engine mysteries, The Sleeper List with car-industry news), we do not copy its subjects. We take its format, visual language or thumbnail layout, which that audience already clicks, and put an idea or a title from another niche on it. On a board this is a merge, and it is labelled as one.

**Style options come after a winner.** Ideas and titles are proposed first. Alternative visual styles for a video are proposed only for an idea Michael has kept, never for the whole list.

For every bend, restyle or merge, run 2b before showing it. Offer three per source and say which gene changed in each.

## 4. Idea first: find the angle and the packaging

Michael has a subject. We need the angle (what the video promises) and the packaging to carry it, taken from niches that have nothing to do with the subject.

0. **Check the packaging library first**: `youtube-niche-bend` in the gallery, or `niche-bend/library.json` without it, holds proven titles and thumbnails with their formulas.
1. **Name what kind of story it is**, in types that exist in every niche. A brand story is usually one of: an origin, a rivalry, a rise against the odds, a collapse, a hidden truth, a single decision, "how it works inside". A person's story: the outsider everyone doubted, the feud, the fall, the secret. Write down the two or three that fit the facts.
2. **Hunt each story type across other niches, this month.** Search title formulas that carry that type with the subject left as a gap: `everyone called him _`, `the _ that destroyed _`, `how _ lost everything`, `why _ failed`, `the true origin of _`, `the man who _`. Run `sheet` on each. We are looking for outliers anywhere: history, science, sports, food.
3. **Collect 8 to 12 outlier packages.** For each: the title, the thumbnail, views, channel size, age, and one line on why the click happens (the gap between what the viewer expects and what the title claims).
4. **Transplant.** Reduce each title to its formula and fill it with our subject. Describe the thumbnail as a layout (what is in frame, the two or three words, where the eye goes) and redraw that layout with our subject in our visual DNA. Keep the source next to our version.
5. **Check the facts carry it.** A formula that needs a villain needs a real villain in our story. If the facts do not support the promise, drop that package. Clickbait that the video cannot pay off kills retention.
6. **Validate with 2b**, then order by strength of proof.

## 5. Ideas: the deliverable

Whichever way in, the output is a list of packaged ideas. Never write ideas from a blank page.

Each card names the **target niche and language plus a concrete title**, with
the original source title/thumbnail and gene lineage beside it. Include
thumbnail promise, human tension, urgency, structure, observed source opening,
our first 30 seconds, and frame-backed adaptation instructions. Then show
separate demand, exact-crossing competition and failed-attempt evidence, the
8–12-video target sample/3–5 channel strips, query coverage and the independent
critic's decision. Observation, transfer inference and unknowns are distinct.
The complete card contract is in `references/cross-verification.md`.

For a format-first run, take source uploads at 2× median or better, reduce their
titles to formulas and test fitting target subjects. Drafting many titles is
not validating them: publish only independently checked target cards. Automatic
runs recommend at most three opportunities; fewer or zero is valid.

Order by proof: the source's views over its channel median, highest first. Titles of our own are plain and specific: no inflated words, no "not X but Y" constructions.

## The routine

When Michael asks what is working, what formats to take, or says to run the routine, run a format lab round (`references/format-lab.md`): start with the format watch (`formulas`, then `spread`) to find title formulas that are at most a month old, getting views and crossing niches; collect what else worked, write A, B, C for six to eight sources, and propose D as target niches with titles. Independently verify D under `references/cross-verification.md`, including actual target frames, comparable attempts and the separate critical reconciler. Save and read back the complete evidence and verdict in the Gallery, or build the format-lab board locally when the Gallery is not connected. Keeps from the last round steer the next one; legacy board instructions are historical context, not the current output destination.

## Output: existing Gallery, with channel/project associations

**No Gallery connected?** Then the output is local: `format_lab.py build` writes the format-lab board into `niche-bend/format-lab/` (serve it with `python3 niche-bend/format-lab/server.py`, port 8793; clicks save `keeps.json`), proposals go on the ideas board from `video-idea-proposals`, and every packaging record below goes into `niche-bend/library.json` with the same fields. The rest of this section is the Gallery path.

Michael's 5 October direction supersedes new local-board creation: publish the
research in the existing Gallery cards, collections, thumbnail wall, notes and
media previews. Do not copy a legacy board template or invent a new dashboard.
Existing boards/keeps remain historical context and are not reset or deleted.
Keep each channel's top three relevant recent videos visible with original
titles, thumbnails, current view/date metadata and a chronological skim sequence.
Source and proposal, independent scout evidence and final verdict stay distinct.

Associate an own channel's ideas, scripts, fact records and reusable sources
with its dedicated channel collection. `channel-europe-self-sabotage` is the
configured Europe/Germany research collection, verified by creation and readback;
its draft ideas do not establish a launched channel or proven audience. Reuse
`youtube-niche-bend` and `youtube-style-map` globally, while adding
channel membership and reference-role tags: `reference-packaging`,
`reference-hook`, `reference-format`, `reference-style`, `reference-facts`,
`reference-script`. Explain each role and its connection to the idea; several
roles are allowed. Use supported existing artifacts for scripts/facts, not
invented YouTube IDs. Do not change owner likes, notes or prior keeps.

Read owner feedback and legacy keeps before the next round; record explicit
rejections and rules rather than assuming every unclicked item was rejected.
In chat, link the live Gallery slice and report checked target niches/titles,
the strongest evidence, experiments/rejections and missing verification. Full
scout/query logs and ordinary linked source records hold the 8–12-video sample;
three featured links in the 4000-character proposal do not replace it.

For new proposal payloads, use the supported Gallery fields: `audienceFit`
(`Supported|Partial|Unknown|Mismatch`, summary and up to three featured evidence
links), `adaptation` (concrete instructions), and `previousAttempts` (summary and
up to three featured evidence links). Add `urgencyEvidence` (summary and HTTPS
URL) for a live/seasonal peg. These required new checks do not retroactively
invalidate older stored cards or imply that old evidence was independently
verified. Do not invent schema fields; link full surveys and scout reports.

**Gallery: the packaging library.** Titles and thumbnails that work are saved to the gallery's YouTube section so any agent can pull them later. The label is **`youtube-niche-bend`** (add a topical label such as `youtube-history-docs` when one fits). Save when Michael says to save; use the `laniameda-gallery` skill, `references/video-refs.md`.

Packaging/model qualification retains source validation and freshness. Use the
requested target language; do not discard native-language audience evidence
because a historical round defaulted to English. A qualifying recent outlier
can supply one packaging gene as Format only. Large/presenter target examples
may be saved with their explicit demand/competition/reference role, but never
receive `passes-filters`, `faceless` or Proven labels they did not earn.

Each record carries, besides the numbers:
- `titlePattern`: the title with the subject replaced by a [gap].
- `thumbnailPattern`: the layout in one or two sentences, written after looking at the thumbnail: what is in frame, the exact words, their colours, where they sit.
- Visual evidence: show the actual chronological hover/scrub frames. Omit source-material `styleDescription`; Michael reads the look from the frames.
- `format` (the structure), `whyItWorks` (why the click happens), `styleFamily` (reuse the names already in the gallery: list first).
- `bendIdea`: our bent titles for it, when we have them.
- `productionStyle`: legacy compatibility field only. Do not populate it in new research or infer material provenance from frames.
- `language` (`en`, `es`…), `channelLastUploadAt` (is the channel alive) and `checkedAt` (the day the numbers were read on YouTube). Send `checkedAt` on every save and re-check.
- `tagNames`: `youtube`, `faceless`, `niche-bend`, `packaging`, the topic, the source set (`danilov-58`, `artofyt-100`), a look tag (`labelled-grid`, `whiteboard`, `cutaway`, `entire-history`), and the status tags `passes-filters`, `one-big-hit`, `big-channel`, `non-english`, `fresh-channel`, `legacy-channel`, `has-bend`.

If a video is already in the gallery, keep its existing analysis and only add what is missing. (Michael's worked payload builders live on his machine.)

To look at the packaging: the gallery's Thumbnails view, `/youtube?view=thumbnails&theme=youtube-niche-bend`. Add `&since=90d` for what worked in the last three months, `&fits=1` for channels that pass every filter, `&size=study` to read the title formula and the thumbnail layout under each tile.

To pull packaging later (idea-first work starts here, before searching YouTube):
```bash
# all of it, best first · one look · words in the title, channel or notes
{"action":"list","collection":"youtube-niche-bend","sort":"views","limit":200}
{"action":"list","collection":"youtube-niche-bend","styleFamily":"Crude paint-drawing listicle"}
{"action":"list","search":"strange mechanism"}
```
Each result has `thumbUrl` and stored in-video `frames`; Gallery adds a richer hover/scrub sequence when available. Read the images when the task is about a look; no AI/stock diagnosis. Apply the freshness windows to `publishedAt`.

## Analysing a "niches" video someone else made

1. Transcript with the `supadata` skill or connector when available, otherwise the browser pane's transcript panel.
2. The speaker rarely says channel names. Read them from the frames: open the video in the browser pane, draw the paused frame to a canvas at full resolution, and read the spreadsheet rows, the address bar and the channel headers. Resolve cut-off handles.
3. Run every channel through 2a with today's numbers.
4. Pull the method too: checks, search tricks, bends. Add what is new to `references/` under its own source heading.
