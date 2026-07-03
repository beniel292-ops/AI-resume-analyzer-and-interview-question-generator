# OmniVideo AI — Autonomous Content & Media Company

**System design for a fully autonomous, AI-powered media company** that discovers content opportunities, researches them, produces videos end-to-end, publishes across platforms, measures results, and feeds those results back into every upstream decision.

## Design goals

The system maximizes, in priority order:

1. **Audience growth** — compounding subscribers/followers across platforms
2. **Revenue** — ad revenue, sponsorships, affiliates, products
3. **Engagement** — likes, comments, shares, saves
4. **Watch time** — retention-optimized formats and pacing
5. **Content quality** — accuracy, clarity, production value
6. **Automation** — minimal human touch per published video

## Core principle: the flywheel

Every published video is an experiment. The Learning System closes the loop:

```
┌─────────────┐    ┌──────────┐    ┌─────────┐    ┌────────────┐
│  DISCOVERY   │───▶│ RESEARCH │───▶│ SCRIPTS │───▶│ PRODUCTION │
└─────────────┘    └──────────┘    └─────────┘    └────────────┘
       ▲                                                 │
       │                                                 ▼
┌─────────────┐    ┌───────────┐    ┌────────────┐    ┌────┐
│  LEARNING    │◀───│ ANALYTICS │◀───│ PUBLISHING │◀───│ QC │
└─────────────┘    └───────────┘    └────────────┘    └────┘
```

Winning hooks, formats, and topics raise the opportunity scores of similar future content; losers lower them. The system gets measurably better every week without human intervention.

## Document map

| Document | Contents |
|---|---|
| [01-architecture.md](01-architecture.md) | System architecture, automation stack (Claude, Make.com, Airtable, Google Workspace, YouTube/Instagram APIs), database schema, workflow diagrams, error handling, monitoring |
| [02-content-engines.md](02-content-engines.md) | Content Discovery, Research, Script Generation, Visual Creation, Voiceover, and Video Assembly engines |
| [03-quality-and-learning.md](03-quality-and-learning.md) | Quality Control system, Content Database, Learning System |
| [04-operations.md](04-operations.md) | Scaling plan (1 → 1000 videos/day), Revenue Engine, cost models, team requirements |
| [05-execution-playbook.md](05-execution-playbook.md) | Step-by-step Execution Mode: what happens when the system is given a niche or topic |

## Organizational model

The system is operated as a set of autonomous "agents" that mirror a media company org chart. Each agent is a Claude-driven pipeline stage with a defined contract (inputs, outputs, quality gates):

| Role | Automated by | Human involvement at scale |
|---|---|---|
| CEO / Strategy | Learning System + weekly board report | Reviews weekly report, sets niche priorities |
| Content Strategist | Discovery Engine | Approves new content pillars |
| Research Lead | Research Engine | Spot-checks flagged claims |
| Scriptwriter | Script Engine | None (QC gate replaces review) |
| Video Producer | Assembly Engine | Handles pipeline failures |
| Motion Designer | Visual Engine templates | Builds new templates monthly |
| Growth Marketer | Publishing + A/B system | Negotiates sponsorships |
| Data Analyst | Analytics + Learning System | None |
| Operations Manager | Monitoring + alerting | On-call for red alerts |

## Non-goals and guardrails

- **No fabricated facts.** The Research Engine flags weak evidence; QC blocks videos containing unverified claims.
- **No copyright risk.** Only licensed music/SFX libraries, AI-generated or licensed visuals, and fair-use-reviewed clips.
- **No engagement bait that erodes trust.** Retention tactics must be earned (curiosity gaps that get resolved, hooks the video actually delivers on).
- **Platform ToS compliance.** Publishing respects API rate limits, disclosure rules for AI content and affiliate links.
