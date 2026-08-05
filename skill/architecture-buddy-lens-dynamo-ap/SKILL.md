---
name: architecture-buddy-lens-dynamo-ap
description: Dynamo-AP lens for Architecture Buddy roundtables. Use when a design values write/read availability under partitions, decentralized replicas, eventual consistency, tunable consistency, multi-region or multi-primary data, conflict repair, or Cassandra/DynamoDB-style key-value and wide-column trade-offs. It asks whether stale or divergent data is acceptable, who resolves conflicts, and which invariants must not be AP.
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (Dynamo AP)
  version: "0.1.0"
  stance: "Keep the user path available under failure by partitioning data, replicating widely, accepting bounded divergence, and making reconciliation an explicit product contract."
  best-for: "available key-value data, global writes, session/cart/preference state, multi-datacenter replicas, tunable consistency, conflict-tolerant business data"
  not-for: "linearizable ledgers, locks, uniqueness-critical writes, cross-item invariants, irreversible side effects without reconciliation"
  evidence-anchors: "Dynamo paper; DynamoDB architecture; Apache Cassandra Dynamo lineage"
---

# Architecture Buddy Lens - Dynamo AP

This is a heuristic architecture lens for Architecture Buddy roundtables, not a persona and not roleplay. It applies the Dynamo/AP lineage as a design stance: preserve availability during common server, network, zone, and regional failures when the business domain can tolerate stale reads, concurrent writes, and explicit repair.

## Lens Metadata

- **Stance:** Keep the user path available under failure by partitioning data, replicating widely, accepting bounded divergence, and making reconciliation an explicit product contract.
- **Best for:** Available key-value data, global writes, session/cart/preference state, multi-datacenter replicas, tunable consistency, conflict-tolerant business data.
- **Not for:** Linearizable ledgers, locks, uniqueness-critical writes, cross-item invariants, irreversible side effects without reconciliation.
- **Evidence anchors:** Dynamo paper; DynamoDB architecture; Apache Cassandra Dynamo lineage.

## Framework Overview

The models below were retained because they recur across Dynamo, DynamoDB, and Cassandra-family practice; they generate concrete architecture decisions; and they distinguish an AP data-plane stance from generic "distributed database" advice.

### 1. Availability Is a Product Contract, Not a Checkbox

**One sentence:** Choose AP only when accepting a write or read during failure is more valuable than immediately proving the one true latest value.

**Evidence anchors:**
- Dynamo was built for Amazon services such as shopping carts where users should still view and modify state while disks fail, routes flap, or datacenters are impaired.
- The Dynamo paper explicitly sacrifices consistency under some failures to provide an "always-on" experience and pushes conflict resolution into the data model and application contract.
- Cassandra documents eventually consistent semantics and high availability as core design goals, with multi-primary replication and per-operation consistency choices.

**Triple verification:**
- **Cross-domain recurrence:** Appears in e-commerce cart/session data, internal Amazon key-value services, Cassandra wide-column deployments, and global replicated tables.
- **Generative power:** For a new proposal, it asks, "Which user action must continue during a partition, and what stale or conflicting states can the product explain?"
- **Exclusivity:** CP systems deliberately make the opposite choice for split-brain-prone metadata, locks, ledgers, and authority records.

**Application:** Start an AP design by naming the customer-visible failure that must not happen, then name the weaker consistency behavior the product will tolerate.

**Limit:** Availability-first is not a free upgrade. If stale or conflicting state breaks trust, money movement, inventory guarantees, or external side effects, this model rejects AP for that invariant.

### 2. Keyspace Ownership Is the Scaling Boundary

**One sentence:** Hash-partitioned keys and replica placement make availability scalable only when the workload can be localized to item, partition-key, or small item-collection boundaries.

**Evidence anchors:**
- Dynamo partitions data with consistent hashing and uses preference lists to identify the replicas responsible for a key while allowing incremental node addition.
- DynamoDB hashes partition keys, splits tables into partitions, routes requests through metadata, and automatically repartitions to preserve predictable performance at scale.
- Cassandra maps partition keys onto a token ring, replicates partitions according to a replication strategy, and explicitly avoids operations requiring broad cross-partition coordination for highly available global semantics.

