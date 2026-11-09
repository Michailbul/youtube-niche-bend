# Video production phases

Michael's shared workflow, set 8 October 2026. Read this when a kept idea enters production for our narrated YouTube films. Individual film status, versions and implementation notes belong in that film's own documentation. Focused revisions to approved work do not restart the whole sequence.

## Cohesion applies at every phase

Michael's standard is **100% alignment between what we hear and what we see**, with the cohesion of premium YouTube creator work. Narration, footage, graphics, motion and sound must communicate the same story moment and feel designed together. Subjects, model identities, facts, numbers, places and time must agree. Visual reveals must land with the relevant spoken words, and music and effects must support their meaning and emotional delivery.

Use the project's established visual DNA and kept premium creator references to judge typography, image treatments, hierarchy, motion, transitions and the mix. Graphics should clarify or demonstrate the narration. All parts must fit the same direction; resolve style drift and generic filler during review.

Critic agents explicitly check each narration beat against its actual footage, graphics and audio timing. Record mismatches against beat IDs or timecodes and fix them before the work is presented for approval. Missing files, uninspected clips and unplayed audio are incomplete evidence; do not certify alignment without reviewing them. Review the first-minute V1 and later cuts with picture and sound together.

## SCRIPT

Start from the kept idea and its packaging. Analyse the competitor/source video and the openings of comparable videos that performed well: the promise, tension, reveal, beat order and payoff. Inspect their actual openings and record the source links, relevant timestamps and checked performance; public views do not establish retention or explain why a hook worked.

Research the subject and check the claims. Bend the proven story structure and hook mechanism into an original script for our subject and audience, preserving source lineage. Write our own words from checked research. A source transcript is evidence, not text to copy.

Always use a separate critic agent, with the project's film-critic brief when it has one (Michael's is `.claude/agents/film-critic.md` in his explainers repo). Give it the actual draft, source/hook evidence and fact notes; revise the script until it reaches at least **9/10**. Show Michael the complete script and obtain his explicit approval of that version before generating voiceover. A critic score and an approved title are not script approval. If wording changes after approval, get the changed script approved again.

## VOICEOVER

Generate narration from the exact approved script. Keep the script version, voice settings and takes together in the film's documentation. Have the independent critic listen to the actual audio and check fidelity to the script, pronunciation, emotional delivery, natural pacing and the opening performance. Revise the take until it reaches at least **9/10** before moving into visual production. A transcript or waveform alone cannot certify the vocal performance; if listening is unavailable, record an incomplete review.

Use the accepted narration as the clock for the boardmatic and edit. Preserve its timings and map the story beats to the spoken words.

## VISUAL DNA

Check the project's existing art direction, kept references and reusable technique packs first.

Use the connected Laniameda Gallery as the starting point for visual inspiration and animation recipes. Verify `check_connection` returns `ok: true` and `authenticated: true`, followed by a successful read. Resolve the current **YOUTUBE CARS** collection and its **Explainer Styles & Skills** shelf through `list_collections`; browse with `list_skills`, and read fitting packs in full with `get_skill`. Inspect their `bodyMedia` and step frames/clips. Browse **Posters & Motion Graphics** and the other current YouTube Cars shelves with asset listings and visual previews. The old **YouTube Docs** folder is a legacy location; follow the live filing. If semantic search fails, use collection and keyword listings and disclose the limitation rather than treating it as lost Gallery access.

- **Visual DNA already exists:** reuse it and go directly to SCOUTING. Do not invent a new direction or repeat the art-direction phase.
- **Visual DNA is missing:** gather references, prepare representative visuals and a timed **boardmatic** (a rough sequence of storyboard frames or placeholders with the accepted narration). Develop the palette, typography, image treatment, motion language and transitions together as an art direction Michael can judge. Use independent critics to check the visual evidence and consistency, and get Michael's direction approval before systematic asset scouting.

A boardmatic is the planning cut. It does not replace the finished first-minute V1.

## SCOUTING

Hunt for video, stock footage, archival material, images and other assets against the narration beats and established visual DNA. Use saved project/Gallery assets and references where they fit. Show actual footage with chronological frames or playable clips so Michael and the critics can judge what it contains.

Saved YouTube competitor videos use the separate `list_video_refs` feature (for example, `collection: "youtube-cars-competitors"`); ordinary asset search does not return them. Keep these research records distinct from the production assets and technique skills filed in YOUTUBE CARS.

For each chosen asset, record its beat, source, useful moment, retrieval location and expected local path; record relevant usage rights or licensing information when available. Retrieve the chosen files and verify they can open. Mark coverage gaps rather than filling them with unrelated material.

Run independent critic agents alongside scouting. They inspect the actual material, cross-check what it shows against the words it would accompany, challenge weak choices and check coverage and visual consistency. The scout cannot certify its own selections. Repair mismatches and complete the timed boardmatic using the accepted assets, preserving the cohesion and picture-word alignment rule above.

## V1 — FIRST MINUTE

Once scouting and preparation are complete, make the first production version cover the first **60 seconds end to end**: accepted narration, finished visual treatment, footage and graphics, purposeful motion, editing, music, sound effects and their mix. Use this minute to prove the film's execution before extending production.

The first **30 seconds must be the strongest possible opening**. Put the most effort into the immediate hook, clear promise, tension and forward movement. Make narration, pictures and sound support the same story moment. The critic reviews the complete minute with sound and separately assesses the first 30 seconds; fix the identified weaknesses and review the revised cut.

Show Michael the playable first-minute V1 with its critic findings and obtain his explicit approval. Do not proceed into producing the remaining minutes until he approves this first minute. This gate follows his script approval; it is a separate decision about the finished execution.

## Continue the film

After first-minute approval, extend the established narration, visual DNA and editing treatment to the rest of the film. Keep independent critic checks during production. Store approved versions, critic findings, unresolved issues and asset retrieval information in the film's own documentation, keeping the shared rules free of film-progress notes.
