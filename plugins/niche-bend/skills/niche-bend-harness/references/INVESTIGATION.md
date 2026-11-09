# INVESTIGATION — how niche bending was actually run

> **History.** Written on Michael's machine during the October 2026 build. Paths are relative to his explainers repo and session ids point to his logs; the plugin layout is in `../SKILL.md`.

Written 22 Oct 2026 from the files and session logs, before any harness code. Paths are relative to
`/Users/eallincreative/michailbul/projects/explainers` unless absolute. Short forms used below:

- `SK` = `.agents/skills/niche-bending-youtube-analyzer/`
- `YT` = `SK/scripts/yt_scout.py`, `FL` = `SK/scripts/format_lab.py`, `RR` = `SK/scripts/research_round.py`
- `FLAB` = `niche-bend/format-lab/`, `OPP` = `research/rounds/2026-10-12-opportunities/`
- `ses_X seq N` = opencode session message, read from `~/.local/share/opencode/opencode.db` (read-only)

Labels: **Observed** = read in a file or log today. **Inferred** = my reading of observed material. **Unknown** = no evidence found.

## 0. Sources read, and what could not be read

| Source | Read? | How |
|---|---|---|
| `SK/SKILL.md` (377 lines), 8 references, 3 scripts, `watch_seeds.json`, `SK/assets/format-lab/` | yes | full text, line numbers below |
| `FLAB` both rounds, `keeps.json`, `KEEPS-NOTE.md`, `server.py`, `rounds.json` | yes | full / parsed |
| `niche-bend/tim-danilov-58-niches`, `art-of-yt-top-100`, `cars-next`, `automotive-legacy-dna`, `unknown-frequencies` | partly | keeps, data fields, reports heads |
| `OPP` (REPORT, FEEDBACK, critic, expansion) | partly | heads, field inventory |
| `3d-timelapse/history-niche/RESEARCH-2026-10-21.md` | partly | §0–2 and scoring table |
| `style-scout/round-01…09`, `3d-timelapse/2026-10-09-warhammer` | keeps only | |
| `.agents/skills/video-idea-proposals/references/how-we-got-here.md` | lessons sections | |
| `git log` on niche-bend / research / skill paths | yes | 24 commits touch the paths |
| opencode `ses_ea1be2fa8ffeBEyi0Ob1Iff6hO` (Quick check-in) | yes | 125 messages, outcome `failed` |
| opencode `ses_e9d226b9cffe0RWqS91sThS40W` (round 2) | yes | 84 messages, all commands extracted |
| opencode `ses_ea21165a3ffeLk6uboCTX3ZQv4` (round 1 triage) | yes | 51 messages |
| opencode `ses_ea0cb6c1bffeuFGqm86uHz1tQB` (script docs) | yes, but empty | 4 messages; the subagent ran one `wc -l` and stopped at 16:06 when its parent session failed. No documentation was produced. |
| Claude Code `~/.claude/projects/-Users-eallincreative-michailbul-projects-explainers/` | user messages only | 9 transcripts; 4 scanned for niche/critic/keep text |
| Claude Code `…-explainers-3d-timelapse/` (4.6 GB) | no | not opened; size |

`opencode export` was not used: there is no `storage/` folder, all sessions sit in `opencode.db` (694 MB), so I queried `session_v2` and `session_message` read-only.

## 1. The method as practised

Two entry points exist on paper (`SK/SKILL.md:125-131`: format first, idea first). In practice, the repeatable routine is the **format lab** (`SK/references/format-lab.md:16-40`, `SK/SKILL.md:300-302`). Round 2 (22 Oct) is the only round whose every command is in a log (`ses_e9d226b9 seq 437-753`); the steps below are that run, with the rule each step comes from.

0. **Read rules and last keeps.** CLAUDE.md, the skill, `no-go.md`, `format-lab.md`, `FLAB/keeps.json` and `KEEPS-NOTE.md` (`ses_e9d226b9 seq 411`; rule: `SK/references/automatic-research.md:8-15`, `no-go.md:3`).
1. **Environment.** Every call ran with `SSL_CERT_FILE=/etc/ssl/cert.pem` (`ses_e9d226b9 seq 437` onward). `timeout` does not exist on this Mac (`seq 450`: "timeout: command not found").
2. **Format watch.**
   ```bash
   S=.agents/skills/niche-bending-youtube-analyzer/scripts/yt_scout.py
   SSL_CERT_FILE=/etc/ssl/cert.pem python3 $S formulas --out niche-bend/format-lab/2026-10-22/formulas.json --table
   ```
   Result: 1,116 videos over 100K from 54 searches, 43 wordings (`FLAB/2026-10-22/formulas.json`, `spec.json.sources`).