**Triple verification:**
- **Cross-domain recurrence:** Shows up in Dynamo rings, DynamoDB table partitions, Cassandra token ranges, and hot-partition operations.
- **Generative power:** It predicts that poor partition keys, hot tenants, global secondary access paths, and cross-partition invariants will dominate the architecture review.
- **Exclusivity:** This is not generic sharding advice; it treats the partition key as the unit of availability, latency, repair, and operational blast radius.

**Application:** Require every AP proposal to state the partition key, expected hot-key distribution, replica placement across failure domains, and what operations cannot be local.

**Limit:** Hashing spreads keys, not demand. Hot products, celebrity users, tenants, or time buckets can still collapse availability into one overloaded range unless the data model absorbs skew.

### 3. Tunable Quorum Is a Dial, Not a Guarantee Label

**One sentence:** N/R/W or consistency-level choices trade latency, durability, freshness, and availability per operation; the architecture must state the dial setting and the failure mode it buys.

**Evidence anchors:**
- Dynamo exposes N, R, and W; R + W > N gives quorum-like overlap, but lower R/W improves latency and availability while increasing staleness or conflict risk.
- Dynamo uses sloppy quorum and hinted handoff so writes can land on healthy substitutes when preferred replicas are down, then be delivered later.
- Cassandra inherits Dynamo-style tunable consistency through levels such as ONE, QUORUM, LOCAL_QUORUM, and ALL, where W + R > replication factor can improve read-after-write visibility for chosen operations.

**Triple verification:**
- **Cross-domain recurrence:** Appears in Dynamo configuration, Cassandra consistency levels, multi-datacenter read/write routing, and AP-vs-CP roundtable decisions.
- **Generative power:** It asks, "For this API call, how many replicas must answer, and what happens when only one side of the partition responds?"
- **Exclusivity:** CP quorum is a safety boundary; AP tunable quorum is often a product-latency-availability dial and may deliberately accept non-overlap.

**Application:** Put consistency levels in the ADR per operation: default reads, user-facing writes, admin reads, repair reads, batch jobs, and multi-region traffic may need different settings.

**Limit:** A quorum-looking setting can still be undermined by sloppy membership, stale routing metadata, clock-based conflict rules, overloaded replicas, or cross-region latency budgets.

### 4. Divergence Repair Is Part of the Write Path

**One sentence:** If the system accepts concurrent or partitioned writes, detection, semantic merge, read repair, hinted handoff, and anti-entropy are first-class design work.

**Evidence anchors:**
- Dynamo uses object versioning and vector clocks to detect causally unrelated versions, returning siblings to clients when application-level semantic reconciliation is required.
- Dynamo uses hinted handoff for temporary failures and Merkle-tree anti-entropy to synchronize replicas that diverged after longer outages.
- Cassandra documents eventual consistency, replica repair, timestamp-based last-write-wins behavior, and Paxos-based lightweight transactions only for cases needing linearizable compare-and-set.

**Triple verification:**
- **Cross-domain recurrence:** Shows up in Dynamo vector clocks, Dynamo hinted handoff and Merkle trees, Cassandra repair and timestamp conflict resolution, and DynamoDB eventually consistent reads/global replication caveats.
- **Generative power:** It asks who sees conflicts, which versions survive, whether merge is semantic or last-writer-wins, and how operators know repair is lagging.
- **Exclusivity:** Many database designs hide conflicts behind serial execution; this stance exposes conflict as a normal case that the domain must own.

**Application:** Before approving AP writes, define the conflict object, merge rule, retry/idempotency key, repair mechanism, anti-entropy schedule, and user-facing semantics for duplicates or stale data.

**Limit:** Generic last-write-wins is unsafe for counters, carts, collaborative edits, inventory, balances, and irreversible commands unless loss is acceptable or compensated elsewhere.

### 5. Decentralization Reduces Single Control Points, Then Moves Complexity to Operations

**One sentence:** Masterless or highly automated replica fleets remove obvious single points of failure, but they demand strong membership, routing, admission control, repair observability, and load-skew management.

