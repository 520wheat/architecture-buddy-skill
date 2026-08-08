---
name: architecture-buddy-lens-log-stream
description: Use when Architecture Buddy roundtable needs a log-stream lens for event-driven integration, append-only logs as source of truth, offsets, replay, audit streams, partitioned consumers, Kafka/Pulsar-style messaging, or EIP channel trade-offs. Not for roleplay; this is a heuristic lens for architecture decisions.
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (Log Stream)
  version: "0.1.0"
  stance: "Treat the append-only log as the durable integration fact, with independent consumer offsets and replay as first-class design constraints."
  best-for: "event-driven integration, audit streams, multi-consumer replay, partitioned stream processing, Kafka/Pulsar trade-offs"
  not-for: "using a log as a cross-service strong-transaction silver bullet or hiding business invariants inside the broker"
  evidence-anchors: "Kafka design; Apache Pulsar architecture; Enterprise Integration Patterns"
---

# Architecture Buddy Lens - Log Stream

This is a **heuristic architecture lens**, not a person and not roleplay. Use it only when Architecture Buddy hosts a roundtable and asks for the log-stream stance on a specific decision point.

## Lens Metadata

- **Best for:** event-driven integration, audit streams, multi-consumer replay, partitioned stream processing, Kafka/Pulsar-style messaging, EIP channel/routing choices.
- **Not for:** treating an event log as a distributed transaction coordinator, a universal ESB, or a substitute for domain ownership and idempotent endpoints.
- **Evidence anchors:** Kafka design docs, Apache Pulsar architecture docs, Enterprise Integration Patterns.

## Framework Overview

The models below were retained because they recur across at least two evidence families, generate concrete design choices, and distinguish the log-stream stance from generic messaging advice.

### 1. Append-Only Log as Integration Fact

**One sentence:** Write immutable events to a durable ordered log first, then let consumers derive their own views from that fact stream.

**Evidence:**
- Kafka frames itself as closer to a distributed commit log than a traditional message queue: persistent append log, sequential write, long retention, and replayable offsets.
- Pulsar stores messages in BookKeeper managed ledgers, keeping durable records and cursors separate from transient broker serving.
- EIP's Message Channel and Guaranteed Delivery patterns give the vocabulary: decouple sender/receiver, persist until safe handling.

**Application:** Favor a log when multiple systems need the same business fact, auditability matters, downstream consumers evolve independently, or derived state must be rebuildable.

**Limits:** The log records facts; it does not make all services share one transaction boundary. If the business invariant requires synchronous commit across domains, this lens should raise a warning rather than force event streaming.

### 2. Offsets Are Consumer-Owned Clocks

**One sentence:** A consumer's position in the log is state, and designing where that state lives determines replay, recovery, and fan-out semantics.

**Evidence:**
- Kafka's consumer model uses pull, long polling, and partition offsets; consumer groups can rewind or advance independently.
- Pulsar persists subscription cursors in BookKeeper, making consumption state part of the durable messaging substrate.
- EIP distinguishes Point-to-Point from Publish-Subscribe channels: one consumer group competes for work; many groups/subscriptions each hold independent progress.

**Application:** Ask who owns the offset, whether each downstream has an independent cursor, what replay range must remain available, and how reprocessing is coordinated with idempotency.

**Limits:** Offset control makes replay possible but also exposes duplicate processing, poison messages, and side-effect reapplication. Replay without idempotent endpoints is operational debt.

### 3. Partition Keys Buy Local Order by Spending Parallelism

**One sentence:** A partition key is a contract about what must stay ordered together, and every such contract constrains scaling.

**Evidence:**
- Kafka gives order inside a partition and uses keyed partitioning for semantic locality while consumer groups parallelize across partitions.
- The Kafka-vs-Pulsar survey notes both systems share partitioned/sharded parallelism, durable replicas, and ordered log mechanics.
- EIP Competing Consumers scales processing, while Resequencer and Aggregator expose the cost of recovering order or related sets after distribution.

**Application:** Choose partition keys from business invariants: account, order, tenant, device, or workflow instance. Document what order is guaranteed, what order is not, and what happens when a hot key appears.

**Limits:** Partitioning does not give global order. Repartitioning later can be expensive because consumers, retention, and downstream assumptions may already depend on the original key.

### 4. Retention and Replay Separate Delivery from Processing

**One sentence:** A retained log turns messaging from "deliver once then forget" into "store facts long enough for recovery, backfill, and new consumers."

**Evidence:**
- Kafka explicitly chooses long retention rather than deleting messages at consumption, enabling rewind and offline/batch consumers.
- Pulsar persistent messaging stores messages until acknowledged, and its ledger model supports durable replay boundaries.
- EIP Message Store, Message History, Wire Tap, and Dead Letter Channel show that integration systems need audit and failure trails, not just transient delivery.

**Application:** Set retention from recovery objectives, audit needs, schema evolution windows, and expected consumer lag. Treat replay as a tested runbook, not a magical property of the platform.

**Limits:** Retention has cost. Infinite replay expectations shift storage, schema compatibility, privacy deletion, and operational burden onto the platform.

### 5. Log Serving Topology Is a Strategic Choice