3. **Drop phrases, news bursts and no-go.** By reading the list (`format-lab.md:20`). Round 2 dropped "What REALLY Happened" as one news event after a `search` showed every hit was the Flydubai incident (`seq 658-667`, `FLAB/2026-10-22/ROUND.md:39-47`).
4. **Spread on survivors**, one at a time:
   ```bash
   python3 $S spread "how long you'd last in every _" > niche-bend/format-lab/2026-10-22/spread-howlongyoudlastine.json
   ```
   A parallel background loop wrote six empty files (`seq 466`); the sequential rerun worked (`seq 475-524`). Five `spread-*.json` were kept.
5. **Find source videos and channel numbers.** `search` on the exact source titles (`seq 556, 719`), then `channel @a @b … --table` in one call (`seq 493, 710`; rule `SKILL.md:144`).
6. **Frames.** `python3 $S frames <ids> --dir <round>/img --sheet <round>/frames-sources.jpg` (`seq 592, 728`; rule `SKILL.md:82-86`).
7. **Write `spec.json` by hand** (A/B/C per format, three D targets each with `topic` and `cross` search words; shape `format-lab.md:55-72`).
8. **Check D.** `python3 SK/scripts/format_lab.py check <round>/spec.json` → `checks.json` (`seq 617`).
9. **Verdicts by reading `checks.json`** and writing `verdict`/`why`/`proofId` into the spec (`format-lab.md:37`). The agent did this itself.
10. **Build the board.** `python3 SK/scripts/format_lab.py build <round>/spec.json` (`seq 651`), then edited flags and the merge in the spec with inline Python and rebuilt (`seq 744, 753`).
11. **Serve and hand over.** `python3 niche-bend/format-lab/server.py` on 8793; Michael clicks keeps; `POST /save` writes `keeps.json` (`format-lab.md:40`, `SK/assets/format-lab/server.py:7-15`).

Steps the rules require that round 2 skipped (Observed from the session and the files):
- `compare` sizing (`format-lab.md:32-36`): no `compare` call in `ses_e9d226b9`.
- Audience/style fit with `styles`/`tally` (`format-lab.md:38`, `SKILL.md:199-214`): not run in round 2; round 1 has one survey (`FLAB/2026-10-04/cars/survey.json`, 25 videos labelled).
- Three scouts + independent critic (`SKILL.md:26-35`, `cross-verification.md:27-53`): not run in either format-lab round. The verdicts in both specs were written by the proposing agent.
- Gallery save and readback (`SKILL.md:304-309`, `automatic-research.md:127-128`): "Nothing saved to the Gallery yet" (`ses_e9d226b9 seq 780`).

Rounds that did run the full gate: `niche-bend/unknown-frequencies/` (9 Oct: `reports/scout-1-demand.md`, `scout-2-visual-fit.md`, `scout-3-crossing.md`, `critic-reconciliation.md`) and `OPP` (`critic/report.md`, `critic/decisions.json`). Both critics overturned the proposer (section 4.8).

## 2. Script reference

### 2.1 `yt_scout.py` (575 lines, no API key, no yt-dlp; `SKILL.md:99`)

Transport: `get()` (`YT:46-50`) returns the string `'ERR …'` on any exception; `initial_data()` (`YT:52-54`) returns `None` when `ytInitialData` is missing. Callers then iterate an empty dict, so **a 429 or block yields an empty result with exit code 0**. Headers fake a Chrome UA and a consent cookie (`YT:37-38`). Search filters are hard-coded `sp` codes for week/month/year/any × relevance/views/date (`YT:41-44`). Per-call result cap is 30 for internal calls; YouTube returns about 20 per page, no pagination.

