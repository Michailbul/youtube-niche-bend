# How we got here

## Script, voiceover and first-minute production gates (8 Oct 2026)

Michael set the sequence for a kept idea entering production: analyse competitors and hooks from well-performing comparable videos, research and bend the script, get his script approval, then make the voiceover with the critic used throughout. The script and voiceover gates are recorded as at least 9/10. If the visual DNA is missing, establish it with references, visual preparation and a timed boardmatic; if it is already present, move directly into asset scouting with independent critic cross-checks. The shared workflow is [video production phases](video-production.md).

The first production V1 must cover the first minute end to end and be approved by Michael before the rest of the film is produced. His emphasis: "the first 30s should be ABSOLETUELY THE BEST POSSIBLE."

Michael also made cohesion a shared requirement: visuals, narration and graphics must match one another in the style of premium YouTube creators, with "100% alignment of what we see what we hear". Critics check actual picture and sound beat by beat, including subject and factual matches, timing and visual-DNA consistency, and flag unresolved mismatches before approval.

The record of the session that produced this skill (4 Oct 2026, car channel, after the Lamborghini film was finished). Each entry: what was proposed, what Michael said, what changed. Add to it after every round. His words are quoted; the readings are mine.

## The starting request

> "our idea now is to start with the thumbnail and title format/idea in mind first. to see what's working well in other places and readapt it… want to have a history explainer kind of format, same as we done now but find some angle we can approach new video with. lets stick to car theme."

So: idea first, packaging before script, history explainers about cars.

## Round 1, first pass: what I got wrong

I searched this month's top videos for story-type title formulas and took the strongest small channels. Half of them were car channels (Rare Car Storys, The Sleeper List), and the bends were car titles rewritten onto other car subjects.

> "we shouldn't necessarily look what is trending in our niche but … see what is trending in other niches. this way we are maximizing the probability of being first in the car niche, because we don't want to go after the market that is already being served, we want to find some new angles. Maybe there is a way we can tell the same story that already been told, about BMW history, whatever, but we would package it under something that is popular lately from a different niche."

**Changed:** other-niche sources first; car-channel sources moved to the bottom and tagged "already served". Added bends from prehistory ("How Long You'd Last in Every Era of Formula 1"), nature ("Why Evolution Keeps Turning Cars Into SUVs"), weapons, war history, ancestry.

**What the research itself showed**, which supports his point: brand-name retellings get nothing. Honda, DeLorean, Pinto and Tucker each had 13 to 18 uploads in the month, none over 1K views. The history is not the problem; the frame is.

## Evidence under the claims

> "when you write demand and saturation, lets also include the thumbnails-links for the references of what you are talking about"

**Changed:** every demand and saturation line shows the videos it refers to as small linked thumbnails (`scripts/evidence.py`).

> "when we are talking about saturation, what do we mean by that. if you mean that they posted the same type of content you proposed and it did not blow up?"

I had been using one word for two things. **Changed:** saturation means someone already serves it our way and gets views. Many uploads with no views is a separate finding, a packaging warning, and is reported as such.

## The title that taught the most

Proposed: "The Mechanic Toyota Rejected", from "The World Champion Formula 1 Rejected" (983K).

> "it's weak… if you look at the original video, why it blew up: the world champion Formula One rejected. It plays on this fear of missing out, because we say that he's world champion, but he was rejected, and this is the tension that people want to cover. But when we say the mechanic… first of all, Toyota is kind of like who cares? The mechanic, it's abstract, it can be anyone. It doesn't create this tension and loop. I want you to really learn from this, to not make this mistake again. When proposing the titles or the ideas, we always have to play on something recognizable, that people recognize and know very well. And also human for them. People want to see how someone succeeds despite something. People want to see how people are different. There should be tension. And the tension can only be if we care about those two parts."

**Changed:** the tension test (recognisable on both sides, contradiction, human). Rewritten on the board:

| Was | Now |
|---|---|
| The Mechanic Toyota Rejected | Toyota Rejected the Man Who Built Honda |
| How a Loom Maker's Son Built the World's Biggest Car Company | How a Fearless Outsider Built Toyota, the World's Biggest Car Company |
| The Engineer Ferrari Threw Out — And The Engine That Made Them Regret It | Ferrari Threw Out the Man Behind the 250 GTO — And He Built Lamborghini's Engine |
| The Tractor Maker Ferrari Rejected | Ferrari Rejected the Man Who Built Lamborghini |

## Words do work

> "I believe there are some words that perform better than others. 'How a fearless engineer' has much more chances to be clicked than 'loom maker's son'. It's not triggering any part of your human brain to click on it."

A sub-agent looked for existing skills on title psychology (none worth installing; eleven opened, all for on-camera tutorial creators) and collected sourced rules. They live in the niche-bending skill at `references/title-psychology.md`. The ones that match his instinct: curiosity needs prior knowledge (Loewenstein 1994); hang the title on a name already top of mind (Paddy Galloway); a status label does the work of a famous name (Creator Hooks); negative and extreme words lift clicks (Robertson 2023, MrBeast handbook).

