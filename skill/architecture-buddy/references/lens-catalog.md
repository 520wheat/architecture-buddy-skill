# Lens Catalog (runtime)

Source: `docs/design/lens-catalog.md` — compressed for Architecture Buddy host.
Dynamic seating: pick ≤3 installed lenses by best-for / not-for (ADR-0017). Distills practices, not voice (ADR-0016).

| shortname | package dir | best-for (summary) | not-for (summary) | tensions with |
|-----------|-------------|--------------------|-------------------|---------------|
| raft-cp | architecture-buddy-lens-raft-cp | CP metadata, membership, fencing, control plane | bulk business data; AP write paths | dynamo-ap, spanner-sql (scope of strong consistency) |
| dynamo-ap | architecture-buddy-lens-dynamo-ap | available KV, global writes, conflict-tolerant data | linearizable ledgers/locks | raft-cp, spanner-sql |
| log-stream | architecture-buddy-lens-log-stream | event integration, audit, replay, multi-consumer | log as cross-service XA silver bullet | often pairs with either CP or AP stores |
| gfs-mr | architecture-buddy-lens-gfs-mr | batch/scan analytics, move compute to data | low-latency OLTP / small files | spanner-sql (OLTP vs batch) |
| spanner-sql | architecture-buddy-lens-spanner-sql | global external consistency + SQL | AP-first / offline merge | dynamo-ap |
| zta-resource | architecture-buddy-lens-zta-resource | Zero Trust resource access, PEP placement | perimeter-only security as sole model | orthogonal; seat when trust boundary is the fork |
| agent-loop | architecture-buddy-lens-agent-loop | LLM tool loops, permissions/HITL, session bounds, tracing, agent runtime | product module maps as architecture; unguarded full autonomy; no observe loop | often pairs with zta-resource on trust; not a substitute for log-stream/CP/AP stores |

Scaffold (`architecture-buddy-lens-scaffold`) is for contract testing only — prefer real stance lenses when installed.
