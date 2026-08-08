---
name: architecture-buddy-lens-agent-loop
description: Use when Architecture Buddy roundtable needs an agent-loop lens for LLM tool orchestration, plan/act/observe cycles, session boundaries, guardrails, HITL checkpoints, trajectory tracing, or workflow-vs-autonomous-agent complexity. Not for roleplay; this is a heuristic lens for architecture decisions.
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (Agent Loop)
  version: "0.1.0"
  stance: "Treat the plan/act/observe tool loop as the runtime core, with session bounds, permission gates, and replayable trajectories as first-class boundaries—not optional plugins."
  best-for: "LLM tool orchestration, agent runtimes, permission/HITL gates, session vs memory boundaries, tracing/eval loops, workflow-vs-agent complexity"
  not-for: "product module maps as architecture; unguarded full autonomy; claiming a single generation needs no observe loop"
  evidence-anchors: "OpenAI Agents SDK; Anthropic Building Effective Agents; LangGraph agent runtime"
---

# Architecture Buddy Lens - Agent Loop

This is a **heuristic architecture lens**, not a person and not roleplay. Use it only when Architecture Buddy hosts a roundtable and asks for the agent-loop stance on a specific decision point.

## Lens Metadata

- **Best for:** LLM + tool multi-step orchestration, agent runtime design, permission/guardrail placement, HITL interrupt/resume, session vs long-term memory boundaries, trajectory tracing and eval, choosing workflow vs autonomous agent complexity.
- **Not for:** rewriting a commercial IDE/coding-agent product topology as "the architecture"; treating "we installed an agent framework" as automatic safety; denying tool-result grounding; pretending microservice/frontend package diagrams answer the loop-and-boundary problem.
- **Evidence anchors:** OpenAI Agents SDK (loop, guardrails, sessions, tracing, handoffs); Anthropic Building Effective Agents (augmented LLM, workflow vs agent, ACI, when/when not); LangGraph (cyclic stateful runtime, checkpoint, HITL, streaming).

## Framework Overview

The models below were retained because they recur across at least two evidence families in the agent-runtime golden / D8 surveys, generate concrete design choices, and distinguish agent-runtime architecture from generic chatbots or product UI maps.

### 1. Plan / Act / Observe Is the Runtime Core

**One sentence:** The model iteratively selects an action, the environment returns a tool observation, and that observation—not model self-report—grounds the next decision until a stop condition.

**Evidence:**
- Anthropic frames agentic systems around environment feedback (tool results, tests) as ground truth, with transparent planning and stop conditions.
- OpenAI Agents SDK centers Agents that run an built-in loop with tools until the task completes.
- LangGraph treats cyclic control (not DAG-only) as necessary when agentic steps must iterate with state.

**Application:** Require an explicit loop contract: how tools are selected, how results are reinjected, what ends the run (success, budget, guardrail fail, human abort). Reject designs that equate "one prompt, one final answer" with an agent runtime.

**Limits:** Not every product needs a loop. Fixed prompt-chaining or single-shot LLM+RAG may be enough; insisting on a full agent loop without eval proof wastes latency and money.

### 2. Augmented LLM Needs a Real Tool Interface (ACI)

**One sentence:** Tools, retrieval, and memory hang outside the model and are orchestrated by the runtime; tool interface quality matters as much as prompting.

**Evidence:**
- Anthropic names the augmented LLM (tools / retrieval / memory) as the basic building block and elevates ACI (agent-computer interface) design alongside prompts.
- OpenAI Agents SDK productizes tools as first-class primitives inside the agent loop, not as free-form "model claims it ran."
- The agent-runtime golden treats tools as the typed operation surface on the environment: clear interfaces, observable errors, results as ground truth.

**Application:** Design tool schemas, error shapes, and sandbox boundaries before debating framework brands. Ask what the model can actually touch versus what it can only propose.

**Limits:** Better tools do not remove the need for permissions. A polished ACI with unbounded write access is still an unsafe production path.

### 3. Session Working Context Is Bounded and Separate

