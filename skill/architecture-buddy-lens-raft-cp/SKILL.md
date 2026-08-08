---
name: architecture-buddy-lens-raft-cp
description: >
  Use when Architecture Buddy roundtable needs a Raft-CP lens for majority consensus,
  strongly consistent metadata coordination, leader election, config state, leases,
  watches, or avoiding split-brain.
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (Raft CP)
  version: "0.1.0"
  stance: "Put small, critical metadata behind understandable majority consensus; keep bulk business data and high-throughput data paths out of the quorum core."
  best-for: "leader election, cluster metadata, configuration, membership, fencing, strongly consistent control-plane state"
  not-for: "large business datasets, low-latency AP paths, Byzantine trust failures, global active-active writes without quorum trade-offs"
  evidence-anchors: "Raft paper; etcd architecture/API guarantees; Kubernetes control-plane architecture"
---

# Architecture Buddy Lens - Raft CP

This is a heuristic lens for Architecture Buddy roundtables, not a persona. It evaluates whether a proposal needs understandable majority consensus and strongly consistent metadata coordination, then makes the quorum, scope, and operational consequences explicit.

## Lens Metadata

- **Stance:** Put small, critical metadata behind understandable majority consensus; keep bulk business data and high-throughput data paths out of the quorum core.
- **Best for:** Leader election, cluster metadata, configuration, membership, fencing, strongly consistent control-plane state.
- **Not for:** Large business datasets, low-latency AP paths, Byzantine trust failures, global active-active writes without quorum trade-offs.
- **Evidence anchors:** Raft paper; etcd architecture/API guarantees; Kubernetes control-plane architecture.

## Framework Overview

### 1. Replicated Log Before Distributed State

**One sentence:** A CP coordination system is safest when every node reaches the same state by applying the same ordered log, not by reconciling ad hoc peer state.

**Evidence anchors:**
- Raft decomposes consensus around a replicated log feeding deterministic state machines: leader election, log replication, safety, and membership change.
- etcd exposes a globally ordered revision over a single Raft-backed KV store, giving clients a concrete ordering handle for metadata.
- Kubernetes treats etcd as the source of truth behind the API server, with controllers observing ordered state changes and reconciling from that durable record.

**Triple verification:**
- **Cross-domain recurrence:** Appears in algorithm design (Raft), production coordination storage (etcd), and orchestration control planes (Kubernetes).
- **Generative power:** For a new coordination proposal, this model asks, "What is the authoritative ordered log, and which state machine consumes it?"
- **Exclusivity:** This is not generic reliability advice; it specifically rejects loose peer convergence for decisions that must never split-brain.

**Application:** Require designs to name the commands that enter the log, the deterministic state transitions they produce, and which reads need the log's latest committed state.

**Limit:** A single ordered log is intentionally narrow. It can become the bottleneck or wrong abstraction when the workload is large, partition-tolerant, or naturally sharded.

### 2. Majority Is the Safety Boundary

**One sentence:** The system stays correct because any committed decision intersects with future decisions through a majority quorum.

**Evidence anchors:**
- Raft serves safely with a majority and uses majority agreement for leader election and log commitment.
- Raft membership changes use joint consensus so old and new configurations overlap by majority.
- etcd chooses CP behavior: it would rather lose availability under partition than allow split-brain metadata writes.

**Triple verification:**
- **Cross-domain recurrence:** Shows up in election, replication, membership changes, and production CP storage behavior.
- **Generative power:** It predicts that a design with two independent writable partitions is outside the lens unless another fencing authority exists.
- **Exclusivity:** AP stores, caches, and eventually consistent systems deliberately choose a different boundary.

**Application:** Ask every proposed failure mode in quorum terms: which side can elect, which side can commit, and what clients observe when no majority is reachable.

**Limit:** Majority protects safety, not user happiness. It can turn common network or capacity problems into visible write unavailability.

### 3. Strong Leader Simplifies the Mental Model

**One sentence:** Raft makes consensus understandable by routing log entries through a strong leader rather than treating all peers symmetrically.

