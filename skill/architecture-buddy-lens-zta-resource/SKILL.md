---
name: architecture-buddy-lens-zta-resource
description: >
  Use when Architecture Buddy roundtable needs a Zero Trust resource lens for trust
  assumptions, access paths, policy enforcement, identity or device posture,
  micro-segmentation, or continuous authorization without network-location trust.
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (ZTA Resource)
  version: "0.1.0"
  stance: "Do not trust a subject, device, or workload because of where it is on the network; authorize access to each resource explicitly and continuously."
  best-for: "Zero Trust Architecture, resource access, PEP placement, trust boundaries, continuous authorization, least privilege"
  not-for: "Generic security checklisting, persona roleplay, or replacing threat modeling and ASVS control verification"
  evidence-anchors: "NIST SP 800-207; OWASP ASVS V1; OWASP SAMM Secure Architecture"
---

# Architecture Buddy Lens — ZTA Resource

This is a **heuristic lens**, not a person or roleplay character. It applies the zero trust resource stance from NIST SP 800-207 to Architecture Buddy roundtables: every protected resource needs an explicit decision path, enforcement point, and revocation story.

## Seat Metadata

- **Best for:** Zero Trust Architecture, resource-centric access, PEP placement, identity/device posture, least privilege, segmentation, continuous authorization.
- **Not for:** Broad security review without an access decision point, compliance-only checkboxing, or replacing ASVS/SAMM verification.
- **Evidence anchors:** NIST SP 800-207 for ZTA principles and PE/PA/PEP logic; OWASP ASVS V1 for verifiable architecture controls; OWASP SAMM Secure Architecture for organizational maturity and reusable patterns.

## Framework Overview

### 1. Network Location Is Not Trust

**One-line model:** Local network, VPN, subnet, or asset ownership is context, not authorization.

**Evidence:**
- NIST SP 800-207 states that no asset is inherently trusted and that enterprise networks may already be compromised.
- NIST requires authentication and authorization before sessions and calls for minimizing implicit trust zones.
- ASVS V1 requires documented trust boundaries and security controls enforced in trusted layers, not in untrusted clients.

**Application:** Ask what would still be allowed if the "internal" network were hostile. Replace "inside the VPC" or "behind VPN" as a trust argument with identity, device posture, workload identity, resource sensitivity, and request context.

**Limit:** This does not mean every legacy implicit trust zone can disappear immediately. It means the design must name remaining implicit zones and shrink them over time.

### 2. Resource-Centric Authorization

**One-line model:** The protected object is the resource, not the network segment around it.

**Evidence:**
- NIST frames access decisions around enterprise resources and communication paths from subject to resource.
- NIST deployment models vary by resource/workflow: device agent/gateway, enclave gateway, and resource portal can coexist in one enterprise.
- ASVS maps data classification and protection requirements into architecture, reinforcing that resource sensitivity should drive controls.

**Application:** Start with a resource inventory and sensitivity map. For each resource or resource group, define who can access it, through which PEP, under what conditions, and how access is revoked.

**Limit:** Resource-centric design can increase policy and inventory complexity. Without good asset, identity, and data classification hygiene, policies become inaccurate or unmaintainable.

### 3. PE / PA / PEP Separation

**One-line model:** Separate policy decision, policy administration, and enforcement so the design has a clear control plane and data plane.

**Evidence:**
- NIST defines Policy Engine (PE), Policy Administrator (PA), and Policy Enforcement Point (PEP) as core logical components.
- NIST separates control-plane communication (PE/PA to PEP) from application data-plane traffic.
- ASVS favors centralized, simple, reusable, and reviewed security controls over duplicated enforcement logic.

**Application:** In the roundtable, locate the PE, PA, and PEP. Identify which component decides, which component establishes or tears down the path, and which component blocks, monitors, or terminates traffic.

**Limit:** Logical separation does not require three products. It does require that the architecture not hide these responsibilities inside vague "gateway" or "platform handles it" claims.

### 4. Continuous, Contextual Authorization

**One-line model:** Access is not a one-time login result; risk can change during the session.

**Evidence:**
- NIST allows continuous session evaluation using identity, device posture, request context, threat intelligence, CDM signals, and resource sensitivity.
- NIST trust algorithms may use static rules or dynamic risk scoring; both are policy choices under the same mechanism.
- ASVS requires consistent authentication/authorization strength across paths and component-to-component communication authentication.

**Application:** Ask what events cause re-evaluation: device posture change, user risk change, token age, unusual request, threat intel, resource sensitivity change, or policy update. Require a revocation and session termination path.

**Limit:** Continuous authorization has operational cost. Overly chatty checks can break reliability or user experience; overly static checks keep stale trust alive.

### 5. Maturity Turns Patterns Into Defaults

**One-line model:** ZTA is not only a per-system diagram; organizations need reusable secure patterns and governed technology choices.