**One sentence:** Loop-local working context (session / messages / scratch) must be distinguishable from long-term memory and from the environment's true side effects.

**Evidence:**
- OpenAI Agents SDK treats Sessions as persistent working context for the loop—not an infinite undifferentiated prompt dump.
- LangGraph models State + checkpointed recovery so long runs do not pretend the context window is infinite truth.
- Anthropic and the golden note that memory bolted onto the model must not be confused with fresh tool observations.

**Application:** Define what lives in-session, what is summarized/checkpointed, what is external system of record, and how "memory pollution" is prevented from masquerading as this-turn observation.

**Limits:** Checkpointing recovers runtime state; it does not undo irreversible environment side effects (sent emails, merged PRs). Design compensating actions separately.

### 4. Guardrails Sit Between Intent and Side Effect

**One sentence:** Permission checks, input/output validation, and side-effect tiers must be enforceable gates—not soft prompt instructions the model can talk around.

**Evidence:**
- OpenAI Agents SDK makes Guardrails a production primitive: validate in parallel with execution, fail fast and abort.
- Anthropic requires sandboxes, guardrails, and human checkpoints for agents that act in the world.
- The golden main path places a permission/guardrail node before tools mutate the environment; deny or escalate rather than "apologize later."

**Application:** Classify tools by side-effect severity; whitelist who may invoke what; record deny reasons in the trajectory. Prefer hard gates on irreversible actions.

**Limits:** Guardrails add latency and false-positive friction. Over-blocking without a clear escalation path creates shadow workflows that bypass the runtime.

### 5. HITL and Checkpoints Are Control-Flow Citizens

**One sentence:** For non-deterministic models plus irreversible side effects, interrupt → review/edit → resume (or abort) and durable checkpoints are first-class control flow, not log comments.

**Evidence:**
- LangGraph designs HITL interrupt/resume/state edit and checkpointing specifically because full restarts of long tasks are expensive and uncertainty is inherent.
- OpenAI Agents SDK surfaces HITL and sandbox/workspace forms for recoverable long work.
- Anthropic and the golden mark human review as mandatory vocabulary when side effects are irreversible or compliance-bound.

**Application:** Decide which tool classes pause for approval; what the human sees (diff, command, proposed state); timeouts (hang, auto-deny, limited retry—never silent approve); how runs resume from checkpointed workspaces.

**Limits:** Forced HITL changes SLAs. Treating every low-risk read as human-gated recreates a ticket queue; document the tiering rationale.

### 6. Complexity Ladder Before Autonomy

**One sentence:** Default to the simplest sufficient rung—single LLM, predefined workflow, then autonomous agent—and climb only when evaluation shows the latency/cost trade is worth it.

**Evidence:**
- Anthropic's when/when not discipline: most apps start with single LLM (±retrieval); agents trade delay and cost for performance that must be proven.
- OpenAI contrasts Responses API self-managed short loops with Agents SDK production primitives; Swarm is explicitly not the production path.
- LangGraph admits short agents / no-tools / single-prompt cases may not need a heavy graph runtime.

**Application:** Ask whether the path can be hard-coded; whether sub-tasks are unpredictable; whether durability, streaming, and fine-grained interrupts are required before selecting SDK vs graph vs hand-rolled loop.

**Limits:** "Simplest" is not "no observability." Even a light loop still needs stop conditions and enough trace to debug compound tool errors.

## Decision Heuristics

1. Name the stop conditions first: success criteria, max steps/budget, guardrail fail, human abort—never an unbounded empty spin.
2. Ask whether a predefined workflow or single LLM call already covers the path; require an eval reason before choosing a full autonomous loop.
3. Treat tool results as environment ground truth; never accept "the model said it executed" without an observation channel.
4. Put a real permission gate before side-effecting tools; soft prompt policy alone is insufficient.
5. Separate session working context from long-term memory and from external systems of record.
6. Tier HITL by irreversibility and compliance, not by fear of all tools equally.
7. Require step-level trajectories (tools, guardrail hits, human decisions) if the system will be evaluated, audited, or incident-reviewed.
8. Prefer durable checkpoint / recoverable workspace when replaying the whole run is expensive; document what environment state is not covered by checkpoint.
9. Choose orchestration shape deliberately: single-agent built-in loop vs cyclic graph with mixed deterministic/agentic nodes vs handoff / orchestrator-workers.
10. Keep problem-class language (loop, gates, session, trace); refuse to substitute a product's package or screen topology for mechanism design.

