# Axes of the opportunity space

How 'nb.py' turns a round's numbers into a point. Every number comes from 'checks.json' / 'lab.json' of a
format-lab round, read on the round date with 'yt_scout.py demand' (month window, same query per target).
Each point stores the inputs in 'axes.demand', 'axes.saturation', 'axes.fit', and the date in 'axes.readOn'.

Demand and saturation stay two separate axes. The skill rule "never merge them into one score" holds:
the board shows them as X and Y; nothing multiplies them.

## X: demand (0-100)

'log10(month topViews)' on a 10K..3M scale. 10K or less = 0, 3M or more = 100.
Input: 'summary.month.topViews' for the target's topic query ('point.query').
Example: formula 1 history, 465,256 views on 22 Oct 2026 -> 67.
Limit: one video sets the number. 'over100K' and the year window stay in 'checks.json' for the reader.

## Y: saturation (0-100)

'0.7 * min(channelsOver50K, 8)/8 + 0.3 * min(channelsWith2PlusOver50K, 3)/3'.
Channels with a video over 50K on the topic this month count as copies that succeed; repeat channels count again.
8 channels or 3 repeat channels is the yt_scout "crowded" line, so those reach the top of the scale.
Limit: this is **topic** saturation. The exact crossing (our title formula on our topic) was judged by the
round author in 'notes'; the 'cross' search lists drift off-topic (Veritasium on "weird car engines"), so
they are kept as 'crossSample' for reading and are not used in the number.

## Z: fit (0-100), Inferred

'makeability x audience', both read from the card:

| Card visual line contains | makeability |
|---|---|
| presenter | 0.2 (packaging only) |
| footage | 0.5 (needs a restyle) |
| generated | 0.8 (monetisation risk) |
| archive | 0.6 (real people, rights) |
| 2d, cartoon, diagram, cutout, canvas, illustrated | 1.0 |
| stills | 0.9 |
| nothing usable | null |

Audience starts at 0.5 (unknown). +0.25 when a channel under 100K subs passed 50K on the topic this month
('smallChannelHits'). +0.25 when the proof video passed 100K from a channel under 100K subs.
This is a rubric over recorded facts. It is not an observed audience test. The Frame Reader and the
audience scout replace it with Observed values when they run.

## Size: freshness (0-1)

'0.5 ^ (days since checkedAt / 30)'. Recomputed at 'nb.py points' time, so old rounds shrink.

## Colour: verdict and confidence

| Round verdict | verdict | class | confidence (reconciled) |
|---|---|---|---|
| Confirmed / Proven | confirmed | support | 0.80 |
| Open | open | support | 0.65 |
| Contested | contested | uncertain | 0.45 |
| Untested, Format only | untested / format only | uncertain | 0.35 |
| Crowded | crowded | against | 0.25 |
| Weak | weak | against | 0.20 |
| Pass / Reject | pass | against | 0.10 |

Unreconciled points get confidence x 0.75. Every ingested point is unreconciled today.

## Missing on 22 Oct 2026

- Merges ('idiot-title-period-stills', 'feared-car-on-canvas', 'teardown-illustrated', 'f1-1994-worse'):
  no same-wording topic search was run, so demand, saturation and fit are null. They are listed, not placed.
- Every 'missing' entry is in 'runs/<round>-ingest/ledger.json'.