## Urgency

Proposed: "Lamborghini Went Bankrupt and Changed Hands [5] Times — Here's WHY", from "Porsche Lost 93% of Its Profit — Here's WHY" (526K).

> "the reason why the first one would work and ours wouldn't is because the first one has the urgency. Because they have news format, they get this 'what happened recently', and this is more urgent than ours. So urgency is also an important factor."

**Changed:** every idea carries an urgency line. The merge "Porsche Lost 93% of Its Profit — It Has Been Here Before" came out of this: the news is the hook, the 1992 near-bankruptcy is the story. A small channel had 43K nine days earlier with "Porsche Made This Exact Mistake in 1978", which is the same move.

## Car channels are format sources

> "when we have 'from a car channel: already served', what we can do maybe is to apply the style of it, or the visual language, or the format of it, into the new, so that we can serve this audience who like this type of content but repackaged into a different idea of the video."

**Changed:** merges. Example: "Every Engine That Shouldn't Exist Explained in 14 Minutes" takes the title from a space channel (Bluntly Explained, 1.13M) and the thumbnail and inside format from Rare Car Storys.

## Style options come later

> "maybe we can also propose not only the alternating of the title name, but also some different style… but this step should only be if we select this as a winner."

**Changed:** visual style alternatives are proposed for kept ideas only.

## The thumbnail step

> "lets design the thumbnail. and the title and the video look already on the feed."

Built a board per kept idea: six thumbnails drawn in code, three titles, and a mock YouTube feed (home, up next, phone; dark and light) with our video as the second card among real neighbours from the month's research. Round 1 used flat silhouettes because no image provider had credit and the one working API reports no price per image; the board says the winner gets redrawn as engraved plates.

Standing thumbnail feedback from the Lamborghini rounds still applies: high contrast; a face and the logo when the story is about a person; the film's own engraving look, composited in code from separately generated layers "as if the graphic designer worked on it"; never a heavy non-film font; no colour rectangles; show the references a layout is based on.

## Demand by subject

> "there is rally and there is Formula One, and clearly the Formula One would have a higher demand. Is there a way we can validate those things, and should we do this validation when we niche bend or narrow down, so that we propose something that serves the demand, that is popular, or trending in the current time?"

**Changed:** the subject ladder. First reading, cars, 4 Oct 2026, two wordings per subject ("history", "explained"), pooled:

| Subject | Median of top 10, year | Over 100K, year | Median of top 10, month | Over 100K, month |
|---|---|---|---|---|
| Formula 1 | 1.07M | 14 | 1K | 2 |
| Ferrari | 603K | 17 | 55K | 3 |
| Lamborghini | 590K | 8 | 2K | 0 |
| BMW | 582K | 12 | 82K | 4 |
| Le Mans | 549K | 12 | 42K | 4 |
| Chinese cars | 383K | 11 | 43K | 2 |
| Porsche | 287K | 9 | 46K | 3 |
| NASCAR | 282K | 9 | 59K | 2 |
| Car engines | 274K | 10 | 3K | 2 |
| Rally | 248K | 11 | 34K | 2 |
| Toyota | 207K | 11 | 74K | 4 |
| Muscle cars | 206K | 8 | 3K | 1 |
| JDM | 68K | 3 | 1K | 0 |
| Car design | 60K | 4 | 78K | 4 |
| Supercars (as a word) | 17K | 0 | 0 | 0 |

His instinct holds: Formula 1 sits about four times above rally on standing demand. Car design is the one subject hotter this month than over the year. The month column is noisy (Formula 1 returned only 15 uploads on these wordings), and "rally" includes tennis and game videos.

## Demand outside YouTube

> "i think in general it should be not only youtube specific. maybe google trends or something" · "vidiq, i think is a good tool, do they have mcp?"

**Changed:** the ladder is cross-checked outside YouTube. First readings, 4 Oct 2026:

| Subject | Wikipedia views, 12 months | Google Trends web search, 12-month average (one group, relative) |
|---|---|---|
| Formula 1 | 2.32M | 30 ("formula 1") |
| Tesla | 1.46M | |
| BYD | 1.10M | |
| BMW | 1.06M | |
| Toyota | 1.04M | |
| Ferrari | 826K | 39 |
| Lamborghini | 779K | 18 |
| Le Mans | 774K | 10 |
| Porsche | 698K | |
| VW Beetle | 642K | |
| NASCAR | 500K | |
| Rally (WRC article) | 295K | 23 ("rally", which includes political rallies) |
| Car engines | 274K | |
| Muscle cars | 146K | |
| Supercar | 83K | |
| JDM | 60K | |
| SUV | 56K | |
| Car design | 36K | |

All three sources put Formula 1 and Ferrari on top and rally well below. Google Trends with the YouTube property returned empty charts after a few loads (rate limit), so that reading is still missing. vidIQ has an official connector; it was not connected in this session.