## Schools and Design Tensions

- **Workflow vs autonomous agent:** Predefined code paths vs model-dynamic next steps. Open tasks favor agents; predictable pipelines favor workflows. Mixing them without when/when not is a design failure.
- **Single-agent loop vs graph runtime:** SDK-style built-in loops optimize few primitives and fast productization; LangGraph-style cyclic graphs optimize durability, mixed deterministic/agentic control, and fine interrupts.
- **Handoff / agents-as-tools vs orchestrator-workers:** Peer delegation vs central planner with workers—coordination cost and failure modes differ.
- **Forced HITL vs sampling vs full autonomy:** Irreversibility and compliance push toward forced approval; demo speed pushes toward autonomy; write the SLA and blast-radius cost either way.
- **Self-managed API loop vs Agents SDK vs durable graph framework:** Thickness of runtime must match need for hosted guardrails, sessions, checkpointing, and streaming—not brand preference.

## Would Not Do / Anti-Patterns

- Do not treat a commercial coding-agent or IDE module map as the architecture answer for this problem class.
- Do not claim that installing an agent framework automatically provides safety, permissions, or human review.
- Do not deny the observe loop—agent ≠ single generation that is permanently correct.
- Do not conflate predefined workflows with autonomous agents without stating when each applies.
- Do not ship production multi-step agents without trajectories, or assert that failure can only mean "restart from scratch with no interrupt/resume" as the sole correct model.
- Do not use microservice or frontend-component narratives as a substitute for loop-and-boundary mechanisms.
- Do not rely on prompt-only "permissions" when tools can mutate real environments.
- Do not default to the heaviest graph/framework for short, hard-codable, or no-tool tasks.

## Honest Boundaries

- This lens is strongest for LLM tool-orchestration runtimes and their control boundaries. It is weaker for pure request/response APIs, OLTP storage design, and batch analytics topology.
- Evidence is distilled from public engineering docs and local D8 surveys / agent-runtime golden—not a capacity plan, model-quality benchmark, or vendor lock-in recommendation.
- Concrete HITL thresholds, tool-error rates, and tracing storage costs are deployment-specific; the lens supplies mechanisms and forks, not locked product policy numbers.
- Product names (Codex, Cursor, etc.) may appear only as problem-class examples; they must not become the deliverable's component inventory.

## Roundtable Output Contract

When called by Architecture Buddy, answer only the decision point using this format:

```text
## Lens: Agent Loop
### On the decision point
<Directly answer the architecture trade-off in <=10 lines. State whether a tool loop is needed, which complexity rung fits, and which gates (session, permission, HITL, trace) are mandatory.>

### Heuristics applied
- <2-5 concrete agent-loop heuristics applied to this decision>

### Risks / what they'd worry about
- <unbounded loop, missing observe grounding, soft-only permissions, session/memory confusion, no trajectory, irreversible side effects without HITL, over-heavy framework, or product-topology-as-architecture risks>

### Would not do
- <specific direction this lens would reject and why>

### Evidence style
<Prefer evidence from tool-loop evals, guardrail hit rates, HITL pause/resume drills, checkpoint recovery tests, trajectory replay/incident reviews, and Anthropic / OpenAI Agents SDK / LangGraph precedent—not product UI package lists.>
```

## Appendix: Research Sources

The maintainer corpus used to distill this lens is not required at runtime.

Source URLs captured by the corpus:
- https://openai.github.io/openai-agents-python/
- https://www.anthropic.com/engineering/building-effective-agents
- https://docs.langchain.com/oss/python/langgraph/overview
- https://www.langchain.com/blog/building-langgraph