| Subcommand | Args (defaults) | Output | Thresholds and constants |
|---|---|---|---|
| `search` | `query --period month --sort views --max 20 --table` (`YT:497-498`) | list of `{id,title,views,age,length,channel,handle,channelId}` (`YT:75-85`) | none |
| `channels` | `query` (`YT:499`) | up to 8 `{name,handle,subs,channelId}` (`YT:87-94`) | handle is read from `subscriberCountText`, subs from `videoCountText` (YouTube quirk, `YT:91`) |
| `channel` | `handles… --thumbs DIR --table` (`YT:500`) | subs, videoCount, joined, ageMonths, totalViews, `latest` (RSS 15), medianViews, bestRecent, bestOverMedian, uploadsPerWeek, daysSinceUpload, bestViewsPerSub, over100K, `checks` (`YT:96-151`) | 3 retries, 1.5 s sleep (`YT:99-109`); Shorts excluded from median when any long exists (`YT:128`); 0.5 s between channels (`YT:571`) |
| (checks) | | `firstVideoUnder6Months`, `median50K`, `stillPosting`, `notOneHit`, `freshRatio` (`YT:153-168`) | first video ≤ 183 days, only when videoCount ≤ RSS size (`YT:158-161`); median ≥ 50,000 (`YT:163`); last upload ≤ 14 days (`YT:164`); best ≤ 10× median **or** ≥ 3 of latest over 100K (`YT:166`); best ≥ 5× subs (`YT:167`). Faceless, not-too-big, makeable, monetisation are not computed. |
| `demand` | `query --channels 12` (`YT:501`) | month and year lists, `summary` {videos, over50K, over100K, over1M, channelsOver50K, channelsWith2PlusOver50K, smallChannelHits, topViews}, `reading` (`YT:190-240`) | relevance and views sorts, 30 each; views-sorted hits must contain the first 2 non-stop words, relevance hits the first 1 (`YT:202-203`); drops < 180 s and streams (`YT:204`); small = subs < 100K and views ≥ 50K (`YT:223`); demand reading cascade (`YT:231-235`): year over100K = 0 → "no demand"; month over50K = 0 → "cold"; smallChannelHits ≥ 2 → "open demand"; month over100K ≥ 3 → "held by established"; else "thin". Saturation (`YT:236-238`): channelsWith2PlusOver50K ≥ 3 or channelsOver50K ≥ 8 → crowded; channelsOver50K ≥ 3 → contested; else open. Subs looked up for 12 channels, 0.4 s apart (`YT:213-214`). |
| `compare` | `topics… --channels 12`; topic = `a\|b=Wiki_Article` (`YT:507`) | per topic: monthUploadsSeen, monthOver100K/1M, monthTop20Views, monthMedianTop10, smallChannelHits, smallChannelBest, smallChannelThird, smallShareOfTop20, yearOver100K/1M, yearTop, top 8, `wikipedia` (`YT:266-303`) | views-sorted hits need any topic word in title/channel/handle (`YT:281`); subs for first 40 month videos, max 12 channels (`YT:286-288`); Wikipedia: last 30 days vs previous 11 months, end = today − 2 days (`YT:242-257`); trend > 1.3 = "now" (`YT:244`, `format-lab.md:35`) |
| `spread` | `formula --need words --table` (`YT:504`) | month and restOfYear {videos, channels, over100K, views}, `monthShare`, `reading`, examples (`YT:305-335`) | must-contain = formula words > 2 letters not in stop list (`YT:310`); month over100K < 3 → thin; share ≥ 0.7 → new and spreading; ≥ 0.2 → established; else past peak (`YT:327-330`). "Year" search includes the month; month ids are removed from it (`YT:321-322`). |
| `formulas` | `--seeds watch_seeds.json --out --min-views 100000 --table` (`YT:505-506`) | `{videosOver100K, searches, wordings[{wording, channels, views, nichesSeen, inCars, examples}]}` (`YT:342-387`) | month only, views + relevance sorts (`YT:351-352`); ≥ min-views, ≥ 180 s (`YT:353-354`); titles with > 30 % non-Latin letters dropped (`YT:355-356`); numbers become `N` (`YT:339`); 3- to 6-word n-grams with ≥ 2 content words (`YT:369-372`); **min_channels = 3 is fixed in code**, the CLI cannot change it (`YT:342, 521`); longest phrasing kept per group (`YT:383-385`); table shows top 40 (`YT:525`); 0.25 s between calls (`YT:362`) |
| `sheet` | `query out.jpg --period month --sort views --max 24` (`YT:502-503`) | JPEG contact sheet 4 columns of 320×180 + list (`YT:389-405`) | mqdefault thumbnails |
| `frames` | `ids… --dir img --sheet` (`YT:511`) | `<id>_1..3.jpg` at 640 px, optional sheet (`YT:407-440`) | YouTube's own stills at about 25/50/75 % (`YT:408`); 4:3 fallbacks cropped to 16:9 (`YT:422-423`); files under 3,000 bytes rejected (`YT:420`). They do **not** show the opening (`automatic-research.md:91-93`). |
| `styles` | `queries… --out DIR --period year --top 24 --min-views 50000` (`YT:508-509`) | `DIR/survey.json`, `DIR/img/`, `styles-N.jpg` sheets of 8 (`YT:442-478`) | `style` field left blank for a human (`YT:466`) |
| `tally` | `survey.json --table` (`YT:510`) | per style: videos, medianViews, topViews, smallChannelVideos, channels (`YT:480-489`) | small = subs < 100K |

