# Video-Informed Architecture Boundary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Absorb the video's useful distinction between architecture thinking and system implementation into Architecture Buddy without hard-coding a microservice or DDD template.

**Architecture:** Add a principle-first architecture-layer checkpoint: problem/business intent and scenarios must derive capabilities, application boundaries, integration, technical mechanisms, and quality attributes. Keep layer selection adaptive for infrastructure, protocol, and library designs. Strengthen the deliverable gate and pressure corpus with system-design-as-architecture counterexamples.

**Tech Stack:** Markdown skill documents, Bash pressure tests, existing rubric scripts, shell validation.

## Global Constraints

- Preserve the existing draft/deliverable flow, roundtable preflight, B6 evidence contract, and dual-layer deliverable format.
- Do not turn architecture work into a fixed checklist or require business layers that do not apply to the design object.
- Do not add project dependencies or modify unrelated dirty files.
- Do not adopt a SkillOpt candidate without a significant semantic improvement and human review.

---

### Task 1: Establish the failing architecture-boundary pressure test

**Files:**
- Modify: `scripts/pressure-test.sh`
- Create: `scripts/fixtures/pressure/system-design-only.md`

- [ ] Add a fixture that has services, APIs, databases, and technology choices but no problem class, business capability derivation, architecture decision, or quality-attribute reasoning.
- [ ] Add a RED assertion requiring the host skill to state the architecture-vs-system-design boundary and the derivation chain.
- [ ] Run `bash scripts/pressure-test.sh` and confirm it fails only because the new host rules are absent.

### Task 2: Add the principle-first architecture-layer guidance

**Files:**
- Modify: `skill/architecture-buddy/SKILL.md`
- Modify: `skill/architecture-buddy/references/deliverable-gate.md`
- Modify: `skill/architecture-buddy/templates/architecture-deliverable.md`

- [ ] Add adaptive layer-positioning guidance and the derivation chain from problem/business intent to technical mechanisms and quality attributes.
- [ ] State that a service/module/API/database/technology inventory alone is system design, not a complete architecture design.
- [ ] Keep DDD and microservices as optional refinements, not universal prerequisites.
- [ ] Add gate checks for target layer, derivation evidence, deliberate omissions, and at least one quality-attribute consequence.
- [ ] Run the pressure test and confirm the new checks pass while existing gates remain green.

### Task 3: Reinstall and verify the skill package

**Files:**
- Modify: `skill/architecture-buddy/SKILL.md` version metadata if the behavioral change is accepted.

- [ ] Run the repository checker, shell syntax checks, pressure tests, and diff whitespace checks.
- [ ] Confirm `/Users/apple/.codex/skills/architecture-buddy` resolves to the updated source and source/install copies match.

### Task 4: Re-run quality evaluation and training gate

**Files:**
- Create: `corpus/runs/2026-08-06-video-informed-architecture-boundary.md`

- [ ] Run the architecture-quality scorer against the system-design-only counterexample and a valid architecture deliverable.
- [ ] Run the held-out architecture corpus baseline and candidate evaluation.
- [ ] Keep `auto_adopt=false`; adopt only if semantic, domain, and held-out quality improve materially after human review.
- [ ] Record authentication failures or incomplete training honestly; do not treat mock results as model-quality evidence.
