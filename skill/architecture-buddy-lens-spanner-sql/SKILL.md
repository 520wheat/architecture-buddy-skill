---
name: architecture-buddy-lens-spanner-sql
description: Use when Architecture Buddy roundtable needs a Spanner SQL lens for globally distributed SQL, external consistency, strict serializability, TrueTime-style bounded clocks, Paxos-replicated splits, multi-region OLTP, lock-free reads, schema changes, or SQL at global scale. Not for roleplay; this is a heuristic architecture lens.
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (Spanner SQL)
  version: "0.1.0"
  stance: "Global SQL can be made externally consistent, but only by paying explicitly for bounded time uncertainty, synchronous replication, placement, and transaction coordination."
  best-for: "global OLTP, externally consistent transactions, multi-region SQL, strongly consistent reads, compliance-grade ordering, read/write locality trade-offs"
  not-for: "low-latency AP writes, offline-first conflict merging, teams unwilling to operate global placement and quorum costs, workloads that only need cached or eventual views"
  evidence-anchors: "Google Spanner OSDI 2012 paper; Cloud Spanner architecture/replication docs; Spanner external consistency docs"
---

# Architecture Buddy Lens - Spanner SQL

This is a heuristic architecture lens for Architecture Buddy roundtables, not a person and not roleplay. It evaluates proposals that want global SQL, strong transactions, and scale at the same time, then makes the hidden costs of external consistency visible.

## Lens Metadata

- **Stance:** Global SQL can be made externally consistent, but only by paying explicitly for bounded time uncertainty, synchronous replication, placement, and transaction coordination.
- **Best for:** Global OLTP, externally consistent transactions, multi-region SQL, strongly consistent reads, compliance-grade ordering, read/write locality trade-offs.
- **Not for:** Low-latency AP writes, offline-first conflict merging, teams unwilling to operate global placement and quorum costs, workloads that only need cached or eventual views.
- **Evidence anchors:** Google Spanner OSDI 2012 paper; Cloud Spanner architecture/replication docs; Spanner external consistency docs.

## Framework Overview

The models below were retained because they recur across the Spanner paper, public Cloud Spanner architecture material, and the local distributed-systems corpus; they generate concrete architecture choices and distinguish this lens from generic SQL or consensus advice.

### 1. Time Is an API, Not an Assumption

**One sentence:** External consistency depends on exposing clock uncertainty as a first-class bound, then making the system wait when the bound is too wide.

**Evidence anchors:**
- The OSDI paper identifies TrueTime as the key enabler: `TT.now()` returns an interval, not a point, and commit timestamps depend on bounded uncertainty.
- Spanner's external consistency rule requires that if transaction T1 commits before T2 starts, T1's commit timestamp is lower than T2's.
- Cloud Spanner materials explain commit wait: a write is not externally visible until its commit timestamp is definitely in the past.

**Triple verification:**
- **Cross-domain recurrence:** Appears in transaction ordering, lock-free reads, schema changes, and consistent backups.
- **Generative power:** For a new global SQL proposal, it asks "what is the timestamp authority, what is the uncertainty bound, and who waits?"
- **Exclusivity:** Most databases treat wall-clock time as approximate metadata; this lens treats bounded uncertainty as part of the correctness protocol.

**Application:** Require any claimed "global real-time order" to name the time source, uncertainty budget, commit-wait behavior, monitoring, and fallback when uncertainty grows.

**Limit:** TrueTime is infrastructure-heavy. Without comparable bounded uncertainty, the design may need a centralized timestamp oracle, hybrid logical clocks with weaker guarantees, or a narrower consistency claim.

### 2. Split the Data, Not the Invariant

**One sentence:** Spanner scales by splitting key ranges into independently replicated Paxos groups, while distributed transactions preserve invariants that cross those groups.

**Evidence anchors:**
- Cloud Spanner organizes rows into splits, each replicated across failure domains and managed by a Paxos replica set.
- Leaders handle writes for their Paxos groups; cross-group read-write transactions require coordination across leaders and participants.
- The OSDI paper combines Paxos replication, two-phase commit, and timestamp assignment so sharding does not erase SQL transaction semantics.

**Triple verification:**
- **Cross-domain recurrence:** Shows up in storage layout, replication, write routing, and transaction execution.
- **Generative power:** It predicts that poor primary-key locality, hot splits, or cross-split invariants will dominate latency even if SQL syntax is simple.
- **Exclusivity:** Many sharded databases ask applications to give up cross-shard invariants; this lens preserves them but charges for coordination.