Watch seeds (`SK/scripts/watch_seeds.json:3-22`): 13 niches × 3 broad words (cars is one of them) + 15 title shapes = 54 searches, which matches round 2's "54 searches".

### 2.2 `format_lab.py` (80 lines)

| Command | Reads | Writes | Notes |
|---|---|---|---|
| `check <round>/spec.json` (`FL:25-41`) | `spec.formats[].targets[].topic/cross` | `<round>/checks.json` keyed `format\|niche`: topic, summary, reading, top 6 month videos, `cross` top 6 | calls `demand(topic, 8)` (`FL:32`) and one `search(cross, year, relevance, 20)` with ≥ 180 s (`FL:34-35`); **resumes**: skips keys already present (`FL:30-31`) and writes after each target (`FL:40`). The `cross` list is a relevance search, so it is not title-matched. |
| `build <round>/spec.json` (`FL:43-76`) | spec, checks | `lab.json`, `img/`, and **overwrites `index.html` and `server.py` one folder up** from `SK/assets/format-lab/` (`FL:69`); updates `rounds.json` (`FL:70-73`); creates `keeps.json` only if missing (`FL:74-75`) | fills channel numbers only for `@handle` sources without `median` (`FL:51-56`) |

### 2.3 `research_round.py` (182 lines)

| Command | Args | Output | Rules in code |
|---|---|---|---|
| `collect` (`RR:26-76`) | `--out`, `--queries 6` (1-20), `--channels 6` (0-12) (`RR:168-171`) | `research/rounds/<YYYY-MM-DD>/<HHMMSS>/collection.json` (`RR:46, 72`), status `partial` when any error (`RR:69`) | wraps `get`/`initial_data` so ERR and missing data **raise** (`RR:32-44`), which is the fix for the silent-empty problem in `YT:46-54`; rotates queries by date ordinal (`RR:49-50`); **excludes the cars niche** from the rotation (`RR:48`); keeps ≥ 100K, ≥ 180 s (`RR:57`); exit 1 only if no search succeeded (`RR:76`) |
| `validate <payload.json>` (`RR:79-162`) | Gallery batch | `{ok, errors}` | 1-12 items (`RR:84`); 12 required fields (`RR:90-92`); agentDescription ≤ 45 words (`RR:98`); collection must be `youtube-niche-bend` or `youtube-style-map` (`RR:100`); **checkedAt within 24 h** (`RR:108`); packaging source ≤ 30 days (`RR:125`); 1-3 bends (`RR:127`); verdict enum Confirmed/Open/Contested/Crowded/Weak/Untested (`RR:131`); three first-30 beats (`RR:133`); ≤ 3 evidence videos with 11-char ids (`RR:135-141`); **Confirmed/Open require `audienceFit = Supported`** (`RR:149-150`); external demand with https URL (`RR:154-156`); `passes-filters` only for Proven (`RR:158`) |

Observed: no `research/rounds/<date>/<HHMMSS>/collection.json` exists on disk (22 Oct), so `collect` appears never to have been run in this checkout. Inferred: round 2's three Open verdicts would fail `validate` because no audience fit was checked (`RR:149-150`).

### 2.4 Board server (`SK/assets/format-lab/server.py`, 23 lines)

Static files plus `POST /save`, which replaces `keeps.json` with the request body (`:7-15`). Port 8793 hard-coded (`:23`). No history, no author field, no merge.

## 3. The rounds

"Kept by Michael" means a file written by a board click, unless marked agent.

