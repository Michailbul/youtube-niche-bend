# The format lab: the routine and its files

The routine turns "what is working on YouTube" into format cards the owners can act on. One round is one folder, `niche-bend/format-lab/<date>/` in your project. The board for all rounds is `niche-bend/format-lab/` (`python3 niche-bend/format-lab/server.py`, port 8793), newest round on top.

## A format card has four parts

| | What it is | Where it comes from |
|---|---|---|
| **A. Packaging** | The thumbnail and the title that won the click, plus the title with its subject replaced by a [gap] | The video itself. Look at the thumbnail before describing it. |
| **B. Niche** | The subject and the audience it worked on | The channel's other titles |
| **C. Format** | How the video is built (list, ladder, timeline, one story, exposé) and what is visibly on screen (drawings, cutouts, diagrams, 3D, presenter) | Many chronological in-video frames to skim, not inferred AI/stock labels. Never the thumbnail. |
| **D. Where else** | Three other niches it could go to, each with the title it would ship with, each checked for views | `format_lab.py check`, then your own reading of the lists |

D is the point of the exercise. A target niche is worth proposing only if it is already getting views, so the work is not in vain. Do not limit D to cars: propose wherever the format fits and the niche is alive, and include a car niche when one honestly fits.

## The routine, step by step

0. **Watch for formats that are new and spreading** (Michael, 4 Oct 2026). A format blows up, and within weeks people carry it into other niches: "The 7 Levels of Rolex" became Audi, Mercedes, private jets, airports. We want to catch it while it is still crossing, and be the one who brings it to our niche.
   - `yt_scout.py formulas --out <round>/formulas.json --table` sweeps this month's uploads over 100K across the niches and title shapes in `scripts/watch_seeds.json`, and lists title wording shared by three or more channels, with the niches each was seen in.
   - Read the list and drop what is a phrase and no format ("N years ago"), a news event, a language tag, or one collab counted under several channel names.
   - Run `yt_scout.py spread "<formula with _ for the gap>"` on each survivor. It compares the last month with the rest of the year:
     - **New and spreading**: 70% or more of the formula's views came in the last month, with 3 or more videos over 100K. This is the one to move on. Example on 4 Oct 2026: "Engineers Tore Down a … What They Found", 13 videos over 100K on 24 channels, 98% of its views inside the month.
     - **Established and still working**: it had views before this month and still gets them ("… Is Worse Than You Think": 18 over 100K this month, 22 in the year). Safe, and no longer a head start.
     - **Past its peak**: the views came earlier in the year and this month is mostly copies ("The 7 Levels of …": 27 over 100K in the year, 4 this month from 18 channels).
     - **Thin**: fewer than 3 hits this month.
   - For each new or established formula, note which niches it has reached and whether ours is among them. A formula that has crossed two or more niches and has not reached ours is the best find. One that started inside our niche (the teardown) is already served there: take it to another niche or leave it.
   - These formulas become the sources of this round's cards. Everything below still applies to them.
