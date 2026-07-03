# 03 — Quality Control, Content Database, Learning System

---

## 1. Quality Control System

Two gates: **script QC** (cheap, before any media spend) and **video QC** (after render, before publish). Both use Claude with a fixed rubric; scores 0–100 per dimension.

### Script QC rubric

| Dimension | Checks | Blocker threshold |
|---|---|---|
| Accuracy | Every factual claim traced to the brief; weak-evidence facts properly hedged; stats carry their year | any untraceable claim |
| Clarity | Grade-8 readability for general niches; one idea per sentence; jargon defined on first use | <70 |
| Engagement | Hook strength (would a cold viewer stop scrolling?); curiosity gap resolved; retention trigger cadence met | <65 |
| Repetition | Semantic similarity vs. last 90 days of published scripts in the niche | similarity >0.85 |
| Ending | Payoff delivered; CTA ≤1 sentence | missing payoff |

Fail → regenerate with the QC feedback injected (max 2 retries) → then human queue.

### Video QC rubric

| Dimension | Checks |
|---|---|
| Audio | Whisper transcript ↔ script diff <2%; loudness −14 LUFS; no clipped/robotic segments |
| Visual quality | Frame sampling: artifacts, unreadable text, off-brand styling, wrong aspect safe-zones |
| Sync | Captions aligned within 200ms; scene visuals match scene text |
| Copyright | All assets from whitelisted sources with `license_ref` set; no unlicensed logos/faces in generated images |
| Compliance | AI-disclosure flag set where platform requires; affiliate disclosure present when links used |

**Composite qc_score ≥80 → auto-publish. 60–79 → human review queue (Airtable interface, one-click approve/reject with reason — reasons feed the Learning System). <60 → auto-reject and re-render or kill.**

Human review is the escape valve, not the default: target <10% of videos touching a human at steady state.

---

## 2. Content Database

The Airtable base (full schema in [01-architecture.md](01-architecture.md#2-database-schema-airtable-base-omnivideo)) is the single source of truth. Key properties:

- **Everything is linked:** Topic → Brief → Scripts → Assets → Videos → Publications → Metrics. Any metric row can be traced back to the hook, script variant, thumbnail, and topic that produced it — this lineage is what makes the Learning System possible.
- **Duplicate prevention (three layers):**
  1. Unique `slug` constraint (exact dupes, free).
  2. Claude semantic check of new topics vs. recent published titles (near-dupes).
  3. Script QC repetition check vs. 90-day script corpus (same topic, different words).
  Deliberate *refreshes* of old winners (>12 months, stats outdated) bypass the check via a `refresh_of` link field.
- **Asset registry:** every generated image, voiceover, and music selection is recorded with its prompt, generator, and license reference — required for copyright defense and for reusing strong assets.
- **Revenue join:** daily `Metrics` rows carry per-video revenue where the platform exposes it (YouTube); sponsorship/affiliate revenue is attributed at the Publication level.

---

## 3. Learning System

**Goal:** every week the system publishes measurably better content than the week before, without a human in the loop.

### Inputs (from `Metrics`, daily)

Watch time, average view duration %, CTR, retention curves (YouTube Analytics per-video), likes/comments/shares/saves, subscribers gained per video, revenue and RPM.

### Analysis cadence

- **Daily (lite):** flag outliers — any video >3× or <0.3× the niche's trailing-30-day median views-per-hour-since-publish. Outliers get an immediate Claude post-mortem (hook, thumbnail, topic, publish time) written to `Learnings`.
- **Weekly (full):** cohort analysis across the week's publications:
  - **Winning formats:** duration class × structure (story vs. listicle) × niche, ranked by watch time and subs-per-view.
  - **Winning topics:** which discovery source and score band actually delivered; recalibrate the opportunity-score weights against realized performance (predicted vs. actual views regression).
  - **Winning hooks:** A/B variant results; classify hooks into a taxonomy (question, contrarian, stat-shock, story cold-open, challenge) and track win rates per taxonomy cell.
  - **Thumbnails:** CTR by concept style from YouTube Test & Compare.
  - **Retention diagnostics:** for long-form, find the biggest retention-curve drop; map its timestamp to the script scene; log the failing pattern.

### Actuation — how learnings change behavior

Each accepted learning writes a concrete change, recorded in `Learnings.action`:

1. **Scoring weights:** Discovery Engine formula coefficients updated (bounded ±20% per week to avoid thrash).
2. **Prompt library:** Script Engine system prompt carries a "current playbook" section (top 5 hook patterns with examples, patterns to avoid) regenerated weekly from `Learnings`.
3. **Quota shifts:** niche daily quotas rebalance toward niches with rising subs-per-video and RPM.
4. **Format mix:** the duration-class distribution per niche shifts toward winners (e.g., 60s Shorts outperforming 30s → shift ratio).
5. **Kill rules:** topic clusters with 3 consecutive underperformers get a 60-day cooldown.

### Statistical discipline

- Minimum sample sizes before a learning is accepted (e.g., ≥8 videos per cell for format conclusions; A/B hook tests need ≥2,000 impressions per arm).
- Learnings carry confidence levels; only high-confidence learnings auto-actuate — medium ones go to the weekly board report as hypotheses to test deliberately.
- Every actuated change is itself an experiment: the weekly report compares pre/post metrics and reverts changes that didn't help.

### Weekly board report (auto-generated, emailed)

Executive summary → wins/losses → KPI trends (subs, watch time, revenue, cost per video, QC pass rate) → learnings applied → learnings proposed → next week's plan (quotas, experiments). This is the CEO-level control surface: a human can veto anything, but silence means the system proceeds.