| Date | Folder | Question | Output | Verdict source | Keeps | Film? |
|---|---|---|---|---|---|---|
| 3 Oct | `style-scout/round-01`, `02-openings` | which looks and openings to use | style refs, Gallery saves | n/a | r01 `board/keeps.json` empty; r02 8 openings kept | style input |
| 4 Oct | `niche-bend/tim-danilov-58-niches` | re-check Danilov's 44 channels | 10 pass, 14 under 10K median, 9 presenters (`references/danilov-method.md:79-84`) | agent | 1 channel: `@unknownfrequencies-tv` (`keeps.json`, 4 Oct 14:40) | led to the 9 Oct UF round |
| 4 Oct | `niche-bend/art-of-yt-top-100` | verify paid top-100 list | 100 → 48, 8 pass (`ses_ea1be2fa seq 892`) | agent | 0 (`keeps.json` `{"channels":[]}`) | no |
| 4 Oct | `niche-bend/cars-next` | idea-first car packages | ~30 packaged ideas, free-text demand/sat (`data*.js`) | agent | **11 ideas** clicked, saved 2026-10-04T14:06Z | **yes: `beetle` → Beetle film** (`how-we-got-here.md:163-175`) |
| 4 Oct | `FLAB/2026-10-04` | format lab round 1 | 10 cards, 30 targets, 3 merges | agent, no critic | **none for 17 days**; agent triage 21 Oct: 4 formats, 5 bends (`keeps.json`) | no |
| 4-7 Oct | `style-scout/round-03…09` | craft references | ~200 refs; keeps in r05-07, r09; r03, r04 empty | n/a | yes (technique library) | style input |
| 5 Oct | `niche-bend/automotive-legacy-dna` | car visual DNA modules | board :8816 | n/a | 0 (`{"modules":[]}`) | no |
| 9 Oct | `niche-bend/unknown-frequencies` | bend the UF format | 5 bends + 3 leads, 3 scouts + critic | **independent critic** | none found | no; critic rejected A-D, 0 supported |
| 9 Oct | `3d-timelapse/2026-10-09-warhammer` | Warhammer 3D/scale | 4 data waves | agent | 0 (`{"videos":[],"titles":[]}`) | fed 12 Oct expansion |
| 12 Oct | `history-channel/` (worktree `.codex-worktrees/history-cartoon-2026-10-12`) | cartoon history channel | 34 channels, 13 formats; critic 8.2/10 (`ses_ea21165a seq 228`) | critic | 0; Michael scored the first report 6/10 (`how-we-got-here.md:185-188`) | no |
| 12-13 Oct | `OPP` + `OPP/expansion` | rank current 3D and 2D formats | 144 refs, 28 packages, 10 directions (`critic/decisions.json`) | **independent critic**, changed the ranking (`OPP/critic/report.md:3-5`) | no keep file; "no validated pilot" | **Inferred yes**: persistent-place 3D → `3d-timelapse/history-niche/RESEARCH-2026-10-21.md` picked Carthage; render exists, final mux broken (`ses_e9d226b9 seq 373`) |
| 19 Oct | `2d-animations/v2` (commit `b789bf1f`) | history bends, teardown | 10 bends, 3 critic passes | critic | outside this audit | Unknown |
| 21 Oct | `3d-timelapse/history-niche/RESEARCH-2026-10-21.md` | which city for a 1M 3D timelapse | weighted 6-criterion rubric, Carthage 88 (`:77-102`) | single author | Carthage built | yes (Carthage, unpublished) |
| 22 Oct | `FLAB/2026-10-22` | format lab round 2 | 4 cards, 12 targets, 1 merge (`ROUND.md`) | agent, no critic | **none** | no |

Counting only the niche-bend boards and format-lab rounds gives the "nine rounds, one film" line in `niche-bend/tasks/2026-10-22-niche-bend-harness.md`. Counting the 12 Oct → 21 Oct chain gives a second film in production. Michael should say which count he uses (section 7).

## 4. Errors and failure modes seen