**Evidence anchors:**
- Raft's paper explicitly favors understandability through decomposition and a strong leader, with log entries flowing leader to follower.
- P5 contrasts this with Paxos's harder-to-teach single-decree model assembled into a log.
- etcd's client-visible behavior includes uncertainty around timeouts and leader elections, making leader transitions part of the API reality.

**Triple verification:**
- **Cross-domain recurrence:** Applies to algorithm pedagogy, implementation strategy, and client error handling.
- **Generative power:** For a new system, it asks who serializes writes, how leadership changes, and what clients must retry or verify.
- **Exclusivity:** Symmetric peer protocols and CRDT-style convergence intentionally avoid this leader-centered shape.

**Application:** Prefer designs where write ownership, retry semantics, and leader failure behavior are explicit enough for operators and client authors to reason about.

**Limit:** A leader is also a focus of latency, load, operational attention, and tail behavior. Read scaling needs careful consistency choices.

### 4. Metadata Scope Discipline

**One sentence:** CP coordination is for small, high-value metadata and coordination primitives, not for turning consensus into a general data plane.

**Evidence anchors:**
- etcd frames itself as strongly consistent, durable metadata storage with reliable scale in the gigabyte range, not a bulk business database.
- Kubernetes centralizes desired cluster state in etcd while leaving container runtime, networking, and workload data paths outside the consensus store.
- P5 explicitly warns against treating a consensus library as a massive business database.

**Triple verification:**
- **Cross-domain recurrence:** Appears in etcd capacity guidance, Kubernetes control-plane/data-plane split, and distributed pattern taxonomy.
- **Generative power:** It predicts which proposed fields belong in the CP store: identity, membership, config, leases, and desired state, not telemetry streams or large payloads.
- **Exclusivity:** Many reliable systems deliberately keep heavy data in sharded stores while using CP only to coordinate ownership and metadata.

**Application:** Force a boundary review: what must be linearizable, what can be cached, what can be eventually consistent, and what should live in another storage system.

**Limit:** The boundary is easy to erode. Once users discover a convenient strongly consistent KV, they may push logs, metrics, blobs, or hot counters into it.

### 5. Watches And Leases Are Coordination Aids, Not Magic

**One sentence:** Watch streams, leases, locks, and elections help clients coordinate, but external correctness still needs version checks, fencing, and recovery logic.

**Evidence anchors:**
- etcd provides Watch, Lease, Lock, and Election primitives alongside MVCC and compaction, but watch latency can be unbounded under unhealthy conditions.
- etcd lock APIs do not by themselves guarantee mutual exclusion over external resources; resource-side version validation or fencing is required.
- Kubernetes controllers use watch-diff-act reconciliation, assuming controllers can recover by re-reading the authoritative API state.

**Triple verification:**
- **Cross-domain recurrence:** Appears in etcd coordination APIs, lock/fencing warnings, and Kubernetes controller architecture.
- **Generative power:** It asks whether every external side effect carries a revision, generation, fencing token, or compare-and-swap condition.
- **Exclusivity:** Simpler lock stories often stop at "I acquired the lock"; this lens treats that as incomplete for external resources.

**Application:** For every lease or watch-driven design, specify stale-holder behavior, missed-event recovery, compaction handling, and the validation performed by the protected resource.

**Limit:** Fencing shifts some burden to downstream systems. If the external resource cannot validate versions, the coordination layer cannot fully protect it.

## Decision Heuristics

- Use Raft-style CP when the business failure is "two authorities both believed they were primary," not merely "some clients saw stale data."
- Keep the consensus group small and the data inside it smaller; store references, desired state, leases, and versions rather than large payloads.
- Design client APIs around completion uncertainty: after timeout, the client may need to read, compare revision, or retry idempotently.
- State the consistency level per read path: linearizable when correctness depends on the latest committed value, serializable or cached only when staleness is acceptable.
- Treat membership changes as first-class operations with overlap, sequencing, and rollback plans; never swap cluster membership as an out-of-band shortcut.
- Pair every distributed lock or lease with fencing, CAS, or resource-side generation checks.
- Make watch consumers resumable from a known revision and able to recover from compaction by relisting authoritative state.
- Separate control plane and data plane early; the CP store coordinates where work should happen, not the high-volume work itself.
- Budget quorum latency and quorum loss explicitly in the architecture decision record, including cross-zone placement and failure domains.
- Prefer an understandable consensus implementation and operational model over a theoretically elegant one the team cannot debug at 3 a.m.

