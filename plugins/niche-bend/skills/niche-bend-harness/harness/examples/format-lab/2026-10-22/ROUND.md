# Format lab · round 2 · 22 October 2026

Numbers read on 22 October 2026 with `yt_scout.py` (formulas, spread, search, channel, frames,
demand) and checked against the no-go list and the keeps from round 1.

## Headline

**The survival ladder is three weeks old and has crossed six niches. Cars have not touched it.**

`How Long You'd Last in Every [X]` — 14 uploads this month from 14 channels, 3.8M views, 96% of
everything the formula has ever earned inside the last month. It started on a prehistoric ocean
(2.9M, flat 2D diagrams) and was copied into ice ages, dinosaurs, iPhones, FNAF and ACOTAR within
three weeks.

Why it matters for us: the best version of it is already drawn in 2D — silhouettes, cutaway
anatomy, one scale object next to the creature. That is our house look doing the work, not a
presenter, not stock footage. A car version is the open crossing.

## The cards

| Card | Source proof | Strongest target |
|---|---|---|
| `you-wouldnt-last` | 96% of views this month; 2.9M on flat 2D | **F1 eras — Open**: 4 of 9 on-topic uploads over 100K this month, none use the ladder |
| `overdue-collapse` | established (28%); 3 of 26 over 100K | **Car dealerships — Open**: 913K in 13 days from a small channel, formula unused |
| `shouldnt-exist` | established (31%); 13 of 22 over 100K | **Engines — Confirmed**: "The Engine That Should NOT Exist", 256K, but the niche is cold this month |
| `worse-than-thought` | established; 23 of 29 over 100K | **Used cars — Open**: 11 of 20 on-topic uploads over 100K this month, exact title free |

Weak crossings are recorded on the board and not recommended: Fisker, the hypercar market,
Dieselgate (two faceless attempts at 358 and 138 views), Group B and Le Mans (thin this month).

## Merge

`f1-1994-worse` — **The 1994 Formula 1 Season Was Worse Than You Think**. Packaging from the
worse-than-thought card (established, proven at 930K on a 15K-subscriber channel), look from the
survival ladder's flat 2D diagrams (2.9M). Audience: F1 story viewers, who gave 316K to a small
channel's F1 car evolution this month. Untested, and it stands or falls on the 1994 facts being
sourced before a script exists.

## Dropped this round, and why

| Dropped | Evidence | Why |
|---|---|---|
| "What REALLY Happened Inside the ___" | 92% of views in the last month, 7 of 14 over 100K | The whole burst is one news event (the Flydubai cockpit incident). News peg plus real footage of real people. |
| "Explained in N Minutes" | 18 channels, 9M views, 19% this month | Past its peak: this month is copies. |
| "The Man Who ___" | 17 channels, 15.9M, 14% this month | Past its peak. |
| "The Full Story of ___" | 18 of 26 over 100K | The hits are films, music and sport; no car fit without inventing a story. |
| "Engineers Tore Down a ___" | 13 channels | AI presenter over footage: no-go as a model (title formula still available under the outlier rule). |

## Files

- `spec.json` — the round as written, with every verdict and its proof video.
- `checks.json` — raw demand and crossing results for all 12 targets.
- `lab.json` — what the board reads.
- `img/` — thumbnails and three inside frames per source and per proof video.

Board: `python3 niche-bend/format-lab/server.py`, port **8793** (running). Newest round on top.
