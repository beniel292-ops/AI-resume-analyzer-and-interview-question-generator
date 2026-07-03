# 01 — System & Automation Architecture

## 1. High-level architecture

OmniVideo AI is an event-driven pipeline. Each stage reads work from the Content Database (Airtable), does its job, writes results back, and advances the record's status. Make.com scenarios are the orchestration layer; Claude is the reasoning layer; specialized media APIs are the production layer.

```
                         ┌──────────────────────────────────────────┐
                         │            ORCHESTRATION (Make.com)       │
                         │  schedulers · webhooks · routers · retry  │
                         └──────┬──────────┬──────────┬─────────────┘
                                │          │          │
        ┌───────────┐    ┌──────▼───┐ ┌────▼─────┐ ┌──▼─────────┐
        │  SIGNALS   │    │ REASONING│ │PRODUCTION│ │ PUBLISHING  │
        │ Trends API │───▶│  Claude  │ │ ElevenLabs│ │ YouTube API │
        │ YT Search  │    │ (scoring,│ │ Midjourney│ │ IG Graph API│
        │ Reddit/X   │    │ research,│ │ /Flux     │ │ Buffer/     │
        │ Competitor │    │ scripts, │ │ Shotstack/│ │ native      │
        │ RSS        │    │ QC)      │ │ Creatomate│ │ scheduling  │
        └───────────┘    └──────┬───┘ └────┬─────┘ └──┬─────────┘
                                │          │          │
                         ┌──────▼──────────▼──────────▼─────────────┐
                         │        CONTENT DATABASE (Airtable)        │
                         │ topics · briefs · scripts · assets ·      │
                         │ videos · publications · metrics · learnings│
                         └──────────────────┬───────────────────────┘
                                            │
                              ┌─────────────▼─────────────┐
                              │  STORAGE (Google Drive)    │
                              │  raw assets · renders ·    │
                              │  thumbnails · archives     │
                              └───────────────────────────┘
```

### Tool stack (recommended)

| Layer | Primary tool | Why | Backup |
|---|---|---|---|
| Reasoning | **Claude API** (Sonnet for volume stages, Opus/Fable for strategy & QC) | Best long-context reasoning, structured JSON output, prompt caching for shared system prompts | — |
| Orchestration | **Make.com** | Visual scenarios, native Airtable/Google/YouTube modules, webhook triggers, built-in retry | n8n (self-hosted at scale) |
| Database | **Airtable** | Human-readable ops dashboard + API; interfaces for the review queue | Postgres (at 100+ videos/day) |
| File storage | **Google Drive** | Native Make modules, shared review access | S3/GCS at scale |
| Ops reporting | **Google Sheets** | Daily KPI exports, cost tracking, board reports | Looker Studio on top |
| Voiceover | **ElevenLabs** | Voice cloning, emotion control, 30+ languages | Azure TTS, OpenVoice |
| Images | **Flux / Midjourney (via API)** | Quality + style consistency via reference images | SDXL self-hosted at scale |
| Video render | **Shotstack or Creatomate** | JSON-template video assembly via API — deterministic, scalable | Remotion (code-based, self-hosted) |
| Captions | **AssemblyAI / Whisper** | Word-level timestamps for animated subtitles | — |
| Music/SFX | **Epidemic Sound / Artlist API** | Licensed, claim-safe | — |
| Publishing | **YouTube Data API v3, Instagram Graph API** | Direct control over metadata, scheduling | Buffer/Metricool as fallback |

## 2. Database schema (Airtable base: `OmniVideo`)

Nine tables. Primary keys are Airtable record IDs; `slug` fields provide idempotency keys for Make scenarios.

### `Topics`
| Field | Type | Notes |
|---|---|---|
| slug | text (unique) | normalized topic key — **duplicate prevention** |
| title | text | |
| niche | link → Niches | |
| source | select | trends / evergreen / competitor / audience-question / learning-system |
| opportunity_score | number 0–100 | see Discovery Engine formula |
| competition_score | number 0–100 | |
| revenue_potential | select | low / medium / high (est. RPM × est. views) |
| audience_size | number | est. monthly searches + social volume |
| difficulty | select | easy / medium / hard (research + production effort) |
| status | select | discovered → approved → researched → scripted → produced → published → archived / rejected |
| embedding_hash | text | similarity hash vs. published topics (dup detection) |

### `Briefs` (Research Engine output)
key_facts (long text, JSON), statistics (JSON, each with source URL + confidence), story_angles, contrarian_insights, faqs, weak_evidence_flags, sources (URLs + reliability tier), topic (link).

### `Scripts`
topic (link), brief (link), duration_class (15s/30s/60s/3m/10m), variant (A/B/C), hook, body (structured JSON: scenes[]), cta, retention_devices (JSON), word_count, status (draft → qc_pass → selected → produced).

### `Assets`
script (link), scene_index, type (image/motion/broll/diagram/thumbnail/music/sfx/voiceover), generator, prompt_used, drive_url, license_ref, qc_status.

### `Videos`
script (link), platform_format (shorts/reels/longform), render_job_id, drive_url, duration_s, qc_score, qc_report (JSON), status (rendering → qc → approved → scheduled → published → failed).

### `Publications`
video (link), platform, external_id, title, description, tags, publish_at, published_at, url, ab_test_group.