**One sentence:** Decide whether the system should be a compact broker-local log or a separated serving and durable-log architecture before optimizing details.

**Evidence:**
- Kafka's classic design leans on broker-local partitions, OS page cache, sequential writes, batching, and zero-copy transfer.
- Pulsar separates stateless brokers from BookKeeper durable storage, with metadata stores, managed ledgers, optional proxies, and geo-replication.
- The Kafka-vs-Pulsar comparison frames the split: operational simplicity and unified log mental model versus independent serving/storage scaling and stronger multi-tenant/global platform features.

**Application:** Prefer a Kafka-like stance when the organization wants a unified real-time data log with efficient broker-local operations. Prefer a Pulsar-like stance when independent storage scaling, explicit multi-tenancy, proxy entry, or geo-replication are central requirements.

**Limits:** More topology knobs create more operational surface. A separated storage architecture can solve scaling problems while introducing metadata, recovery, and component ownership problems.

## Decision Heuristics

1. Start with the integration fact: name the event that is true once appended, who produces it, and who is allowed to change its schema.
2. Use publish-subscribe when multiple consumers need independent offsets; use a competing-consumer group when exactly one worker should handle each event.
3. Pick the partition key from the smallest business scope that requires ordering; do not claim global order unless the platform actually provides it.
4. Design idempotency before promising replay. Every replayable side effect needs a dedupe key, natural idempotence, or a compensating workflow.
5. Size retention from concrete use cases: outage recovery, backfill, audit, ML/offline consumers, and schema migration. "Keep everything forever" is a storage policy, not an architecture.
6. Keep routing rules observable and owned. Content-based routing, filters, splitters, and aggregators become change hotspots if ownership is vague.
7. Separate poison messages from transient failures. Dead letter, invalid, retry, and quarantine channels need explicit semantics.
8. Use batching, sequential I/O, and compression for throughput, but check where encryption or proxying removes zero-copy assumptions.
9. Decide whether clients should discover partition leaders directly or enter through a proxy/service gateway; cloud/Kubernetes networking often changes the answer.
10. Treat schema evolution as part of the log contract: replay means old events will meet new code.

## Schools and Design Tensions

- **Kafka-style unified log vs Pulsar-style separated ledger:** Kafka emphasizes a simple distributed log mental model and efficient broker-local data path; Pulsar emphasizes stateless brokers, BookKeeper ledgers, cursors, proxy options, and geo-replication.
- **Pull vs push:** Kafka's pull model lets consumers control pace and batching; push/event-driven consumers can reduce latency in some systems but can overrun heterogeneous downstreams.
- **Application routing vs broker-centered routing:** EIP routing patterns are useful vocabulary, but routing logic can become an operational hotspot. Prefer clear ownership over "smart pipe" ambiguity.
- **Replay as power vs replay as blast radius:** The same feature that enables backfill can duplicate emails, payments, webhooks, or irreversible side effects if endpoints are not designed for it.
- **Ordering vs throughput:** More ordering usually means fewer independent lanes. More lanes usually means more reordering, aggregation, and correlation work downstream.

## Would Not Do / Anti-Patterns

- Do not sell a log stream as a replacement for ACID transactions across services.
- Do not put every integration through Kafka/Pulsar just because the platform exists; simple RPC, file transfer, or shared database may fit some bounded problems better.
- Do not use random partitioning when business order or locality matters.
- Do not hide failures by silently filtering, dropping, or endlessly retrying messages.
- Do not create a central router that no team owns and every team depends on.
- Do not promise replay without retention, schema compatibility, idempotency, and operational runbooks.
- Do not assume broker-level durability automatically means business-level exactly-once outcomes.

## Honest Boundaries

- This lens is strongest for integration architecture, audit streams, and event-driven derived state. It is weaker for low-latency request/response APIs, OLTP invariants, and human workflow design.
- The source corpus is a local survey distillation, not a full benchmark or production capacity plan.
- Kafka and Pulsar ecosystems evolve; validate operational claims against the deployed version, managed service, and team experience.
- EIP names are vocabulary for reasoning. They are not permission to install an ESB or over-centralize integration logic.

## Roundtable Output Contract

When called by Architecture Buddy, answer only the decision point using this format:

```text
## Lens: Log Stream
### On the decision point
<Directly answer the architecture trade-off in <=10 lines. State whether the append-only log should be source of truth, side channel, or not used.>

### Heuristics applied
- <2-5 concrete log-stream heuristics applied to this decision>

### Risks / what they'd worry about
- <replay, offset ownership, partition key, schema, poison message, retention, topology, or operational risks>

### Would not do
- <specific direction this lens would reject and why>

### Evidence style
<Prefer evidence from production replay drills, consumer lag/throughput data, partition hot-spot analysis, schema compatibility tests, incident history, and Kafka/Pulsar/EIP precedent.>
```

## Appendix: Research Sources

The maintainer survey corpus used to distill this lens is not required at runtime.

Source URLs captured by the corpus:
- https://kafka.apache.org/documentation/#design
- https://pulsar.apache.org/docs/concepts-architecture-overview/
- https://www.enterpriseintegrationpatterns.com/
