# Video-Informed Architecture Boundary Review

## Source

- Video: [一张图说明软件架构设计-核心关键点和底层逻辑](https://www.bilibili.com/video/BV1ve4y1b7gH/)
- Duration: 719 seconds
- Page status: publicly readable
- Author subtitles: none; burned-in subtitles were extracted from sampled video frames and OCR-checked
- Local evidence: `.video-analysis/video-cover.jpg`, `.video-analysis/contact-sheet.jpg`, `.video-analysis/frame-ocr.txt`

## Absorbed Principles

The skill absorbed only the generalizable principles:

- Start from the problem, goals, scenarios, and flows rather than from services or frameworks.
- Derive capabilities or domain invariants, application boundaries, integration, technical mechanisms, and quality attributes.
- Treat service/module/API/database/technology inventories as system-design material, not sufficient architecture evidence.
- Keep the layer chain adaptive for Git, protocols, storage, compilers, and infrastructure; do not force business terminology.
- Treat microservices, DDD, and named layers as optional refinements rather than architecture completion criteria.

## Changed Surface

- `skill/architecture-buddy/SKILL.md` version `0.3.5`
- `skill/architecture-buddy/references/deliverable-gate.md`
- `skill/architecture-buddy/templates/architecture-deliverable.md`
- `scripts/architecture-quality-report.sh`
- `docs/design/architecture-quality-rubric.md`
- `scripts/pressure-test.sh` and architecture/system-design counterexamples

## RED-GREEN Evidence

- Before the host change, the new pressure test failed with `missing explicit architecture-vs-system-design boundary`.
- After the host and scorer changes, the full pressure suite passed.
- A technical-only document is now classified with `architecture-boundary-debt` and rejected by the hard gate.
- A valid deliverable with target-layer and derivation-chain evidence remains `PASS` with `20/20` structure.

## SkillOpt Training Attempt

- Task set: `2026-08-06-skillopt-architecture-tasks-v5.json`
- Tasks: 10, including `architecture-layer-positioning` and `system-design-boundary`
- Backend: real Codex
- `auto_adopt`: false
- Baseline validation: hard `0.3333333333`, soft `0.825`, mixed `0.5791666667`
- Candidate/gate: **not produced**
- Outcome: interrupted during candidate replay/consolidation after repeated silent Codex subprocess waiting; no candidate was adopted
- Staging evidence: `.skillopt-sleep/staging/20260806-101721/evidence.jsonl`

The baseline score is evidence that the new behavior is testable, not evidence of improvement. A future run requires a functioning Codex subprocess/authentication path and must produce a candidate plus held-out gate result before any training claim or adoption.