| # | Failure | Evidence | Workaround used | Harness rule |
|---|---|---|---|---|
| 4.1 | **Server restarts** kill work and questions | 5 synthetic "server restarted" messages in `ses_ea21165a` (seq 238-299), 9 in `ses_ea1be2fa` (seq 319-1021); the plan session ended `failed` with "Failed to execute statement" (seq 1023); "the question tool keeps getting killed" (`ses_ea21165a seq 259`) | boards restarted under `nohup` (seq 391); decisions written to files | state on disk, one artifact per step, resume from the last complete artifact |
| 4.2 | **Unjudged rounds** | `FLAB/keeps.json` empty 4-21 Oct (`KEEPS-NOTE.md:8`); empty keeps in art-of-yt, automotive-legacy-dna, warhammer, history-channel, style-scout r01/r03/r04 | none; the agent eventually triaged round 1 itself | the loop stops at the gate and shows the queue age |
| 4.3 | **Agent self-keeps** | `KEEPS-NOTE.md:6` "proposed by the agent, not clicked by Michael"; the agent wrote `keeps.json` directly (`ses_ea21165a seq 407`) | labelled in a note file only; `keeps.json` itself carries no author | keeps need an author field; agents write proposals elsewhere |
| 4.4 | **keeps.json and its note disagree** | `KEEPS-NOTE.md:21` lists merge `feared-car-on-canvas` as kept; `FLAB/keeps.json` has `"merges": []` (read 22 Oct); `ses_ea21165a seq 400` showed the merge present on 21 Oct | none | Inferred: a later save or rebuild dropped it. Keeps must be append-only with a log. |
| 4.5 | **Builds clobber board code** | `FL:69` copies `index.html`/`server.py`; working-tree `FLAB/server.py` lost the `/research/rounds/2026-10-12-opportunities/` routing that is in git (`git diff`); `/round/2026-10-22` returned 404 (`ses_e9d226b9 seq 676-694`) | none | generated board files separate from hand-edited ones |
| 4.6 | **Lost clicks on reload** | "Reloading a board while Michael has unsaved keeps … his clicks were lost" (`how-we-got-here.md:160`); `server.py:12` replaces the file wholesale | none | gate writes are appends, never replaces |
| 4.7 | **Silent empty results under throttling** | `YT:46-54` swallows errors; six empty `spread` files from a parallel loop (`ses_e9d226b9 seq 466`); `/watch` 429 after a few hundred reads (`SKILL.md:123`); hosted storyboard 403 (`OPP/REPORT.md`, critic report) | sequential reruns; `RR:32-44` raises instead; "stop at the first 429" (`automatic-research.md:164-166`) | every query logged with status; empty ≠ zero |
| 4.8 | **Self-certified verdicts** | both format-lab specs carry Open/Confirmed written by the proposer; 8 of 12 "Open" targets have a script saturation reading of contested or crowded (e.g. Used cars: 12 channels over 50K, `FLAB/2026-10-22/checks.json`); where an independent critic ran, it rejected 4 of 5 UF bends including "The ENTIRE History of Formula 1" (`unknown-frequencies/reports/critic-reconciliation.md:11-20`), which round 1 had as Contested; `OPP` critic: "No exact H1-H5 pilot earned a validated … verdict" (`OPP/critic/report.md:5`) | none in format lab | VALIDATE verdicts come only from a separate critic run |
| 4.9 | **Stale paths** | `.claude/launch.json` had 34 `/Users/michael/AI-video-work/…` args, fixed 21 Oct (`ses_ea21165a seq 364-373`); 3 remain (`launch.json:8,16,154`, other repos); `SKILL.md:102` uses `.claude/skills/…` (works only through the symlink in `.claude/skills`) | rewrite script | resolve all paths from the repo root at run time |
| 4.10 | **Port collisions and drift** | Danilov board defaults to 8791 (`launch.json:164`), 8791 was taken by the Middle-earth server, so the board moved to 8792 via `PORT` (`ses_ea1be2fa seq 892`); `LINKS.md` lists 8792 | manual `PORT=8792` | one port registry |
| 4.11 | **Gitignored research** | `.gitignore:31` ignores `/niche-bend/`; only 9 files under it are tracked (format-lab `latest.html`, `server.py`, harness 5, tasks 2); every spec, check, keep and note has no git history; `img/` folders were found empty and 3,600+ images re-fetched with `niche-bend/refetch_images.py` (`ses_ea1be2fa seq 892`); `how-we-got-here.md:161` warns against referencing `niche-bend/` from a skill | re-fetch script | harness state needs a tracked or backed-up home; a new `INVESTIGATION.md` here needs `git add -f` |
| 4.12 | **Snapshot and disk bloat** | `~/.local/share/opencode/snapshot` is 69 GB; snapshots tracked `yt-deepseek-2/.venv/…` (`ses_ea1be2fa` tool parts); `niche-bend/` is 430+ MB, `research/` 447 MB, `FLAB/2026-10-04/img` 42 MB for 552 files | none | runs reference image paths; no copies |
| 4.13 | **Usage limits** | "[Usage limit reached …]" three times in Claude transcript `0b12ef33…jsonl` (9-10 Oct) | none | runs must stop cleanly with a partial artifact |
| 4.14 | **Deleted channels** | `@hex-tvs`, `@historicdave1` gone by 21 Oct (`ses_ea1be2fa seq 892`) | placeholder tiles, `unavailable` flag | re-check before reuse |
| 4.15 | **Numbers age between rounds** | round 1 numbers read 4 Oct, triaged 21 Oct (`KEEPS-NOTE.md:4`); snapshots differ: CityEons 1.41K subs on 12 Oct (`OPP/REPORT.md`) vs 3,100 on 21 Oct (`RESEARCH-2026-10-21.md` §1.1) | flagged in prose | each number stores its `checkedAt` and query |
| 4.16 | **Wrong flags at small n** | `notOneHit=true` with n = 1 (`YT:166`; `OPP/critic/report.md`, corrections list) | critic caught it | require n ≥ 3 before the check counts |
| 4.17 | **Car bias** | skill said "cars first" when loaded 9 Oct (Claude transcript `08081838…`); changed 19 Oct (`SKILL.md:8`, CLAUDE.md:46); most format-lab targets are car niches; meanwhile `RR:48` excludes cars from rotation | rule edit | target niches ranked by evidence |
| 4.18 | **Script reading and verdict measure different things** | `demand()` reading measures topic saturation (`YT:236-238`), the verdict table measures the exact crossing (`format-lab.md:42-51`); the `cross` list is an unmatched relevance search, so its views count off-topic videos (`FL:34`) | human reading | Y axis must be title-matched |