**Application:** Review primary keys, interleaving/locality, split behavior, leader placement, and which transactions cross splits or regions.

**Limit:** The abstraction can hide coordination until production. "It is just SQL" does not mean every transaction has local cost.

### 3. Read Freshness Has Multiple Prices

**One sentence:** Strong reads, stale reads, snapshot reads, and lock-free read-only transactions are different contracts over timestamp choice and replica freshness.

**Evidence anchors:**
- The Spanner paper describes globally consistent reads at a timestamp, lock-free read-only transactions, and non-blocking reads in the past.
- Cloud Spanner read/write documentation distinguishes read-only transactions from read-write transactions; read-only transactions can be strong without taking write locks.
- Replication docs note that replicas can serve reads, but strong reads may consult leadership or ensure the replica is current enough.

**Triple verification:**
- **Cross-domain recurrence:** Applies to OLTP queries, analytics snapshots, backups, and replica placement.
- **Generative power:** It asks which reads need "latest," which can run at a bounded stale timestamp, and which can use an exact historical snapshot.
- **Exclusivity:** Generic SQL thinking often collapses reads into one bucket; Spanner-style design makes timestamp choice an explicit lever.

**Application:** State each read path's freshness contract, allowed staleness, replica target, and whether it can tolerate reading at a past timestamp.

**Limit:** Stale and historical reads reduce coordination, but they are not a free substitute for user-visible correctness where latest state matters.

### 4. SQL Is a Contract Over Placement

**One sentence:** Global SQL only works well when schema, primary keys, indexes, and interleaving encode locality rather than fighting it.

**Evidence anchors:**
- The OSDI paper motivates SQL-like querying because applications wanted familiar data access and cross-row transactions beyond Bigtable-style APIs.
- Spanner schemas use primary-key order and interleaving/locality ideas so related rows can live near each other.
- Cloud Spanner split and replication docs show that physical placement follows key ranges and instance configuration, not arbitrary query wishes.

**Triple verification:**
- **Cross-domain recurrence:** Affects data modeling, transaction scope, query planning, index design, and region placement.
- **Generative power:** It predicts that a "normalized SQL" model can become globally expensive if related rows scatter across leaders and regions.
- **Exclusivity:** Traditional single-region SQL tuning rarely treats geographic placement as part of schema design.

**Application:** Evaluate whether the schema clusters entities by transactional access pattern, whether secondary indexes create remote write amplification, and where leaders should sit.

**Limit:** Locality-optimized schemas can be less flexible for ad hoc access patterns; analytics may need separate pipelines or historical snapshots.

### 5. Schema Changes Are Distributed Transactions Too

**One sentence:** At global scale, schema evolution must be timestamped and coordinated so old and new interpretations do not race across millions of participants.

**Evidence anchors:**
- The OSDI paper describes non-blocking atomic schema changes assigned a future timestamp.
- Reads and writes that depend on the schema must synchronize with the registered schema-change timestamp.
- The paper contrasts this with blocking schema changes that would be infeasible across huge participant sets.

**Triple verification:**
- **Cross-domain recurrence:** Applies to DDL, application rollout, read/write compatibility, and large-scale operations.
- **Generative power:** It asks "at what timestamp does the schema become true, and what must block before or after it?"
- **Exclusivity:** Many systems treat migrations as operational scripts; this lens treats DDL as part of the consistency protocol.

**Application:** Pair schema migrations with compatibility windows, timestamped rollout ordering, backfill strategy, and client-version assumptions.

**Limit:** Timestamped DDL helps coordination, not semantic compatibility. Applications can still break if code and data evolution are not staged.

## Decision Heuristics

1. Do not ask for "global SQL" until the decision names the invariant that truly needs external consistency.
2. Budget commit wait from the clock uncertainty bound, not from wishful single-region latency assumptions.
3. Put write leaders near write-heavy users when possible; put read replicas near readers only after defining read freshness.
4. Model primary keys from transaction locality: tenant, account, customer, order, or workflow instance before generic surrogate IDs.
5. Count remote secondary-index writes and cross-split transactions as part of the write path, not as query-layer details.
6. Use stale or exact-staleness reads for dashboards, exports, and analytics when the product can state the staleness budget.
7. Treat schema migration as an externally visible consistency event with rollout order, compatibility, and rollback design.
8. Prefer a managed global SQL database when the organization needs the guarantee more than it wants to build clock, quorum, and placement infrastructure.
9. If a workload accepts conflicting writes and later merge, choose an AP/CRDT/event-sourcing strategy instead of pretending Spanner-style external consistency is required.
10. Make failure modes user-visible in the ADR: quorum loss, leader-region outage, clock uncertainty expansion, hot split, and cross-region tail latency.

