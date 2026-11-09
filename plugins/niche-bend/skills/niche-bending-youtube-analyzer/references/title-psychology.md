# Title psychology: why some titles get the click

Researched 4 Oct 2026 for the `niche-bending-youtube-analyzer` skill. Scope: faceless narrated car-history videos.

How to read the sourcing. "Read" means I opened the page or file. "Snippet" means the page blocked me (vidIQ, Cybernews, Nature, X) and the figure comes from a search result quoting it. Podcast pages were read through an automatic summary of the transcript, so treat the quotes as close paraphrase until checked against the audio. Lines marked "our reading" are my inference from the sources and from Michael's feedback, and have no outside proof.

---

## A. Agent skills found

Searched with `npx -y skills find` for youtube, title, thumbnail, hook, viral, youtube title, youtube thumbnail, youtube packaging, clickbait, headline, youtube script, plus GitHub and skills.sh by web search. Nothing was installed. Install commands follow the format the CLI prints (`npx skills add <owner/repo@skill>`) and were not run.

**Short answer: none is worth installing.** Every one is written for a creator who appears on camera and teaches or reviews things. None covers story titles about people and brands, none says what makes a subject recognisable, and only one cites its sources. Three contain a part worth copying into our own skill.

| Skill | Repo | Install command | What is inside (files read) | Verdict |
|---|---|---|---|---|
| `yt-package` | [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) (466 stars, MIT) | `npx skills add Jakeschincariol/youtube-agent-skill@yt-package` | A 2.3 KB SKILL.md and `title.py`, a linter: flags titles over 60 characters (desktop cut) and shows what survives the 40-character mobile cut, flags a list of vague words (amazing, insane, ultimate, secret…), more than two all-caps words, thumbnail text that repeats the title, and any title without a number. No sources. | **Do not install.** The "no number is a fault" rule would mark down every story title we write. Worth copying: the 40-character mobile check and the vague-word list. |
| `youtube-packaging` + `youtube-virality-gate` | [ravsau/youtuber-skills](https://github.com/ravsau/youtuber-skills) (5 stars, MIT, 15 installs) | `npx skills add ravsau/youtuber-skills@youtube-packaging` | 3.6 KB + a visual-checks file. Five title and thumbnail pairs per topic, one in the "Galloway formula" (subject + number + timeframe + mechanism), truth and legibility gates, a backup pair for YouTube Test & Compare. Cites the MrBeast handbook, vidIQ's 500-video study and YouTube's help pages. The gate skill is an eight-row pass/fail table. | **Do not install.** Built for screen-recording tech channels. Worth copying: the "thumbnail adds what the title does not say" gate and the habit of naming a backup title. The only candidate that links sources. |
| `titles-and-thumbnails` | [yaxeen/storytelling-skills](https://github.com/yaxeen/storytelling-skills) (9 stars, MIT, 17 installs) | `npx skills add yaxeen/storytelling-skills@titles-and-thumbnails` | 6.4 KB + a pattern bank. Six how-to formulas ("How I [result] in [timeframe]", "Stop [practice]. Do this instead"), the title-thumbnail pairing test (cover one, does the other still pull), a bad-to-good rewrite. No sources. | **Do not install.** Tutorial and vlog formulas only. The pairing test is the one useful idea and it is one sentence. |
| `packaging-youtube-thumbnails` | [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) (3,600 stars, MIT, 12 installs) | `npx skills add ericosiu/ai-marketing-skills@packaging-youtube-thumbnails` | The largest: 15 KB SKILL.md, a rubric, Python guards with tests, a per-channel profile and a performance memory. I read the opening of the SKILL.md and most of the rubric. Thumbnail-first, built around a creator's face and an existing channel with analytics. Runs a telemetry script on start (remote telemetry is opt-in by its own description). | **Do not install now.** Too heavy and aimed at presenter channels. Come back to its rubric when we build thumbnail QA: "no more than three visual groups plus one text block" and "two viewers must give the same explanation of the image at 320×180" are good gates. |
| `youtube-title-generator` | [vincentchan/AI-Content-Engine](https://github.com/vincentchan/AI-Content-Engine) (73 stars, no licence, last push Jan 2026) | not on skills.sh; would be `npx skills add vincentchan/AI-Content-Engine` (unverified) | 10 KB. Thirty titles per idea in three self-improvement formulas ("How To Get Ahead Of 99% Of People In 6-12 Months"). Tells the model to be "polarizing" and "hyperbolic". | **Do not install.** Wrong genre, no licence, stale. |
| `higgsfield-youtube-thumbnail` | [higgsfield-ai/skills](https://skills.sh/higgsfield-ai/skills/higgsfield-youtube-thumbnail) (73.7K installs) | `npx skills add higgsfield-ai/skills@higgsfield-youtube-thumbnail` | A generation workflow for the Higgsfield CLI; needs a Higgsfield login. The visible part has no click rules. Page was truncated, not fully read. | **Not for this job.** It makes thumbnails, it does not say which thumbnail to make. |
| `youtube-thumbnail-design` | [101-skills/superpowers](https://skills.sh/101-skills/superpowers/youtube-thumbnail-design) (41.6K installs) | `npx skills add 101-skills/superpowers@youtube-thumbnail-design` | A wrapper for the inference.sh CLI. The same skill is published under five other owner names (qu-skills, magentosh, skills-shell…) with large install counts. | **Do not install.** A tool advert, and the mirrored copies make the install numbers unreliable. |
| `youtube-seo` | [kostja94/marketing-skills](https://github.com/kostja94/marketing-skills) (1,012 stars, MIT) | `npx skills add kostja94/marketing-skills@youtube-seo` | Search optimisation: keyword in the first characters, descriptions, tags. Quotes "89% better CTR" with no source. | **Do not install.** We live on browse and suggested, where search rules do not apply. |
| `curiosity-gap` | [flpbalada/fb-skills](https://github.com/flpbalada/fb-skills) (8 stars) | `npx skills add flpbalada/fb-skills@curiosity-gap` | 2 KB of general principles for headlines and notifications. | **Do not install.** Thin. |
| `youtube-thumbnail` | [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills) (3,734 stars, MIT) | `npx skills add charlie947/social-media-skills@youtube-thumbnail` | Builds a Gemini prompt from the creator's reference photo and brand colours. | **Do not install.** Needs a face. |
| `viral-hook-creator` | [ognjengt/founder-skills](https://skills.sh/ognjengt/founder-skills/viral-hook-creator) (1.8K installs) | `npx skills add ognjengt/founder-skills@viral-hook-creator` | Hooks for X, LinkedIn, Instagram and TikTok posts. Page truncated. | **Do not install.** Social posts, no YouTube titles. |

Already installed on this machine and overlapping: `viral-psychology-hooks`, `marketing-psychology`, `youtube-documentary-valpha`. Check those before adding anything.

**Recommendation:** put sections B and C of this file into the skill as `references/title-psychology.md`, next to the tension test that is already in SKILL.md. That gives us more than any of the skills above.

---

## B. Checklist: 15 rules

1. **The viewer must already know something about the subject, because curiosity is the wish to close a gap in what you know and no gap opens around a thing you have never heard of.** George Loewenstein, "The Psychology of Curiosity", 1994, as summarised in [Kidd & Hayden, Neuron 2015](https://www.sciencedirect.com/science/article/pii/S0896627315007679) (snippet).
2. **Hang the title on a name that is already in the viewer's head: Paddy Galloway's example is "the UN is holding back the Sahara Desert", which works because the UN is "super well known" and "top of mind".** [Creator Science, Paddy Galloway episode](https://podcast.creatorscience.com/paddy-galloway-2/) (read).
3. **"Be familiar, but unexpected": a known subject or format, plus one thing that contradicts what the viewer assumes about it.** Paddy Galloway in [Colin and Samir, The New Rules of YouTube](https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway) (read).
4. **Pair curiosity with fear or with desire: in Jake Thomas's set of 408 outlier titles, 61% carry curiosity, 46% desire and 40% fear, and the usual winner is curiosity plus one of the other two.** [Creator Science #125, Jake Thomas](https://podcast.creatorscience.com/jake-thomas/) (read).
5. **Negative words raise clicks: across about 105,000 headline variants and 370 million impressions on Upworthy, each added negative word lifted click-through by 2.3%, and positive words lowered it.** Robertson et al., [Nature Human Behaviour, 2023](https://www.nature.com/articles/s41562-023-01538-4) (snippet; news headlines, the nearest controlled data we have for titles).
6. **Pick the most extreme true verb: MrBeast's handbook says "I Survived" beats "I Spent" and "in general, the more extreme, the better".** "How to Succeed in MrBeast Production", quoted by [Cybernews](https://cybernews.com/news/mrbeast-leaked-pdf-spills-secrets-how-to-be-successful-on-youtube/) (snippet).
7. **Use a noun the viewer can picture: "I Spent 50 Hours In My Front Yard is lame… but you would click I Spent 50 Hours In Ketchup".** MrBeast handbook, in [Simon Willison's notes](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/) (read).
8. **Superlatives, versus match-ups and three-step comparisons are the three structures Galloway names as steady performers ("World's Fastest Drone vs F1 Car", "$25K vs $25M").** [Colin and Samir](https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway) (read); Aprilynne Alter says the same of adjectives, "especially superlatives", in [Creator Science #196](https://podcast.creatorscience.com/aprilynne-alter/) (read).
9. **A status label everyone understands does the work of a famous name: "Harvard negotiator explains how to argue" scored +553 on Creator Hooks.** [Creator Hooks](https://creatorhooks.com/psychologist-explains-how-to-write-great-youtube-titles/) (read).
10. **One idea per title: "the more commas and the more ands you put in your title… it's just not going to have a focus".** Jake Thomas, [Creator Science #125](https://podcast.creatorscience.com/jake-thomas/) (read).
11. **Stay under about 55 characters and put the hook word first, because the mobile feed cuts titles near 40.** Jake Thomas, same episode (read); the 40 and 60 cut points are from [yt-package](https://github.com/Jakeschincariol/youtube-agent-skill) (read, unsourced there).
12. **Aim between too narrow and too vague: "Nikon B500 review" loses reach, "my favourite camera ever" targets nobody, "best camera for vlogging" works.** Jake Thomas on [Creators on Air](https://www.passionfroot.me/creators-on-air/how-to-write-youtube-titles-to-get-more-views-with-jake-thomas) (read).
13. **The idea has to be understood in under a second, and if it cannot be put into a title and thumbnail it is no longer an idea.** Paddy Galloway, [Creator Science](https://podcast.creatorscience.com/paddy-galloway-2/) (read) and his [five traits thread](https://x.com/PaddyG96/status/1720823481670025613) (snippet).
14. **Take the formula from an outlier in another niche: Thomas's "Do this and you will never hit a fat iron shot" (golf) and "Do this to get them hooked in the early stages of dating" were both outliers on their channels.** [Net Influencer interview](https://www.netinfluencer.com/creator-hooks-jake-thomas-code-on-clickable-youtube-titles/) (read).
15. **The first minute must show that the title's promise will be kept, since the title and thumbnail set the expectation the whole video is measured against.** MrBeast handbook, in [Simon Willison's notes](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/) (read); Galloway calls it "overpromise and overdeliver" in the thread above.

For the thumbnail that sits beside the title: at most three things for the eye (Galloway, glance test), and in vidIQ's study of 500 breakout videos from June 2026, 89% used a face or high contrast and the median text was five words ([vidIQ](https://vidiq.com/research/youtube-thumbnail-study/), snippet). We have no face, so contrast and a famous object have to carry it.

### What makes a subject "recognisable enough" (our reading)

No practitioner gives a threshold. Putting rules 1, 2, 9 and 12 together with Michael's feedback, a title noun passes when a general viewer can do one of three things without help:

- **Name it**: Ferrari, Formula 1, Porsche, the Beetle, Henry Ford.
- **Rank it**: world champion, richest man, world's first, fastest, biggest. The status is known even when the person is not.
- **Picture it**: a tractor, a taxi, a tank, ketchup.

A noun that needs a sentence of explanation fails (a supplier brand, a model code, an engineer's surname outside car circles). Then check the pairing: two recognised things that should not go together make the tension ("champion" and "rejected"). One recognised thing plus one unknown thing makes a label.

### Michael's two examples, explained with the rules

- "The World Champion Formula 1 Rejected": a status everyone ranks (rule 9), a name everyone knows (rule 2), a negative verb (rule 5), and the two contradict (rule 3). Short, one idea (rules 10, 11).
- "The Mechanic Toyota Rejected": "mechanic" has no rank and no face, so rule 1 fails and there is nothing to contradict. Toyota is known, but the viewer has no expectation about whom Toyota hires, so "rejected" breaks nothing.
- "How a Fearless Engineer Built the World's First Car": a superlative that everyone ranks (rule 8), an object everyone pictures (rule 7), and an emotional adjective in place of a biography.
- "How a Loom Maker's Son Built…": "loom maker's son" is a fact the viewer has no prior knowledge of (rule 1) and it is too narrow (rule 12). It would work only after the video has taught them who he is.

---

## C. Word classes

Sourced where a rule above covers it; the rest is our reading and should be tested against outliers with `yt_scout.py search`. Car examples with a fact in [brackets] are unchecked and must be verified before use.

### Classes that test well

| Class | Why | Examples |
|---|---|---|
| Famous proper names | Rule 2. The name is the prior knowledge. | Ferrari, Lamborghini, Porsche, Ford, Formula 1, Le Mans, Tesla |
| Status labels | Rule 9. Rank is understood without knowing the person. | World Champion, Richest Man, Fastest Driver, Harvard, Nobel |
| Superlatives and firsts | Rule 8. | World's First, Fastest, Biggest, Most Hated, Last, Only |
| Negative verbs of fate | Rules 5 and 6. | Rejected, Banned, Destroyed, Killed, Fired, Lost, Humiliated, Stole, Betrayed |
| Extreme, survival-grade verbs | Rule 6. | Survived, Refused, Broke, Crushed (over "spent", "made", "worked on") |
| Emotional adjectives on a person | Alter on adjectives (rule 8); Thomas's "teenage golden retriever" beat "five-month-old golden retriever". | Fearless, Stubborn, Hated, Forgotten, Broke, Illiterate |
| Contradiction and "despite" words | Rule 3. They announce that two known things clash. | "…That Formula 1 Rejected", "Everyone Called Him an Idiot", Without, Until, Never, Still |
| Picturable objects | Rule 7. | Tractor, Taxi, Shed, Tank, Lawnmower |
| Round, concrete numbers | Thomas: "$10,000 a month" beats "make money online"; yt-package: a number, a name or a date beats any adjective. | $1, $1 Billion, 24 Hours, 1 Vote, 300 MPH |
| Insider signals | Thomas: "actually" signals inside information. | Actually, Really, The Real Reason, The True Origin |
| Enemy or rival named | Versus is one of Galloway's three (rule 8). | Ferrari vs Ford, "The Tractor Maker Ferrari [Insulted]" |

### Dead weight

| Class | Why it fails | Examples |
|---|---|---|
| Job titles standing in for a name | Rule 1: no prior knowledge, no rank. | The Mechanic, The Engineer, A Designer, The Supplier |
| Family and biography descriptors | Rule 12: too narrow. Interesting only after the video. | A Loom Maker's Son, A Farmer From Modena, The Apprentice |
| Names known only inside the hobby | Rule 2 fails for the casual and new viewer (Galloway's core, casual, new test). | Model codes (E30, 2JZ, W124), engineers' surnames, supplier brands, Toyota when the story is not about Toyota |
| Topic labels | Thomas: bland statements ("Cooking", "My childhood bedroom") work only for channels with a large audience. | "The History of Toyota", "Toyota: A Documentary", "The Story of the Beetle" |
| Vague hype adjectives | Flagged by yt-package's linter; they claim a feeling and show nothing. | Amazing, Incredible, Insane, Ultimate, Epic, Interesting |
| Neutral verbs | Rule 6: there is a stronger true verb. | Made, Created, Worked On, Developed, Was Involved In |
| Second ideas | Rule 10. | "…and How It Changed Everything", "…and What Happened Next", anything after a second comma |
| Exact but unpicturable numbers and dates | Our reading of rule 12. A year is a fact; it carries no stakes. | "in 1937", "the 1,493 cc engine" |
| Year tags late in the year | Thomas: "in 2023"-style tags work in November to January and fade monthly. | "(2026)" in October |

### What kills a title, in one list

1. A carrying noun the viewer cannot name, rank or picture.
2. Two known things with no contradiction between them.
3. A promise the first minute does not pay (rule 15).
4. Two ideas in one title (rule 10).
5. The hook word after character 40 (rule 11).
6. Thumbnail text that repeats the title's words. Every skill in section A agrees on this, and none gives a source.

---

## Gaps in this research

- No practitioner source states the recognition rule the way Michael did. The closest are Galloway's "super well known" remark and Loewenstein's prior-knowledge condition. The three-way test (name, rank, picture) is ours.
- 1of10 publishes no title study I could find; its findings sit inside the paid tool.
- Creator Hooks' framework archive and Jake Thomas's second Creator Science episode did not load. His per-word data (he scores titles against channel average) would be the best next source.
- Not found: any data set of story titles for history or documentary channels. The quickest proof is our own: run the dead-weight and tests-well lists against last month's outliers in the packaging library.