## 5. Lessons as rules for the harness

1. **Every step writes a file before the next starts.** Evidence 4.1, 4.13. The plan session died one message after "Starting with the investigation".
2. **The keep gate is append-only and has an author.** `keeps.json` records who (`michael` or `agent-proposal`), when, and from which round; the server appends. Evidence 4.3, 4.4, 4.6.
3. **Agent proposals never count as keeps.** Round 1's triage stays a proposal until Michael clicks. Evidence 4.3, `STATE.md` risks.
4. **VALIDATE verdicts are written only by a separate critic run**; the proposer's verdict is stored as `proposedVerdict`. If no independent agent is available, the candidate stays Untested (`cross-verification.md:50-53`). Evidence 4.8.
5. **Empty is not zero.** Each query records status ok / empty / error; a run with errors is `partial`. Use `RR`'s strict wrappers (`RR:32-44`) for every `YT` call. Evidence 4.7.
6. **No parallel YouTube calls; stop at the first 429.** Evidence 4.7, `automatic-research.md:164-166`.
7. **Same wording, same day for every axis number.** Each point stores query, period, sort, checkedAt. Evidence 4.15, `cross-verification.md:80-100`.
8. **Generated board files are separate from hand-edited ones**; builds never overwrite a server. Evidence 4.5.
9. **Dedupe against previous rounds and `no-go.md`, including the "car crossing is dead" table** (`no-go.md:64-84`). Evidence: round 1 re-proposed car crossings that had 324 and 87 views.
10. **Rank targets by evidence, any niche.** Evidence 4.17.
11. **Reference images by path; never copy.** Evidence 4.12.
12. **Keep demand, saturation and failed attempts as separate numbers on the point**; show them separately on hover. Evidence `SKILL.md:197`, `cross-verification.md:96-98`.
13. **Show the queue age at the gate** (days since a round was written without a keep). Evidence 4.2: 17 days for round 1.
14. **Resolve paths from the repo root and ports from one registry.** Evidence 4.9, 4.10.
15. **The harness folder is git-ignored**; decide where state is backed up before rails run. Evidence 4.11.
16. **Faceless and makeable are frame judgments**; no script field computes them (`YT:153-154` docstring). The Frame Reader artifact is required before fit gets a value.
17. **A report leads with pictures and the decision** (`how-we-got-here.md:185-197`): Michael rejected text piles twice.

## 6. Data available for the 3D space

### 6.1 What exists

| File | Fields | Coverage | Axis use |
|---|---|---|---|
| `FLAB/2026-10-04/checks.json`, `FLAB/2026-10-22/checks.json` | per target: `summary.month` / `summary.year` {videos, over50K, over100K, over1M, channelsOver50K, channelsWith2PlusOver50K, smallChannelHits, topViews}; `reading.demand`, `reading.saturation`; `top[6]`, `cross[6]` {id,title,views,age,handle,subs,length} | 30 + 12 = **42 targets**, read 4 Oct and 22 Oct | X and Y; the only numeric per-target set |
| `FLAB/*/spec.json`, `lab.json` | `targets[].verdict/why/proofId`, `source` {views, subs, median, over100K, sample, date}, `flags` | 42 targets + 4 merges | colour (verdict), size (source date) |
| `FLAB/2026-10-22/spread-*.json` | `monthShare`, `month/restOfYear` {videos, channels, over100K, views}, `reading` | 5 formulas | format freshness |
| `FLAB/2026-10-22/formulas.json` | `wordings[]` {channels, views, nichesSeen, inCars} | 43 wordings, 1,116 videos | DISCOVER input |
| `FLAB/2026-10-04/cars/survey.json` | `videos[]` {views, subs, viewsPerSub, style} | 25 car-history videos, all labelled | fit evidence, one niche only |
| `niche-bend/unknown-frequencies/evidence/scout-1-demand/compare.json` | `compare` output (monthTop20Views, smallChannelBest/Third, smallShareOfTop20, wikipedia) | one round, 9 Oct | X alternative |
| `OPP/critic/decisions.json` | `directions[]` {rank, confidence (text), strongestFailureReason, cheapNextCheck, titlePairs} | 10 directions | colour; no numbers |
| `OPP/expansion/directions.json` | `ideas[]` {demand, saturation, verdict, priority} as **free text** | 28 packages | needs re-measure |
| `OPP/expansion/scale-crossing/evidence.json` | videos {views, channelSubscribers, channelLongFormMedian, facelessStatus, coverage} | 8 videos | fit evidence |
| `niche-bend/cars-next/data*.js` | ideas {demand, sat, verdict} as free text | ~30 ideas | needs re-measure |
| `niche-bend/art-of-yt-top-100/final.json` | channels {medianViews, subs, over100K, uploads30d, passes, checks} | 100 channels | source scorecard |
| `3d-timelapse/history-niche/RESEARCH-2026-10-21.md` §2 | 6-criterion weighted score incl. "Format openness" | 6 cities, one author | example only; not independent |