## Design Disagreements

- **Linearizable reads vs lower-latency reads:** Linearizable reads preserve the strongest mental model, while serializable or cached reads reduce latency at the cost of possible staleness.
- **Single coordination group vs sharded coordination:** A single group gives simple global ordering; sharding improves capacity but makes cross-shard invariants harder.
- **Embedded consensus vs managed coordination service:** Embedding can reduce dependencies and fit product shape; using etcd/ZooKeeper/Consul-like systems concentrates operational knowledge and failure semantics.
- **Lease convenience vs correctness discipline:** Leases simplify liveness and cleanup, but TTL and client pauses can mislead holders unless downstream fencing exists.
- **CP purity vs user-facing availability:** Refusing writes without quorum prevents split-brain, but product owners may prefer degraded, stale, or read-only behavior during partitions.

## Would Not Do / Antipatterns

- Would not put high-cardinality business records, metrics streams, logs, blobs, or hot counters in the quorum-backed metadata store.
- Would not claim "we have a lock" as proof of external mutual exclusion unless the protected resource checks a revision, generation, or fencing token.
- Would not allow both sides of a partition to accept authoritative metadata writes.
- Would not hide leader election and timeout uncertainty behind an API that pretends writes are simply success-or-failure.
- Would not use watches as the only source of truth; consumers must be able to relist and resume.
- Would not treat wall-clock TTL as a correctness proof in the presence of pauses, partitions, or slow clients.
- Would not add CP consensus to a workload whose real requirement is cache invalidation, queueing, idempotency, or eventual convergence.

## Honest Limits

- This lens assumes non-Byzantine failures. It does not cover malicious peers, arbitrary corruption, or adversarial consensus.
- It is strongest for metadata coordination and control-plane state, not for OLTP, analytics, document storage, or event streaming architecture.
- It does not choose a specific product for the team; etcd, ZooKeeper, Consul, database transactions, or a managed control plane may each be reasonable depending on operational context.
- It cannot eliminate CAP trade-offs. It makes the decision to reject unsafe writes during quorum loss visible.
- Local corpus coverage is centered on Raft, etcd, and Kubernetes; broader Paxos-family and multi-region consensus variants are only secondary context here.

## Roundtable Output Contract

When Architecture Buddy asks this lens to contribute, answer only in this shape:

```text
## Lens: Raft CP
### On the decision point
State whether the decision is truly CP metadata coordination, what must be strongly consistent, and what can remain outside the quorum path.

### Heuristics applied
Name the specific quorum/log/metadata/watch/lease heuristics used. Tie each to the proposal, not to generic distributed-systems advice.

### Risks / what this lens would worry about
Call out quorum loss, leader transition uncertainty, data-scope creep, stale lock holders, watch recovery gaps, compaction, and operational capacity risks where relevant.

### Would not do
List concrete design moves this lens would reject for this decision.

### Evidence style
Use Raft majority/log safety, etcd API guarantees and limits, and Kubernetes control-plane separation as anchors. Mark assumptions that need validation.
```

## Sources

The maintainer corpus and build instructions used to distill this lens are not required at runtime.
- Diego Ongaro and John Ousterhout, "In Search of an Understandable Consensus Algorithm (Raft)": https://raft.github.io/raft.pdf
- Raft project site and visualization resources: https://raft.github.io/
- etcd Learning documentation: https://etcd.io/docs/latest/learning/
- etcd "Why etcd?" documentation: https://etcd.io/docs/v3.5/learning/why/
- Kubernetes Cluster Architecture documentation: https://kubernetes.io/docs/concepts/architecture/
