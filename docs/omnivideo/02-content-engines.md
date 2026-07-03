# 02 — Content Engines

The six production engines, in pipeline order. Each engine is a Claude-driven stage with defined inputs, outputs, and scoring rules.

---

## 1. Content Discovery Engine

**Goal:** produce a ranked list of content opportunities daily, blending fast-moving trends with durable evergreen demand.

### Signal sources

| Signal | Source | Cadence | What it finds |
|---|---|---|---|
| Trending topics | Google Trends (rising queries), YouTube trending + search suggest, Reddit hot posts, X trends | 3×/day | Timely spikes |
| Evergreen topics | Keyword tools (search volume stable ≥12 months), "top questions" scrapes, own back-catalog winners | weekly | Durable demand |
| Underserved topics | High search volume ÷ low count of quality recent videos (search top-20 results: check age, view velocity, production quality) | weekly | Gaps to own |
| Viral patterns | Outlier detection on competitor uploads: views ÷ channel median >5× within 72h | daily | Formats/hooks to adapt |
| Competitors | RSS/API watch on 10–30 channels per niche: new uploads, title patterns, cadence | daily | Positioning intelligence |
| Audience | Own comments, community posts, FAQ mining | daily | Direct demand |

### Scoring model (per topic, computed by Claude with the rubric below, calibrated by the Learning System)

- **Opportunity score (0–100)** = `0.30·trend_momentum + 0.25·audience_size_norm + 0.20·niche_fit + 0.15·(100 − competition) + 0.10·evergreen_bonus`
- **Competition score (0–100):** density and strength of existing coverage — number of videos <6 months old in top results, median channel size covering it, quality of the best incumbent.
- **Revenue potential:** est. views × niche RPM × format multiplier (long-form ≈ 5–10× Shorts RPM), plus affiliate/sponsor fit flags.
- **Audience size:** normalized monthly search volume + social mention volume.
- **Difficulty:** research burden (contested claims? expert domain?) + production burden (needs custom diagrams? long-form?).

Daily output: top N topics per niche (N = niche `daily_quota`), each with all five scores and a one-line "why now" rationale. Everything else stays in the backlog and is re-scored weekly (trend components decay; evergreen components persist).

---

## 2. Research Engine

**Goal:** turn an approved topic into a verified research brief the Script Engine can trust.

### Process

1. **Gather** — web search (top articles, primary sources, papers, official stats), transcripts of the 3 best existing videos on the topic, relevant Reddit/forum threads.
2. **Extract** — Claude pulls candidate facts, each tagged with source URL and a reliability tier (T1 primary/official, T2 reputable secondary, T3 anecdotal).
3. **Cross-check** — every fact used in the brief needs either one T1 source or two independent T2 sources. Claude explicitly searches for contradicting claims for each headline statistic.
4. **Flag** — facts failing the check are kept but marked `weak_evidence`; the Script Engine may only use them with hedged language ("some studies suggest"), and QC verifies the hedge survived.

### Brief output (stored in `Briefs`)

- **Key facts** (5–15, each with source + tier)
- **Statistics** (with year — stale stats are a top accuracy failure mode)
- **Story angles** (3–5: e.g., origin story, myth-busting, "what nobody tells you", comparison, timeline)
- **Contrarian insights** (defensible positions against conventional wisdom — highest-performing hook material)
- **FAQs** (from People Also Ask, Reddit, comments — each is a potential Short)
- **Weak-evidence flags** and open questions

---

## 3. Script Generation Engine

**Goal:** retention-engineered scripts in five duration classes, multiple variants each for A/B testing.

### Duration classes & structure

| Class | Structure | Word budget |
|---|---|---|
| 15s | Hook (0–2s) → single payoff → loop-friendly ending | ~40 |
| 30s | Hook → setup → payoff → twist/CTA | ~80 |
| 60s | Hook → curiosity gap → 2–3 beats → resolution → CTA | ~160 |
| 3min | Hook → roadmap tease → 3 chapters with mini-payoffs → synthesis → CTA | ~450 |
| 10min | Cold open → stakes → chaptered narrative with open loops → climax → resolution → next-video bridge | ~1500 |

### Retention engineering (required elements, checked by QC)

- **Hook:** first line must create an information gap or pattern interrupt; never start with "Hi" / topic announcement. Generate 5 hook candidates, pick 2 for A/B.
- **Curiosity gap:** promise made in the hook must be explicitly resolved — unresolved gaps destroy trust and are blocked by QC.
- **Retention triggers:** every 20–30s (long-form) insert a re-hook: open loop, visual change cue, "but here's the part nobody mentions", numbered progress markers.
- **Narrative structure:** prefer story spine (situation → complication → resolution) over listicle when the brief has a story angle.
- **Strong ending:** end on payoff or loop point, not a fade-out; CTA is one sentence max and earned.