**Evidence anchors:**
- Dynamo favors symmetry, decentralization, gossip membership, and decentralized failure detection to avoid centralized outages and manual repartitioning.
- DynamoDB evolved from the Dynamo lineage into a managed service with request routers, metadata, autoadmin, adaptive capacity, global admission control, replica health automation, and Multi-Paxos inside partition replication groups.
- Cassandra uses gossip for membership and failure detection and relies on operationally visible replication, consistency levels, repair, and data modeling to sustain availability.

**Triple verification:**
- **Cross-domain recurrence:** Appears in Dynamo peer symmetry, Cassandra masterless operations, and DynamoDB's managed automation around partitions and replicas.
- **Generative power:** It predicts operational questions: who owns membership, who detects skew, who repairs replicas, who throttles noisy tenants, and what happens when automation lags reality?
- **Exclusivity:** This model rejects both "just add replicas" and "central coordinator will save us" as sufficient availability stories.

**Application:** Review the operational control plane separately from the data path: membership propagation, request routing, replica replacement, throttling/admission, hot-key mitigation, repair lag, and game-day evidence.

**Limit:** Modern DynamoDB is not the original leaderless Dynamo. It uses leader-based Multi-Paxos within partition replication groups for writes and strong reads, so lineage must not be flattened into "all Dynamo-family systems are masterless AP."

## Decision Heuristics

1. Use this lens when the business can tolerate stale, duplicated, reordered, or concurrently edited item state better than it can tolerate rejected reads or writes.
2. Declare the invariant scope: item-local, partition-local, tenant-local, region-local, or global. Anything global is suspect in an AP data path.
3. Choose the partition key from the highest-volume access path, then stress it against skew, celebrity tenants, temporal bursts, and item-collection growth.
4. State R/W/consistency level per operation instead of saying "eventual consistency" once for the whole system.
5. Put conflict resolution in the domain language: merge carts, union preferences, max timestamp, append event, compensate command, or reject via a CP side path.
6. Prefer idempotent writes with client request IDs or natural keys; AP retry storms otherwise create duplicates that look like successful availability.
7. Separate "available to accept" from "durably replicated everywhere." Hinted handoff, repair, and anti-entropy need lag metrics and alarms.
8. Treat read-your-writes as a product feature, not an assumption. If users require it, route, session-stick, quorum-read, or confirm via a stronger path.
9. Keep AP stores away from lock ownership, money movement, inventory uniqueness, external once-only side effects, and authorization source-of-truth unless a CP/fencing mechanism protects the invariant.
10. Validate with failure drills: node loss, rack/zone loss, regional partition, hot partition, repair backlog, clock skew, and client retry amplification.

## Schools and Design Tensions

- **Original Dynamo leaderless AP vs modern DynamoDB managed service:** Dynamo emphasized peer symmetry, sloppy quorum, vector clocks, and application-assisted reconciliation. DynamoDB shares the availability and key-value lineage but uses managed partition services, request routing, leader-based replication groups, and selectable strong/eventual reads.
- **Dynamo object-versioning vs Cassandra timestamp conflict rules:** Vector clocks expose concurrent siblings for semantic merge; last-write-wins is simpler but can silently discard causally independent updates.
- **Strict quorum vs sloppy quorum:** Strict quorum simplifies reasoning about overlap; sloppy quorum and hinted handoff preserve availability when preferred replicas are unreachable but make repair and durability windows more visible.
- **Always writable vs invariant preservation:** Carts, sessions, preferences, and telemetry often prefer acceptance plus repair; ledgers, locks, uniqueness, and authorization may need CP or transactional constraints.
- **Decentralized replicas vs managed automation:** Masterless peer systems reduce central bottlenecks but push repair, data modeling, and failure visibility to operators. Managed services hide more mechanics but still require key design and consistency choices.

## Would Not Do / Anti-Patterns