1. **Collect what worked.** Sources, in this order: the gallery's packaging library (`youtube-niche-bend`), this month's searches (`yt_scout.py search` with title formulas and broad words, `--period month`), a niche survey (`yt_scout.py styles`), and anything Michael sends. Keep videos under a month old where you can; note the age when older.
2. **Pick 6 to 8 sources.** A source qualifies when it is an outlier (5× its channel's median or its subscriber count), the channel is not big (under 100K), and it is not on the no-go list. Run `yt_scout.py channel` on each: a cooled channel or a one-hit channel still gives packaging, and the card says so.
3. **Write A, B, C** for each from the thumbnail, the channel and the frames.
4. **Propose D**: three target niches per format, each with a title that changes as little of the source title as possible. Before proposing, look at what the source channel already tried: its own weak videos are the cheapest evidence there is (Odd Machines made "Weirdest Cars Ever Made Explained" in the same format and got 4.6K against 1.2M for combat robots).
5. **Size the target niches against each other before proposing them** (Michael, 4 Oct 2026: "there is rally and there is Formula One, and clearly Formula One would have a higher demand"). `yt_scout.py compare "formula 1|f1|grand prix=Formula One" "rally car|wrc=World Rally Championship"` gives, per topic: the views this month's top videos collected, how many passed 100K and 1M, how many came from channels under 100K subscribers and the best of those, and Wikipedia page views per day with their trend against the rest of the year. Run it twice: once on the plain topic (the whole pie) and once on the wording of our kind of video ("f1 history|f1 story"), because the pie is mostly official highlights and the slice is where we compete. Read three numbers:
   - **Size**: top-20 views this month and Wikipedia views per day. On 4 Oct 2026 Formula 1 was about 7 times rally on both (85M against 12.5M; 5K a day against 757).
   - **Ceiling for a small channel**: the best and the third-best video from channels under 100K subscribers, in the story slice. F1: 986K and 373K. Rally: 268K and 114K. This is the realistic upside for us, and the number to rank targets by.
   - **Now or always**: a Wikipedia trend above 1.3, a season in progress or a news peg means now. Otherwise it is evergreen, and say so.
   Prefer the bigger topic when its crossing is open. A small topic is worth proposing only when small channels take a large share of it or the crossing is confirmed. Put the size line on the card next to the verdict.
5b. **Check D.** `format_lab.py check <round>/spec.json` gathers, for every target: on-topic videos of the last month and year, how many passed 100K, how many came from channels under 100K subscribers, and whether the bent title already exists (the crossing). Then read `checks.json` yourself and give each target a verdict and one or two sentences of why.
6. **Audience and style fit** for any target where the look moves into a niche that may not accept it (see SKILL.md, 2c). Run `yt_scout.py styles` on the target niche, read the frames, tally.
7. **Merges.** Two or three, each from two cards: packaging from one, look and structure from another, with the audience named.
8. **Build and show.** `format_lab.py build <round>/spec.json`, open the board. An owner keeps formats, bends and merges by clicking. Read `keeps.json` before the next round, and move what he calls no good into `no-go.md`.

## Verdicts for a target niche

| Verdict | Means |
|---|---|
| **Confirmed** | Someone already made this crossing and it got views. The niche takes the format. Check how many are on it. |
| **Open** | The niche gets views from small channels, and nobody has made this crossing well. Best case, and unproven by definition. |
| **Contested** | The niche gets views and two or three channels already serve this angle. |
| **Crowded** | Many channels on it, or the views belong to big channels. |
| **Weak** | The niche or the crossing shows no pull: attempts exist and they failed, or nothing on the topic passed 100K. |
| **Untested** | Not enough on-topic results to tell. Say so. |

The numbers never decide alone. Search sorted by views drifts off topic, so read the titles: a count of "videos over 100K" means nothing if they are about something else.

## spec.json

```json
{"date": "2026-10-04", "sources": "where this round's sources came from",
 "headline": "optional, HTML allowed", "lede": "optional",
 "question": { "question": "", "verdict": "", "points": ["HTML allowed"], "stylesTitle": "", "styles": [{"style": "", "videos": 0, "medianViews": 0, "ours": true}],
               "attemptsTitle": "", "attempts": [{"title": "", "views": 0, "by": "", "age": ""}],
               "evidenceTitle": "", "evidence": [{"id": "", "title": "", "views": 0, "subs": 0, "by": "", "age": "", "style": "", "note": ""}] },
 "formats": [ { "key": "slug", "name": "short name", "flags": ["optional warnings"],
   "source": {"id": "video id", "handle": "@channel", "title": "", "views": 0, "age": ""},
   "niche": "B", "formula": "title with [gap]", "thumbnail": "layout in a sentence",
   "structure": "C, how it is built", "visual": "C, what is on screen, from the frames", "visualTag": "short look name",
   "targets": [ {"niche": "", "title": "our title", "topic": "plain search words for the niche", "cross": "the bent title as search words",
                 "verdict": "after check", "why": "after check", "proofId": "id of the niche's best on-topic video, from checks.json"} ] } ],
 "merges": [ {"key": "slug", "title": "our title", "niche": "", "verdict": "",
   "packaging": {"id": "", "title": "", "by": "", "views": 0}, "look": {"id": "", "title": "", "by": "", "views": 0},
   "audience": "who watches this and what they already watch", "proven": "", "unproven": ""} ] }
```

`question` is optional: use it when Michael asks whether one specific format would hold in one specific niche. `build` fills in channel numbers for `@handle` sources, downloads every thumbnail and three frames per video, and writes `lab.json`.