### Output format

Scripts are structured JSON — `scenes[]`, each with `voiceover_text`, `visual_direction`, `on_screen_text`, `broll_suggestion`, `duration_estimate` — so the Visual and Assembly engines consume them directly. 2–3 variants per duration class differing in hook + angle (not just wording), tagged for A/B assignment at publish time.

---

## 4. Visual Creation Engine

**Goal:** every scene gets a visual matched to its `visual_direction`, produced by the cheapest tool that meets the quality bar.

### Workflow routing (per scene type)

| Scene need | Tool | Workflow |
|---|---|---|
| AI images (scenes, characters, backdrops) | Flux via API (fal.ai/Replicate) or Midjourney | Style-reference image per niche for brand consistency; 2 candidates per scene, Claude picks |
| Motion graphics (kinetic text, transitions, branded intros) | Creatomate/Shotstack templates; After Effects templates rendered via Plainly for hero content | Template library keyed by scene type; Claude fills template slots |
| Explainer animations | Template-based character/scene systems (e.g., animated stock from Artlist/Storyblocks) + Ken Burns on stills; Runway/Kling image-to-video for hero moments | Reserve generative video for the top 10% of content (cost) |
| Infographics | Claude generates chart spec → QuickChart/Recharts render → branded frame | Fully deterministic, cheap |
| Diagrams | Claude generates Mermaid/Graphviz → render → styled | Fully deterministic |
| Educational visualizations | Claude writes Remotion (React) component from a vetted library of 10–15 visualization patterns | Highest quality per dollar at scale |
| Thumbnails | Flux portrait/scene + template text layer (3 concepts per video, A/B via YouTube's Test & Compare) | Face + emotion + ≤4 words rule |

**Consistency system:** each niche has a visual bible (palette, font, style-reference images, watermark). All generation prompts inject it; QC rejects off-brand assets.

---

## 5. Voiceover Engine

**Goal:** consistent, human-quality narration in multiple voices and languages.

- **Narrator identities:** 2–4 cloned/designed ElevenLabs voices per niche (e.g., "authoritative explainer", "energetic storyteller"). Voice ID is pinned per channel — consistency builds parasocial trust.
- **Emotion control:** script JSON carries per-scene `tone` tags (curious, urgent, warm, deadpan); mapped to ElevenLabs stability/style settings. v3 audio tags for laughter/pauses where supported.
- **Educational vs. storytelling tone:** two delivery presets per narrator — measured pace + neutral pitch contour for educational; wider dynamics + shorter sentences for storytelling. Script Engine tags which preset applies.
- **Multilingual:** top-performing videos (top 10% by watch time) auto-localized — Claude translates + culturally adapts the script (idioms, examples, units), same narrator voice via ElevenLabs multilingual model, subtitles regenerated. Launch order by RPM/size: Spanish, Portuguese, Hindi, German, Japanese.
- **QC:** pronunciation dictionary per niche (names, jargon); Whisper re-transcription diffed against script to catch TTS errors before assembly.

---

## 6. Video Assembly Engine

**Goal:** deterministic, fully automated assembly from script JSON + assets to platform-ready exports.

### Pipeline

1. **Scene build:** for each scene, pair voiceover audio (duration = ground truth) with its visual; apply motion preset (zoom/pan for stills).
2. **Visual↔script matching:** already guaranteed by scene-keyed assets; a Claude spot-check compares scene text vs. a frame description for mismatches.
3. **Subtitles:** AssemblyAI word timestamps → animated word-by-word captions (Shorts/Reels) or clean line captions (long-form); styled per niche visual bible.
4. **Transitions:** rule-based — hard cuts within a beat, whip/slide between chapters; never more than one transition style per video.
5. **Music:** licensed track selected by mood tag from script; auto-ducked −12 dB under voiceover; SFX from a whitelisted library on emphasis markers the Script Engine embeds.
6. **Export matrix:**

| Output | Aspect | Length | Notes |
|---|---|---|---|
| YouTube Shorts | 9:16, 1080×1920 | ≤60s (up to 3 min allowed; keep ≤60s for loop rate) | Loop-friendly ending |
| Instagram Reels | 9:16, 1080×1920 | ≤90s | Safe-zone margins for UI overlays; burned-in captions |
| YouTube long-form | 16:9, 3840×2160 or 1080p | 3–12 min | Chapters from scene markers; end screen last 20s |

One script → one render template per platform; renders run in parallel via Shotstack render API with webhook callbacks into the QC scenario.