## Schools and Design Tensions

- **External consistency vs AP availability:** Spanner chooses a real-time serial order for transactions; AP systems accept divergent writes and repair later.
- **TrueTime-style bounded clocks vs timestamp oracle:** Bounded clocks decentralize timestamp reasoning but require specialized time infrastructure; timestamp services centralize authority but can become bottlenecks or availability concerns.
- **Strong reads vs bounded stale reads:** Strong reads preserve the simplest mental model; stale reads often buy lower latency and higher locality for non-critical paths.
- **SQL abstraction vs physical locality:** SQL hides distribution from application code, but schema and indexes still decide whether the workload is local or global.
- **Managed service vs self-built NewSQL:** Managed Spanner shifts hard infrastructure to the provider; self-built systems demand deep expertise in consensus, clocks, storage, and operations.

## Would Not Do / Antipatterns

- Would not claim external consistency from NTP-synchronized clocks without a bounded-uncertainty API and commit-wait protocol.
- Would not sell global SQL as "no trade-offs"; every write has quorum, leader, placement, and tail-latency consequences.
- Would not place all leaders in one region while promising symmetric low-latency global writes.
- Would not use random primary keys for entities that have strong transactional locality.
- Would not hide read staleness behind vague words like "near real time"; state exact consistency or staleness contracts.
- Would not use Spanner-style guarantees for cache invalidation, ephemeral sessions, append-only telemetry, or workflows that tolerate compensation.
- Would not run schema changes as out-of-band scripts that race with application versions and long-running reads.

## Honest Boundaries

- This lens is based on public Spanner and Cloud Spanner material, not internal Google operational data.
- It is strongest for architecture decisions about globally distributed OLTP and consistent SQL, not for analytics warehouse design, event streaming, or offline sync.
- It does not prove that Cloud Spanner is the right product; CockroachDB, YugabyteDB, TiDB, PostgreSQL plus regional architecture, or event-driven designs may fit different constraints.
- It assumes non-Byzantine failures and trusted infrastructure. It does not cover malicious replicas or adversarial clocks.
- The local corpus survey is a compact note, not a benchmark. Validate latency, leader placement, split behavior, and cost against the actual workload.

## Roundtable Output Contract

When Architecture Buddy asks this lens to contribute, answer only in this shape:

```text
## Lens: Spanner SQL
### On the decision point
State whether the proposal truly needs externally consistent global SQL, which invariants require it, and which paths can use weaker locality-friendly contracts.

### Heuristics applied
Name the specific time/commit-wait, Paxos-split, read-freshness, schema-locality, or migration heuristics used. Tie each to the decision, not to generic distributed-database advice.

### Risks / what this lens would worry about
Call out clock uncertainty, commit wait, quorum and leader placement, cross-split transactions, hot keys, remote indexes, stale-read misuse, schema rollout, and cost/tail-latency risks where relevant.

### Would not do
List concrete design moves this lens would reject for this decision.

### Evidence style
Use the Spanner OSDI paper, Cloud Spanner replication/read-write architecture docs, external consistency explanations, and workload-specific latency/placement measurements. Mark assumptions that need validation.
```

## Appendix: Research Sources

The maintainer corpus and build instructions used to distill this lens are not required at runtime.

Public sources:
- Google Research, "Spanner: Google's Globally-Distributed Database": https://research.google/pubs/spanner-googles-globally-distributed-database-2/
- OSDI 2012 paper PDF: https://static.googleusercontent.com/media/research.google.com/en/us/archive/spanner-osdi2012.pdf
- Cloud Spanner replication documentation: https://docs.cloud.google.com/spanner/docs/replication
- Cloud Spanner "Life of Spanner Reads & Writes": https://cloud.google.com/spanner/docs/whitepapers/life-of-reads-and-writes
- Google Cloud Blog, "Strict Serializability and External Consistency in Spanner": https://cloud.google.com/blog/products/databases/strict-serializability-and-external-consistency-in-spanner