### `Metrics` (append-only, one row per video per day)
publication (link), date, views, watch_time_min, avg_view_duration_pct, ctr, likes, comments, shares, subs_gained, revenue_usd, rpm.

### `Learnings`
period, insight_type (hook/format/topic/thumbnail/length/publish_time), statement, evidence (JSON: sample size, lift, confidence), action (prompt/scoring adjustment applied), applied_at.

### `Niches`
name, target_audience, pillars, rpm_estimate, active (checkbox), daily_quota.

**Duplicate prevention:** before inserting a Topic, a Make scenario calls Claude with the candidate title + the 200 most recent topic slugs/titles in the niche and asks for a semantic-duplicate verdict; exact `slug` collisions are rejected by an Airtable unique-field check first (cheap path before the LLM call).

## 3. Make.com scenario catalog

Twelve scenarios; each is small, single-purpose, and idempotent.

| # | Scenario | Trigger | Flow |
|---|---|---|---|
| S1 | Discover Trends | Schedule 3×/day | Pull Google Trends, YouTube search, Reddit, competitor RSS → Claude scores & dedups → insert `Topics` |
| S2 | Approve Topics | Schedule 1×/day | Claude ranks day's topics vs. niche quota + Learnings → sets status=approved (top N) |
| S3 | Research | Airtable watch: status=approved | Fetch sources (HTTP + search API) → Claude cross-checks → insert `Briefs` → status=researched |
| S4 | Script | watch: status=researched | Claude generates 2–3 variants per duration class → insert `Scripts` |
| S5 | Script QC | watch: Scripts status=draft | Claude QC rubric → qc_pass or regenerate (max 2 retries) → select best variant |
| S6 | Voiceover | watch: status=selected | ElevenLabs per scene → upload Drive → insert `Assets` |
| S7 | Visuals | parallel with S6 | Image/motion generation per scene → Drive → `Assets` |
| S8 | Assemble | all assets qc_status=pass | Build Shotstack JSON (scenes, subtitles from AssemblyAI, transitions, music ducking) → render per platform format → `Videos` |
| S9 | Video QC | render webhook | Claude reviews transcript+frames rubric → qc_score → approved or flag |
| S10 | Publish | watch: status=approved | Slot into calendar → YouTube/IG upload with metadata + thumbnail → `Publications` |
| S11 | Collect Metrics | Schedule 1×/day | YouTube Analytics API + IG Insights → append `Metrics` |
| S12 | Learn & Report | Schedule weekly (+ daily lite) | Claude analyzes Metrics → writes `Learnings` → updates scoring weights + prompt library → emails board report |

### Workflow diagram — happy path for one video

```
S1 discover ─▶ S2 approve ─▶ S3 research ─▶ S4 script ─▶ S5 script QC
                                                            │
                                              ┌─────────────┴─────────────┐
                                              ▼                           ▼
                                        S6 voiceover                 S7 visuals
                                              └─────────────┬─────────────┘
                                                            ▼
                                                       S8 assemble
                                                            ▼
                                                       S9 video QC ──fail──▶ human review queue
                                                            ▼ pass
                                                       S10 publish
                                                            ▼
                                              S11 metrics (daily) ─▶ S12 learn (weekly)
```

## 4. API requirements

| API | Used for | Quota notes |
|---|---|---|
| Claude API | scoring, research synthesis, scripts, QC, learning | Use prompt caching for rubrics/system prompts; batch API for overnight scoring at scale |
| YouTube Data API v3 | upload, metadata, scheduling | Upload = 1600 quota units; default 10k units/day ≈ 6 uploads → request quota extension early |
| YouTube Analytics API | metrics | Separate quota, generous |
| Instagram Graph API | Reels publish + insights | 25 API-published posts/day/account cap — plan accounts accordingly |
| Google Trends (via SerpAPI/Glimpse) | discovery | No official API; use wrapper |
| ElevenLabs | TTS | Character-based pricing; cache narrator settings |
| Shotstack/Creatomate | rendering | Per-render-minute pricing; webhook callbacks |
| AssemblyAI | word-level captions | Per audio-hour |

## 5. Error handling

- **Idempotency:** every scenario checks the record's status before acting and writes a `processing_lock` timestamp; re-runs are no-ops.
- **Retries:** Make built-in retry with exponential backoff (3 attempts) on all HTTP modules; media generation gets a dedicated retry queue (transient GPU failures are common).
- **Dead-letter queue:** any record failing 3 attempts moves to status=`failed` with `error_log`; a Slack/email digest lists failures daily.
- **Circuit breakers:** if a provider fails >20% of calls in an hour, the scenario pauses that provider and (where a backup exists) fails over.
- **Content-level fallback:** if a scene's visual fails permanently, Assembly substitutes a template card (headline on branded background) rather than blocking the video.
- **Budget guards:** daily spend counters per API in Google Sheets; scenarios halt when a cap is hit and alert Ops.

## 6. Monitoring

- **Pipeline health dashboard (Airtable interface):** counts by status, age of oldest stuck record per stage, failure rate per scenario.
- **Alerts:** red = publishing missed a scheduled slot, QC pass rate <60%, spend cap hit; yellow = stage latency >2× baseline.
- **Quality drift:** weekly sample of 5 published videos re-scored by the QC rubric; declining trend triggers prompt-library review.
- **Cost per video:** computed nightly (API costs ÷ videos published), tracked as a first-class KPI.