- Do not use AP replication as the authority for distributed locks, leader election, money balances, uniqueness-critical identifiers, or entitlement decisions.
- Do not claim "multi-region active-active" without specifying conflict resolution, read-your-writes expectations, idempotency, and failback behavior.
- Do not model data around secondary queries and then expect partition-key availability; AP storage works best when primary access paths are designed first.
- Do not hide last-write-wins behind a friendly API when lost updates would surprise users or violate business rules.
- Do not assume quorum settings alone solve partitions; define which replicas may be contacted, whether membership is strict or sloppy, and what repair follows.
- Do not promise availability without admission control and hot-partition mitigation; overloaded replicas can be a partition in practice.
- Do not move cross-item transactions into application retries without a duplicate, compensation, or reconciliation story.
- Do not equate Dynamo, DynamoDB, and Cassandra as the same architecture; use the shared AP lessons but verify the concrete product semantics.

## Honest Boundaries

- This lens is strongest for available data-plane state with item-level or partition-local semantics. It is intentionally weak for metadata coordination, linearizable decisions, and cross-entity invariants.
- "Eventually consistent" is not a complete requirement. The acceptable inconsistency window, merge rule, user-visible behavior, and repair SLO must be named.
- The public Dynamo paper describes an internal Amazon system from 2007; DynamoDB and Cassandra evolved different mechanics and guarantees. This lens uses the lineage as proven practice, not as a claim of identical internals.
- CAP language is a useful warning but too coarse for implementation. Real designs still need latency budgets, failure domains, consistency levels, throttling, and operations evidence.
- Source coverage here is based on the local Architecture Buddy corpus plus public Dynamo, DynamoDB, and Cassandra documents available during distillation; validate managed-service behavior against current vendor documentation before final design.

## Roundtable Output Contract

When Architecture Buddy asks this lens to contribute, answer only the decision point using this format:

```text
## Lens: Dynamo AP
### On the decision point
<Directly answer whether the decision fits availability-first, eventually consistent replicas. Name the invariant scope, accepted inconsistency, and where AP must stop. Keep this to <=10 lines.>

### Heuristics applied
- <2-5 concrete AP heuristics applied: partition key, consistency level, conflict repair, replica placement, idempotency, hot-key handling>

### Risks / what this lens would worry about
- <stale reads, lost updates, hot partitions, repair lag, clock/conflict behavior, retry duplicates, cross-item invariants, operational visibility>

### Would not do
- <specific design move this lens would reject and why>

### Evidence style
<Prefer failure-mode evidence, partition/load tests, conflict-resolution examples, consistency-level traces, repair-lag metrics, hot-key analysis, and precedent from Dynamo/DynamoDB/Cassandra semantics.>
```

## Appendix: Research Sources

Local corpus and build instructions:
- `/Users/apple/Desktop/skill-create/tools/nuwa-skill/SKILL.md` - theme Skill variant requirements.
- `/Users/apple/Desktop/skill-create/tools/nuwa-skill/references/extraction-framework.md` - triple verification method and theme-skill distinction.
- `/Users/apple/Desktop/skill-create/docs/build/nuwa-lens-distill-prompt.md` - Architecture Buddy lens output contract.
- `/Users/apple/Desktop/skill-create/docs/survey/living/strategies-and-patterns.md` - local Architecture Buddy strategy vocabulary and P5 entry point.
- `/Users/apple/Desktop/skill-create/docs/survey/patterns/P5-concurrency-distributed.md` - local CP contrast vocabulary for Raft/quorum coordination.
- `/Users/apple/Desktop/skill-create/docs/design/lens-catalog.md` - `dynamo-ap` catalog placement, best-for, not-for, and evidence anchors.
- `/Users/apple/Desktop/skill-create/docs/adr/0016-lens-distills-proven-practice-not-voice.md` - non-roleplay, proven-practice lens decision.

Public sources:
- Giuseppe DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" / Amazon Science abstract: https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store
- Werner Vogels, "Amazon's Dynamo" with paper text and summary: https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html
- Amazon DynamoDB ATC 2022 paper, "A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service": https://www.usenix.org/system/files/atc22-elhemali.pdf
- Amazon DynamoDB Developer Guide, partitions overview: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html
- Apache Cassandra documentation, architecture overview: https://cassandra.apache.org/doc/5.0.8/cassandra/architecture/overview.html
- Apache Cassandra documentation, Dynamo lineage: https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html
- Apache Cassandra documentation, guarantees: https://cassandra.apache.org/doc/5.0/cassandra/architecture/guarantees.html
