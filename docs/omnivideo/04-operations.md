# 04 — Scaling Plan & Revenue Engine

---

## 1. Scaling plan: 1 → 1000 videos/day

Costs are rough 2026 estimates for a mostly-Shorts mix (long-form adds render + research cost but much higher RPM). "Cost/video" = all API + tooling costs ÷ published videos.

### Stage 1 — 1 video/day (validate the loop)

- **Infrastructure:** Make.com Core, Airtable Team, Claude API, ElevenLabs Starter, Shotstack sandbox→prod, one YouTube channel + one IG account.
- **Cost:** ~$150–300/mo (≈$5–10/video).
- **Bottleneck:** none technical — the bottleneck is *learning speed*. Goal is not volume; it's proving QC pass rate >80% and getting the first learnings loop running.
- **Team:** the founder, ~1 hr/day reviewing everything published.
- **Exit criteria:** 30 consecutive days fully automated, QC ≥80% auto-pass, retention within 20% of niche benchmarks.

### Stage 2 — 10 videos/day (multi-channel)

- **Infrastructure:** same stack, upgraded tiers; 3–5 channels/niches; YouTube quota extension approved; Claude Batch API for overnight scoring; template library ~30 scene templates.
- **Cost:** ~$1.5–3k/mo (≈$5–10/video).
- **Bottlenecks:**
  - IG Graph API 25 posts/day/account → multiple accounts, one per niche.
  - Make operations count → consolidate scenarios, move heavy loops into Claude tool-use or small Cloud Functions.
  - Human review queue (10% of 10/day is fine; watch it).
- **Team:** founder + 1 part-time editor/reviewer (5–10 hr/wk) handling QC queue and template refresh.
- **Automation opportunity:** auto-localization of top performers effectively multiplies output free.

### Stage 3 — 100 videos/day (platform migration)

- **Infrastructure changes (the big rewrite):**
  - Airtable → **Postgres** (Airtable API limits and record caps break here); keep an Airtable/Retool view as the ops dashboard.
  - Make.com → **n8n self-hosted or a queue-based worker system** (Make per-operation pricing becomes the dominant cost; you need parallelism and priority queues).
  - Image generation → self-hosted SDXL/Flux on GPU spot instances for the volume tier; paid APIs only for hero content.
  - Rendering → Remotion render farm on AWS Lambda or a Shotstack enterprise contract.
  - 15–30 channels; channel-management tooling; per-channel voice + visual bibles.
- **Cost:** ~$10–20k/mo (≈$3–6/video — unit cost falls with self-hosting).
- **Bottlenecks:** GPU capacity planning; YouTube upload quotas per channel; QC review queue (10% = 10/day → need a second reviewer or a tighter auto-pass threshold backed by better rubrics); duplicate-topic pressure within niches (raise semantic-dup threshold, expand niches).
- **Team:** 3–5 people — 1 ops engineer, 1–2 content reviewers/template designers, 1 growth/partnerships. Everyone manages the system, nobody makes videos.

### Stage 4 — 1000 videos/day (media platform)

- **Infrastructure:** Kubernetes worker fleet; dedicated GPU reservations + spot mix; event bus (SQS/PubSub) replacing scheduled scenarios; data warehouse (BigQuery) + real ML for scoring (learned ranking model replaces the weighted formula, trained on your own outcome data — a real moat); 100+ channels across languages.
- **Cost:** ~$60–120k/mo (≈$2–4/video).
- **Bottlenecks:** platform risk becomes the #1 risk (spam/AI-content policy enforcement across many channels — mitigate with per-channel quality floors, human-touch hero content, and platform diversification); trust & brand (at this volume, one viral inaccuracy damages everything — QC budget grows, not shrinks); organizational (on-call, incident response).
- **Team:** 8–15 — platform engineers, ML engineer, QC leads per language, partnerships/sales for sponsorship inventory, finance.

### Bottleneck summary

| Scale | Binding constraint | Fix |
|---|---|---|
| 1/day | Learning speed | Ship daily, measure everything |
| 10/day | Platform API caps, Make ops pricing | More accounts, batch APIs |
| 100/day | Airtable/Make ceilings, GPU cost, review queue | Postgres + queue workers, self-hosted generation |
| 1000/day | Platform policy risk, quality at volume | Diversification, learned QC, human hero-content layer |

---

## 2. Revenue Engine

### Streams, in order of activation

1. **YouTube monetization (AdSense).** Long-form RPM $2–20+ by niche (finance/B2B tech high, entertainment low); Shorts RPM ~$0.05–0.30. **Strategic consequence: Shorts are the audience-acquisition engine; long-form is the ad-revenue engine.** The system should funnel Shorts viewers to long-form via pinned comments, end screens, and "full video" bridges.
2. **Affiliate marketing.** Activate immediately (no threshold). Discovery Engine flags topics with commercial intent ("best X", "X vs Y", "how to choose"); Publishing injects tracked links + disclosure. Typical: $0.5–5 per 1,000 views in commercial niches.
3. **Sponsorships.** Viable from ~10k engaged subs/channel. Standard rates ≈ $15–30 CPM on expected views for integrated reads. The Script Engine generates the integration segment from a sponsor brief; QC checks disclosure. At Stage 3+, sponsorship inventory across channels is the largest revenue line — this is the one function that stays human (sales).
4. **Digital products.** Package the Learning System's proven content into paid assets: niche playbooks, template packs, courses. Gross margin ~95%; launch once any channel passes ~50k subs.
5. **Lead generation / consulting.** In B2B niches, videos feed an email list (lead magnet per content pillar); leads sold or converted to consulting. Highest $/view of any stream in professional niches.

### Revenue model by stage (conservative, blended)

| Stage | Monthly views (est.) | AdSense | Affiliate | Sponsors | Products/Leads | Total/mo | Cost/mo | Net |
|---|---|---|---|---|---|---|---|---|
| 1/day (mo 1–3) | 100k–500k | $50–300 | $50–200 | — | — | **$0.1–0.5k** | $0.3k | ≈ break-even |
| 10/day (mo 4–9) | 2–8M | $1–4k | $0.5–2k | $1–3k | — | **$2.5–9k** | $2.5k | positive |
| 100/day (yr 1–2) | 20–80M | $10–40k | $5–15k | $15–50k | $5–20k | **$35–125k** | $15k | strongly positive |
| 1000/day (yr 2–3) | 150M+ | $75k+ | $30k+ | $100k+ | $50k+ | **$250k+** | $90k | platform economics |

Assumptions to validate early: blended RPM (drives everything — niche selection matters more than volume), Shorts→long-form conversion rate, QC pass rate (drives real unit cost).

### Niche selection rule

Pick niches scoring high on: RPM × searchable evergreen demand × automatability of visuals × founder credibility. Recommended starting portfolio: **AI/software education** (high RPM, diagram-friendly, evergreen), **personal finance basics** (highest RPM; requires strictest accuracy QC), **productivity/career** (broad audience, storytelling-friendly).