**Evidence:**
- OWASP SAMM Secure Architecture moves from training, to secure design patterns, to reference architectures and continuous assessment.
- SAMM Technology Management moves from identifying risk, to standardizing frameworks, to enforcing approved technologies.
- ASVS describes architecture as a way to reason about multiple valid implementations rather than a single correct implementation.

**Application:** Check whether the proposed ZTA approach is a one-off exception or an adopted pattern: reference architecture, standard PEP options, identity source rules, device posture sources, logging requirements, and review checkpoints.

**Limit:** Maturity models do not choose the correct PEP placement for a specific workflow. They ensure the organization can repeat and verify the choice.

## Decision Heuristics

1. If the argument says "trusted network," translate it into named subjects, devices, workloads, resources, and policies.
2. Put the PEP as close to the protected resource as the workflow and legacy constraints allow.
3. Keep the implicit trust zone behind a PEP small enough to name, monitor, and eventually shrink.
4. Treat identity, device posture, workload identity, threat intelligence, and resource sensitivity as inputs to one explicit decision, not separate checkboxes.
5. Separate logical responsibilities: PE decides, PA establishes or tears down the path, PEP enforces and monitors.
6. Prefer centralized, reviewed authorization controls over duplicated authorization logic in many services or clients.
7. Model revocation before approval: ask how the system removes access when risk changes.
8. Use different deployment models per workflow when needed; do not force a single portal, gateway, or agent pattern across unlike resources.
9. Pair ZTA design with ASVS-style verifiable controls and SAMM-style organizational adoption.
10. When legacy constraints force enclave trust, label the enclave boundary, data flows, and residual lateral-movement risk.

## Schools / Design Tensions

- **Identity-first vs resource/gateway-first:** Enhanced identity governance works well for SaaS, BYOD, and open networks; gateway or micro-segmentation patterns often fit legacy resources and finer network control. Strong designs usually combine them.
- **Static policy vs adaptive risk:** Static policies are easier to reason about and audit; adaptive risk scoring can respond to live context but adds explainability and operations burden.
- **Per-resource PEP vs enclave gateway:** Per-resource enforcement shrinks implicit trust but can be hard to retrofit; enclave gateways ease migration but preserve trust inside the enclave.
- **Portal simplicity vs concentration risk:** A resource portal simplifies user flow and browser access, but it becomes a high-value enforcement and availability dependency.
- **Security rigor vs operability:** Continuous evaluation and posture checks improve control, but poor tuning creates outages, false denies, and support load.

## Would Not Do / Anti-Patterns

- Would not approve "inside the VPN/VPC" as the main authorization claim.
- Would not place authorization enforcement only in an untrusted client or front-end.
- Would not describe "Zero Trust" only as MFA, SSO, or micro-segmentation.
- Would not allow multiple paths to the same resource with weaker authentication or authorization on one path.
- Would not use one large enclave gateway while pretending lateral movement risk is solved.
- Would not skip resource classification and then write broad policies against vague resource groups.
- Would not accept a policy decision without an enforcement, monitoring, and revocation path.
- Would not turn ZTA into product selection before naming trust assumptions and protected resources.

## Honest Boundaries

- This lens does not replace threat modeling; it provides questions that should feed threat modeling.
- This lens does not guarantee compliance with NIST, ASVS, or SAMM; it helps align architecture discussion with their concepts.
- ZTA adoption is incremental. Some implicit trust may remain in legacy zones, but it must be explicit and governed.
- Continuous authorization depends on signal quality. Bad identity, device, asset, or telemetry data can make the policy engine confidently wrong.
- The lens is strongest for access-path and resource-protection decisions; it is weaker for unrelated security topics such as secure coding details, cryptographic primitive choice, or incident response process.

## Roundtable Output Contract

```text
## Lens: ZTA Resource
### On the decision point
State whether the proposal relies on network location, broad enclave trust, client-side enforcement, or one-time authentication.

### Heuristics applied
Name the relevant ZTA checks: resource scope, PE/PA/PEP responsibilities, PEP placement, continuous authorization signals, trust boundary size, and revocation path.

### Risks / what this lens worries about
List concrete failure modes such as lateral movement, bypass paths, stale sessions, weak alternate routes, over-broad resource groups, or ungoverned policy sprawl.

### Would not do
Call out the specific anti-pattern this proposal should avoid.

### Evidence style
Anchor claims in NIST SP 800-207 terms first, then use ASVS V1 for verifiable architecture requirements and SAMM for maturity or reference-architecture questions.
```

## Appendix: Research Sources

- NIST SP 800-207, Zero Trust Architecture:
  - Source: https://csrc.nist.gov/pubs/sp/800/207/final
  - PDF: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf
- OWASP SAMM Secure Architecture:
  - Source: https://owaspsamm.org/model/design/secure-architecture/
- OWASP ASVS V1 Architecture:
  - Source: https://asvs.dev/v4.0.3/V1-Architecture/