- Kept on the board: "Everyone Called It Ugly. It Outsold Every Car on Earth." (the Beetle; source MonteLago, 986K).
- Asked for thumbnails of: "Why Evolution Keeps Turning Cars Into SUVs" and the Beetle.
- Called the proposal structure promising and asked for it to become this skill.

## What the structure looks like when it works

The row he kept has: a source title with a clear human contradiction; our title in the same rhythm with a shape everyone can picture; a thumbnail layout carried from the source (a crowd pointing at one outsider); the strongest topic demand of the round (394K, 116K, 111K within the year); an open field; and facts listed for checking. Use it as the reference row.

## Mistakes to avoid repeating

- Bending a title without first saying why the source works.
- A description where a famous name should be.
- Counting a channel in our own niche as an other-niche source.
- Writing "saturated" for a topic that is merely full of unwatched uploads.
- Demand claims with no linked videos under them.
- Reloading a board while Michael has unsaved keeps (it happened once; his clicks were lost).
- Referencing a file inside `niche-bend/` from a skill: that folder is gitignored.

## From the idea to a film: the Beetle (4 Oct 2026)

Michael picked the Beetle idea and asked for a project folder, the source's script adapted to 9 minutes, an explorer to iterate in, and free footage.

> "I'm thinking it has to be like live action, like realistic, not animation style. For car enthusiasts."
> "make it in a gallery view so that I can review the asset that I like and scroll through the ones that I like"
> "it would be great if you would be able to have the footage split into frames, that when I hover on the archival footage I can see it in the frames, so that I can see what the video is about without looking at the video"
> "take this archival footage and post-process it, apply some filters, cut out like an animator, and layer it… we have the video playing, and then the animation of a photography click, and then we cut out the image, transform it to some kind of paper look, and then move to paper animation, or maybe not paper but just a plain background… this combination of real footage with motion graphics elements"

**What was built:** the source transcript pulled through vidIQ and taken apart move by move; our script written beat for beat against it, then every claim fact-checked before showing it (four popular "facts" turned out to be legends); an explorer with tabs; a footage list with rights classes and hover strips; an art-direction gallery of moving frames made only from free footage and code.

**Worth repeating:** adapt the structure of the source, never its sentences. Fact-check before the script is shown. Sort footage by the story beat it covers and count the free items per beat, so it is plain which parts must be drawn. Show a style as the same beat done several ways.


## Existing Gallery only; historical 3D revival (12 Oct 2026)

Michael reaffirmed that research must reuse the existing UI/frontend. Use Gallery `/youtube`, source cards, private proposal cards and native text records. Do not create another research dashboard or redesign the frontend.

For this round he explicitly requested older successful 3D videos, roughly one or two years old, alongside current traction. Label those donors as historical mechanism/demand evidence. This exception does not make established channels emerging proof or remove the normal freshness filter for new packaging.

Separate source-family success from an untested target transfer. A novel rendering style and an empty bounded search cannot justify a numerical launch probability.

## A research report must answer the decision (12 Oct 2026)

Michael scored the first cartoon-history report 6/10 and asked for 8/10: more finds, more statistics and independent agents to critique the finished result, while retaining the existing Claude HTML design.

Use the full Latest non-Short video-tab inventory with N, rather than an RSS subset, for the channel baseline. Show weak uploads beside hits, raw and mature-upload medians separately, hit rates, concentration and checked dates. A one-upload sample cannot pass repeatability even when a ratio-based proxy says otherwise. Views/day must use one stated denominator throughout.

Lead with two or three ranked decisions, the original package, actual opening frames, the strongest objection and a concrete next test. Independently audit the actual rendered board and identifiers as well as the statistics. A research-quality score is separate from proof that a target crossing is open. Preserve the owner's keeps. Detailed round records remain in the channel project's documentation.


## Images are the research result (12 Oct 2026)

Michael rejected the improved history packet's statistics and raw Markdown reports as unusable piles of text. Accurate data and a critic's numeric score do not settle the owner's visual-usability requirement. Channel statistics must lead with original thumbnails, titles, view counts and visible inside-frame strips; medians and weak uploads sit beside those pictures. Reports open as illustrated findings and comparisons, with long text available secondarily. Judge the actual desktop/mobile skim, preserve the existing UI language and keeps, and label missing bodies instead of guessing style from a cover.


## Scripts, words and performance comparisons · 12 October 2026

Michael requested script-level research plus title/thumbnail keywords, patterns, hooks and psychology for the history-channel findings. Keep the visual handoff: original packaging beside strong and ordinary/weak examples, then caption-grounded opening, body and ending annotations. Count actual full readings separately from retrieved transcripts. Use all available recent upload inventories for word associations, show each channel baseline and N, and label psychology as inference. In this round the same title words, scene hooks and callbacks appear in weaker uploads; resemblance is reusable craft, not proof of what caused success. Full evidence: `history-channel/research/2026-10-12/round-04-patterns/`.
