# Tim Danilov's method

Source: "I Found 58 Faceless YouTube Niches In An Hour", Tim Danilov Biz, 22 Sep 2026, https://www.youtube.com/watch?v=Lo_JRTjq3fc. Transcript: `niche-bend/tim-danilov-58-niches/transcript.txt`. He runs faceless channels (The Art of War, Wholesome Wendy, Zeck Felms) and sells a coaching program, so read his income numbers as marketing. The search and bend logic is what we keep.

## His six checks for a niche

1. Launch budget under $1,000 a month. Above that, the money at risk on something unproven grows too fast.
2. Can realistically reach $15K a month within three months. Otherwise he does not enter.
3. The niche started less than six months ago. "If the niche is older than six months, there's no potential for you to enter it. Typically those niches are already taken."
4. Fewer than three competitors, so it can be dominated.
5. You can come up with a few bends for it.
6. You would enjoy running it.

Where we differ: we add a 50K median floor and a one-hit test (he judges by the most popular video), and we require faceless with no AI presenter (he rates AI presenters highest: "AI influencers are the highest rank possible").

## What he reads on a channel page, in about 20 seconds

- **Views against subscribers.** "The more views they get and the less followers they have, the better for you. It means the channel is fresh."
- **Videos tab → Popular**, then the age of the top video. He wants "two weeks ago", "a month ago".
- **Videos tab → Oldest.** When did it start. Four months is "perfect". A year is a reject.
- **Is it still posting.** A channel that stopped "probably got demonetized". Skip.
- **How many uploads.** Many uploads with a low average scores lower. Tennis Shadow Report got a 3 for that.
- **Collab feature.** A new channel fed with traffic from a sister channel is inflated. Note it.
- **How it is made.** He guesses the tool (Vidrush, AI stills, whiteboard, real animation) to price it. AI stills: cheap and "99% margin" but risky. Hand animation: "for whoever has $1,000 a month to spend on animators".

## His search methods

1. **A curated database** (his paid dashboard). Not available to us unless the `theartofyt` connector is authorised.
2. **A Claude connector that queries YouTube** per market. He asked for history, fitness, news and politics, fishing, true crime, psychology, relationships, celebrities, one report each.
3. **Incognito search**, free:
   - Logged out, search a broad word, filter to This month, sort by view count. Open small channels.
   - Search a title formula with a gap: "every _ explained". "This allows you to find all of the videos that used that particular formula."
   - After clicking several videos of one kind, return to the home page: it now recommends more of that kind.
4. **Community**: Discord alerts, a friend. People who watch YouTube for a living pass niches to each other.

`scripts/yt_scout.py search` reproduces method 3 from the command line.

## Niche bending, in his words

"Whenever you have a channel like this and you know that the format works, you can always switch one variable. The whole channel is about ships, so we can replace ships with something else, and this way we can easily get in front of the new audience."

"Niche bending is when you change one thing about the channel."

His bends from the stream:

| Source | What it is | Bends |
|---|---|---|
| Tennis Shadow Report | Daily tennis news | Golf, basketball, NFL |
| Letters from Britannia | British ancestry | USA, Germany, France |
| Silas Mercer | Off-grid DIY for men over 40 | Fishing, any hobby people over 40 have |
| How Ships Work | Life inside one kind of machine | Planes, trains, construction tech ("cars… no, not cars") |
| Animated History | Cartoon history | Dub it into another language |
| Unknown Frequencies | WWII cartoons | Roman Empire, Napoleonic Wars, any other army |
| The Frosty 1 | Game vs reality | GTA, any historical game |
| Fossil | "How long would you last" prehistory | The same visual format for true crime |
| MonteLago | One title: "Everyone Called Him an Idiot. He Got Richer Every Time." | The title for any history niche |
| Professor Gusty | Tornado records, whiteboard | Volcanoes, earthquakes |
| Cowball | Every gun mechanism explained | Planes, tanks, construction tech |
| SimpleToon | Cartoon character reviews | Anime, Marvel, Harry Potter |
| The Japanese Kitchen | Japanese kitchen tricks, AI host | DIY |
| Ryoga | Training explained with anime bodies | Looksmaxxing, female fitness |

## Testing a bend

"I would often just come up with ideas and then for each idea I would go and validate it on YouTube."

He typed "Japanese psychology", filtered to last month, saw videos with 57 and 45 views, and removed the bend on air. "You're coming up with the idea, you're testing it against YouTube in five minutes, and you have your decision."

For the Professor Gusty bend he checked the source channel itself: it had one volcano video, at 15K views. He read that as a sign to double down on. We would call it unproven and run the search test.

## Warnings he gives

- Plain AI visuals with a thin script get demonetised. Add real research and move the images.
- Bodycam and other footage niches only work with exclusive footage.
- Do not run a gaming channel unless you play. "Gamers have such a high bar that you can never meet it without being a gamer yourself."
- Non-English channels have a lower RPM.
- A competitor getting into a niche lowers its score even when the views are high (HEX, the Fern look).

## What we found re-checking his list on 4 Oct 2026

- 44 channels. 10 pass our filters.
- 14 had a median under 10K two weeks after the stream. His proof was one big video.
- 9 put a real person or an AI presenter on camera.
- The ten that pass: Pinoy Paint Explainer, Paint Maniac, Bexy Bloxy, Brainosophy, Finest Explainer, Cowball (all labelled grid), Professor Gusty (whiteboard), Animated History, Unknown Frequencies (cartoon history), Ryoga (anime figures). Six of the ten are the labelled grid.