No file holds a numeric fit value. No two rounds were read on the same day.

### 6.2 Proposed normalisation (0-100)

All three are computed from a fresh, same-day `demand` + exact-title search per point, with fixed query templates (`<topic>` and `<topic> history|explained`, `cross-verification.md:85-87`). Old numbers may seed the board but are drawn as "stale" until re-read.

- **X demand** = 0.6 × L(month.topViews) + 0.4 × min(month.smallChannelHits / 3, 1) × 100, with L(v) = clamp((log10 v − 4) / 3, 0, 1) × 100 (10K → 0, 10M → 100). Small-channel hits are weighted because they are "the signal that matters most" (`SKILL.md:177`). Caveat: views-sorted search drifts off topic (`format-lab.md:53`); Rockets has month.topViews 3.7M with reading "no demand shown" in `FLAB/2026-10-04/checks.json`. Only title-checked videos may count.
- **Y saturation** = min(100, 34 × successful exact-crossing copies), where a copy is a title matching the bent formula with ≥ 50K views in the year, deduplicated by channel. Use the script's topic reading only as a fallback band (open 0-33, contested 34-66, crowded 67-100, `YT:236-238`). **Failed copies** (matching title, < 5K views) are stored as `failedAttempts` and lower confidence; they are evidence against the transfer (`no-go.md:66-68`), not saturation. Caveat: today's `cross` field is unmatched (4.18), so no current file supports Y without a re-read.
- **Z fit** = makeable (100 / 50 / 0 from `format-families.md` "Makeable by us" Yes / Partly / No, judged from frames) × audienceFit (Supported 1.0, Partial 0.6, Mismatch 0.1). **Unknown** gets no value: the point is drawn on the floor plane as hollow. Caveat: a product of two judgments is a blended score, which `SKILL.md:197` and `cross-verification.md:96-98` forbid for demand and saturation; hover must show both parts. Fit is a judgment; it is not a measurement of the audience (`cross-verification.md:178-181`).
- **Size (freshness)** = clamp(1 − sourceAgeDays / 30, 0.15, 1) for packaging sources (`SKILL.md:92`).
- **Colour (confidence)** from the critic's verdict only: Confirmed/Open with critic = green; Untested or no critic = amber; Weak/Reject/Crowded = red. Proposer verdicts render grey.

Honest limits: counts describe the searched sample, not market size (`cross-verification.md:90-92`); ~20 results per search; one locale (en-US headers, `YT:37-38`); public views say nothing about CTR, retention or audience (`cross-verification.md:98-100`).

## 7. Open questions for Michael

1. Do the round 1 agent keeps stand until you click, or should the board show them as proposals only?
2. Is `feared-car-on-canvas` kept? The note says yes, `keeps.json` says no (4.4).
3. Round 2 is undecided: judge it on the board first, or let the harness re-run VALIDATE with a critic before you look?
4. Does "one film from nine rounds" count Carthage (12 Oct research → 21 Oct report → render)?
5. The skill says Gallery is the output and no new boards (`SKILL.md:306-309`, `automatic-research.md:6`); the harness plan adds a 3D board. Is the 3D board an approved exception, and should it live inside the format-lab board or `harness/board/`?
6. Fit as a product of makeability × audience fit: acceptable on the axis, or keep them as two separate dimensions (and drop to a 2D view plus colour)?
7. `niche-bend/` is git-ignored. Where should harness state and run ledgers be backed up?
8. Rails cadence: every three days now, or manual until three runs are trusted? Cloud research is still paused (`cross-verification.md:186-189`).
9. What did you mean by "the 8789" in the request (`ses_ea1be2fa seq 933`)? No board uses port 8789 in `.claude/launch.json`; the format lab is 8793.
