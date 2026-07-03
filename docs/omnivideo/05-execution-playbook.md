# 05 — Execution Playbook (Execution Mode)

What happens, step by step, when the system is given a niche or topic. This is the operational contract every run follows — whether triggered by the daily scheduler or a human typing "go do X".

## Input

Either a **niche** ("AI tools for students") or a **specific topic** ("Why context windows matter"). A niche run executes steps 1–8 for the whole pipeline; a topic run skips to step 4 with a forced-approve.

## The eight steps

### 1. Research the niche
- Map the audience: who watches, what they search, what they fear/want.
- Pull the competitive landscape: top 20 channels, their formats, cadence, view medians, gaps.
- Establish the niche record: RPM estimate, content pillars (4–6), visual bible seed, narrator voice selection.

### 2. Generate content opportunities
- Run the Discovery Engine across all signal sources scoped to the niche.
- Target: 30–50 candidate topics on day one; dedupe against anything already in `Topics`.

### 3. Rank opportunities
- Score every candidate (opportunity, competition, revenue potential, audience size, difficulty).
- Build the launch slate: **70% evergreen / 20% trending / 10% contrarian bets** — evergreen builds the searchable library, trending tests hooks fast, bets find outliers.
- Approve the top N per the niche's daily quota.

### 4. Create scripts
- Research Engine produces briefs for each approved topic.
- Script Engine generates the variant matrix. Default launch mix per topic: 2× 60s Shorts variants (A/B hooks) + 1× 3min where the brief supports depth; 10min reserved for the pillar topic of the week.

### 5. Create production plans
Per selected script, a production manifest:
- Scene-by-scene visual assignments (tool routing per the Visual Engine table).
- Voiceover plan: narrator, tone preset, pronunciation-dictionary additions.
- Music mood, caption style, export formats.
- Cost estimate per video; flag anything over budget for template substitution.

### 6. Create publishing plans
- Calendar slots from niche-audience timezone data (defaults: Shorts 12:00 & 19:00 local; long-form Sat/Sun morning) — replaced by learned optimal times after 4 weeks of data.
- Metadata pack per publication: title (≤60 chars, keyword-front-loaded), description with chapters + links + disclosures, tags, thumbnail concepts (3, A/B tested), pinned comment (long-form funnel link).
- A/B assignments recorded so the Learning System can attribute results.

### 7. Create growth plans
- **Cross-platform ladder:** every long-form spawns 2–3 Shorts/Reels cuts; every winning Short (top decile at 72h) triggers a long-form expansion topic.
- **Funnel:** Shorts → channel subscribe → long-form → email list (lead magnet per pillar).
- **Community loop:** Claude drafts replies to the top comments in the first 6 hours (human-approved above a sensitivity threshold); comment questions are mined back into `Topics`.
- Weekly experiment budget: 10% of quota reserved for format/hook experiments chosen by the Learning System.

### 8. Create monetization plans
- Map each content pillar to its primary revenue stream (AdSense / affiliate / sponsor-fit / lead-gen) per the Revenue Engine.
- Insert affiliate opportunities into commercial-intent topics from day one.
- Define the sponsorship readiness milestone (10k subs) and the digital-product trigger (50k subs + one pillar with >60% avg retention).

## Operating principles (always-on)

1. **Long-term over short-term:** never publish a video that trades trust for clicks — the Learning System optimizes watch time and subs-per-view, not raw views.
2. **Everything is an experiment:** no change to prompts, formats, or schedules without a measurement plan.
3. **Quality floors are non-negotiable at every scale:** QC thresholds rise, never fall, as volume grows.
4. **Humans do only what machines can't yet:** review-queue exceptions, new template design, sponsorship sales, and vetoing the weekly plan.

## Day-one checklist (new niche launch)

- [ ] Niche record created (pillars, RPM, quota, visual bible, narrator)
- [ ] Channel + accounts created, branding applied, API credentials connected
- [ ] 30+ topics discovered, scored, slate approved
- [ ] First 7 days of content scripted, QC-passed, and scheduled
- [ ] Metrics collection verified end-to-end on the first publication
- [ ] Weekly board report subscription confirmed
