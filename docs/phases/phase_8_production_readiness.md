# Talk-to-Data Delivery Blueprint — Phase 8: Production Readiness & Controlled Release

*Daniel Brule · Talk-to-Data Delivery Blueprint · v1.0 · June 2026*

---

**Table of contents**

- [1 Executive summary](#1-executive-summary)
- [2 Phase overview](#2-phase-overview)
  - [2.1 Objective](#21-objective)
  - [2.2 Scope of the phase](#22-scope-of-the-phase)
  - [2.3 What this phase does not do](#23-what-this-phase-does-not-do)
  - [2.4 Expected duration and level of effort](#24-expected-duration-and-level-of-effort)
  - [2.5 Main participants and decision owners](#25-main-participants-and-decision-owners)
- [3 Production-readiness decision and release implications](#3-production-readiness-decision-and-release-implications)
  - [3.1 Possible Phase 8 outcomes](#31-possible-phase-8-outcomes)
  - [3.2 Minimum conditions for controlled production release](#32-minimum-conditions-for-controlled-production-release)
  - [3.3 Issue disposition and release constraint model](#33-issue-disposition-and-release-constraint-model)
  - [3.4 Common reasons to release, constrain, harden or stop](#34-common-reasons-to-release-constrain-harden-or-stop)
  - [3.5 How Phase 8 shapes Phase 9 operations and scaling](#35-how-phase-8-shapes-phase-9-operations-and-scaling)
- [4 Production-readiness activities overview](#4-production-readiness-activities-overview)
  - [4.1 Activity sequence](#41-activity-sequence)
  - [4.2 Release control model](#42-release-control-model)
  - [4.3 Activity logic](#43-activity-logic)
  - [4.4 Release-depth expectations](#44-release-depth-expectations)
- [5 Core production-readiness activities](#5-core-production-readiness-activities)
  - [5.1 Confirm production scope and release boundary](#51-confirm-production-scope-and-release-boundary)
  - [5.2 Triage pilot findings and production-readiness backlog](#52-triage-pilot-findings-and-production-readiness-backlog)
  - [5.3 Complete pre-release hardening and regression checks](#53-complete-pre-release-hardening-and-regression-checks)
  - [5.4 Confirm production control readiness](#54-confirm-production-control-readiness)
  - [5.5 Confirm operational reliability and observability](#55-confirm-operational-reliability-and-observability)
  - [5.6 Prepare support, documentation, onboarding and controlled adoption readiness](#56-prepare-support-documentation-onboarding-and-controlled-adoption-readiness)
  - [5.7 Consolidate operating model, budget and roadmap capacity](#57-consolidate-operating-model-budget-and-roadmap-capacity)
  - [5.8 Approve and execute controlled release, residual-risk acceptance and Phase 9 handover](#58-approve-and-execute-controlled-release-residual-risk-acceptance-and-phase-9-handover)
- [6 Controlled release decision pack](#6-controlled-release-decision-pack)
  - [6.1 Controlled production release pack](#61-controlled-production-release-pack)
  - [6.2 Release pack quality test](#62-release-pack-quality-test)
- [7 Exit criteria and handover](#7-exit-criteria-and-handover)
  - [7.1 Required exit outputs](#71-required-exit-outputs)
  - [7.2 Handover to Phase 9](#72-handover-to-phase-9)
  - [7.3 Exit decision wording](#73-exit-decision-wording)
  - [7.4 Practitioner note](#74-practitioner-note)
- [8 Key risks and failure modes](#8-key-risks-and-failure-modes)

---

## 1 Executive summary

Phase 8 determines whether the controlled pilot can become a controlled production release, and how that release should be fixed, scoped, governed, funded, supported and handed over.

It builds on Phase 7 evidence: real usage, workflow fit, trust, supportability, access lifecycle, cost, latency, monitoring gaps, hot fixes and the production-readiness backlog. The goal is to decide what can go live, what must be fixed first, what constraints apply, and what should move into Phase 9.

Phase 8 is not another pilot, a feature-expansion exercise or a broad adoption push. The standard is higher than pilot acceptance: users must be able to rely on the system within a defined production boundary, with critical fixes completed, controls enforceable, support ready, onboarding clear, budget confirmed and residual risks accepted.

A controlled production release can be narrow. It may be limited by user group, data domain, question type, answer type, risk level, usage volume or support model. This is not a failure; it is often the safest way to protect trust while the foundation, operating model and roadmap mature.

By the end of Phase 8, stakeholders should be able to decide whether to release, release with constraints, harden further, narrow the scope, return to an earlier phase, redesign, pause or stop. Where release is approved, the phase should produce the release package and handover required for Phase 9 operations, adoption, monitoring and selective scaling.

**  
**

## 2 Phase overview

### 2.1 Objective

The objective of Phase 8 is to convert the Phase 7 production-readiness recommendation into a controlled production release outcome.

Phase 7 decides whether the pilot evidence justifies moving towards production readiness. Phase 8 decides whether release can actually happen, after release-critical fixes, production controls, support, ownership, budget, onboarding and residual-risk acceptance have been confirmed.

Phase 8 confirms what can go live, what must be fixed before release, what can only be released with constraints, what risk must be accepted, and what should move into Phase 9 operations, adoption, monitoring and selective scaling.

The phase should include a focused hardening window. Release-critical defects, control gaps, documentation gaps or support-readiness issues should be fixed before go-live, with targeted regression checks. Phase 9 should not absorb unfinished production-readiness work unless the risk is explicitly accepted and controlled.

### 2.2 Scope of the phase

Phase 8 covers the final readiness work required to move from controlled pilot to controlled production release. The minimum scope should include:

- confirming the production release boundary by user group, data domain, question type, answer type, usage level and support model;

- triaging Phase 7 findings, hot fixes, user feedback, support issues and the production-readiness backlog;

- fixing release-critical issues and running targeted regression checks;

- confirming production controls across data, semantics, metadata, access, security, auditability and compliance;

- confirming operational readiness across reliability, latency, cost, capacity, monitoring, alerting, logging and incident response;

- refreshing support material, runbooks, release notes, known limitations, onboarding material and escalation routes;

- sizing support, bug-fix, improvement and roadmap capacity, including budget and ownership;

- confirming residual-risk acceptance, change rights, release approval and Phase 9 handover.

Phase 8 should be proportionate to the release exposure. A small controlled release may require a lightweight but explicit release package. A broader or higher-risk release requires stronger evidence, clearer sign-off, more formal support arrangements and more mature monitoring.

### 2.3 What this phase does not do

Phase 8 is not a second pilot. If more user evidence is needed, the appropriate decision may be to extend or redesign the pilot, not to disguise further testing as production readiness.

Phase 8 is not broad adoption. It may include onboarding the first production users, but it should not drive enterprise-wide rollout, behavioural change at scale or expansion to all interested users. Those belong in Phase 9, once the first production release is operating safely.

Phase 8 is not feature expansion. Additional user groups, domains, question types, integrations or answer formats should only be added if they are required for the approved release boundary and are supported by evidence. Otherwise, they should move into the Phase 9 roadmap.

Phase 8 is not a full rebuild or a repeat of Phase 6 validation. If Phase 7 reveals structural blockers in the data foundation, semantic layer, architecture, controls or operating model, the correct response is to return to the relevant earlier phase, narrow the release or stop. Phase 8 may fix release-critical issues, but it should not silently absorb redesign work.

### 2.4 Expected duration and level of effort

Phase 8 typically takes two to four weeks for a narrow controlled release, depending on the number of release-critical issues, the maturity of the support model, the governance route and the complexity of the production environment.

A lightweight release may focus on final fixes, regression checks, release sign-off, onboarding and support handover. A higher-risk release may require deeper hardening, formal risk acceptance, stronger monitoring, cost approval, security sign-off and operating-model sizing.

The phase should have a clear cut-off. Without one, production readiness can become an endless improvement loop. The goal is to fix what must be fixed before release, constrain what cannot yet be supported, and defer only what the live service can genuinely operate with.

### 2.5 Main participants and decision owners

Phase 8 requires both delivery and operating stakeholders. Core participants typically include the business sponsor, product owner, delivery lead, data and semantic owners, engineering or platform owner, security / risk / compliance representatives, support owner, finance owner, onboarding lead and representative users.

Before release, decision rights should be explicit. The product or business owner approves the release boundary. Data and semantic owners approve governed content in scope. Security, risk and compliance approve relevant controls and residual risks. Engineering approves operational readiness. Support accepts the support model. Finance confirms run and change funding.

If these ownership roles cannot be named, Phase 8 should not approve a production release.

## 3 Production-readiness decision and release implications

### 3.1 Possible Phase 8 outcomes

Phase 8 should end with an explicit release outcome. The decision should not be reduced to simple go / no-go, because controlled production release may be approved under constraints.

| Outcome                        | Meaning                                                                                             |
|--------------------------------|-----------------------------------------------------------------------------------------------------|
| **Release**                    | Ready for controlled production use within the agreed boundary.                                     |
| **Release with constraints**   | Release is approved only for defined users, domains, question types, volumes or support conditions. |
| **Complete further hardening** | Release is delayed until specific fixes, controls or regression checks are complete.                |
| **Narrow the scope**           | The original ambition is too broad, but a smaller release remains viable.                           |
| **Return to an earlier phase** | A blocker requires renewed work on data, semantics, architecture, validation or pilot evidence.     |
| **Redesign / pause / stop**    | The current value, risk, cost, ownership or support case does not justify release.                  |

The decision should record the rationale, release boundary, constraints, owners, accepted risks and Phase 9 handover conditions.

### 3.2 Minimum conditions for controlled production release

A controlled production release should only be approved when users can rely on the system within a defined boundary.

At minimum, Phase 8 should confirm that release-critical issues are fixed and regression-tested; production scope is explicit; data, semantic, metadata, access, security and audit controls are enforceable; monitoring, logging, alerting, cost tracking and incident response are ready; support routes, runbooks and escalation paths are defined; users are onboarded; ownership, funding, change rights and residual-risk acceptance are explicit; and Phase 9 has enough capacity to run, fix, improve and selectively scale the capability.

These conditions do not require perfection. They require enough evidence, control and ownership for production reliance.

### 3.3 Issue disposition and release constraint model

Phase 8 should classify every material Phase 7 finding before release. Issues should not remain in a generic backlog.

| Classification               | Meaning                                          | Release implication                               |
|------------------------------|--------------------------------------------------|---------------------------------------------------|
| **Production blocker**       | Unsafe or unworkable for production.             | Fix before release, narrow, redesign or stop.     |
| **Pre-release fix**          | Fixable issue required for controlled release.   | Resolve during Phase 8 and regression test.       |
| **Release constraint**       | Issue can be managed by limiting scope or usage. | Release only under explicit constraint.           |
| **Accepted residual risk**   | Known risk accepted by accountable owner.        | Record owner, rationale and review conditions.    |
| **Monitored risk**           | Acceptable only if actively watched.             | Add threshold, owner and response route.          |
| **Post-release improvement** | Useful, but not required for first release.      | Add to Phase 9 backlog.                           |
| **Redesign / stop signal**   | Indicates a structural weakness.                 | Return to earlier phase, redesign, pause or stop. |

Production readiness is a balance, not a search for perfection. The standard is not “no issues”; it is whether the remaining issues are understood, owned, constrained, monitored or accepted well enough for users to rely on the system within the approved boundary.

### 3.4 Common reasons to release, constrain, harden or stop

Release is appropriate when pilot value is clear, the production scope is evidenced, critical fixes are complete, controls are enforceable, support is ready, cost is approved and ownership is explicit.

Release with constraints is appropriate when the capability is useful but only safe under limits such as named users, approved domains, supported question types, usage caps, enhanced support cover or temporary exclusions.

Further hardening is required when the release case is strong but specific gaps remain, such as incomplete regression evidence, weak monitoring thresholds, missing runbooks, unclear support process, unstable latency, cost uncertainty, access lifecycle gaps or documentation not aligned with the final release boundary.

Return, redesign, pause or stop is required when Phase 8 exposes a structural issue that hardening cannot fix, such as untrusted data, contested metrics, unsafe access enforcement, unsuitable architecture, weak validation evidence, unaffordable run cost or no accountable production owner.

### 3.5 How Phase 8 shapes Phase 9 operations and scaling

Phase 8 should hand over more than release approval. It should define what has been released, what remains out of scope, which risks and constraints must be monitored, who owns support and change, and what must happen before the capability expands.

The Phase 9 roadmap should be capacity-aware and evidence-led. It should separate four lanes: **run**, **fix**, **improve** and **expand**. Expansion should only happen when the foundation, controls, support model and budget can absorb it.

The main output of Phase 8 is therefore a controlled release contract: the approved boundary, completed fixes, remaining constraints, accepted risks, operating commitments and roadmap conditions for safe evolution.

## 4 Production-readiness activities overview

### 4.1 Activity sequence

Phase 8 should follow a controlled release sequence. The aim is not to re-test everything from previous phases, but to turn pilot evidence into a release outcome that can be operated safely.

| Step | Activity                                                                     | Main question                                                                                |
|------|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| 1    | Confirm production scope and release boundary                                | What exactly can go live?                                                                    |
| 2    | Triage pilot findings and production-readiness backlog                       | What must be fixed, constrained, accepted, monitored or deferred?                            |
| 3    | Complete pre-release hardening and regression checks                         | Have release-critical issues been fixed without breaking anything else?                      |
| 4    | Confirm production control readiness                                         | Are data, semantic, access, security and audit controls enforceable?                         |
| 5    | Confirm operational reliability and observability                            | Can the service be monitored, supported and paused if needed?                                |
| 6    | Prepare support, documentation, onboarding and controlled adoption readiness | Are users and support teams ready for the first production release?                          |
| 7    | Consolidate operating model, budget and roadmap capacity                     | Are the cost, capacity and roadmap implications from all Phase 8 work understood and funded? |
| 8    | Approve controlled release and Phase 9 handover                              | Is the release approved, owned and handed over with clear conditions?                        |

The sequence can be iterative. For example, issue triage may change the release boundary, hardening may reveal new regression risks, and operating-model sizing may force a narrower release. The important point is that Phase 8 should end with one coherent release position, not separate technical, business and support opinions.

### 4.2 Release control model

A controlled production release should be defined by explicit release controls. These controls prevent a pilot from expanding silently into unsupported production use.

| Control           | What it defines                                                                     |
|-------------------|-------------------------------------------------------------------------------------|
| User boundary     | Which users or groups can access the release.                                       |
| Domain boundary   | Which data domains, sources and governed assets are in scope.                       |
| Question boundary | Which question types, metrics, dimensions and follow-ups are supported.             |
| Answer boundary   | Which answer formats are supported, caveated, refused or excluded.                  |
| Risk boundary     | Which use cases are low enough risk for controlled production.                      |
| Usage boundary    | Expected user numbers, query volumes, latency limits and cost limits.               |
| Support boundary  | What support is available, when, by whom and for which issue types.                 |
| Change boundary   | Who can approve changes to scope, prompts, models, data assets, controls or access. |

These boundaries should be visible in the release decision, user guidance, support material and Phase 9 handover. If users, support teams or owners cannot explain the release boundary, the release is not controlled.

### 4.3 Activity logic

The activity logic is deliberately practical:

- **Start with scope.** Production scope should be selected from evidence, not from total pilot demand.

- **Classify issues before fixing.** Not every issue deserves the same response; some block release, some constrain it, some can be monitored, and some belong in the roadmap.

- **Fix before handover.** Release-critical issues should be closed in Phase 8, not left for Phase 9 to discover under production pressure.

- **Confirm controls as operating controls.** Phase 8 is not asking whether controls passed a test once; it asks whether they are enforceable, monitored and owned in production.

- **Prepare people as well as the system.** Support teams, users, owners and governance stakeholders need to understand the release boundary before access is enabled.

- **Track cost throughout.** Each Phase 8 activity should identify cost and capacity implications. Activity 7 consolidates these into the run budget, support model and roadmap capacity decision.

- **Approve with conditions.** A release decision should state what is approved, what is constrained, what is accepted and what would trigger pause, rollback or return to an earlier phase.

### 4.4 Release-depth expectations

Not every release needs the same level of documentation or formality. The level of evidence should match the exposure, risk and organisational maturity.

| Output level | When appropriate                                                                              | Typical evidence                                                                                                                                          |
|--------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Lightweight  | Narrow internal release, low-risk questions, limited users, strong existing ownership.        | Release note, final scope, key fixes, support route, basic monitoring, named owners.                                                                      |
| Standard     | Controlled business release, meaningful decision use, multiple owners or moderate risk.       | Release pack, issue disposition, regression evidence, runbooks, onboarding material, cost estimate, residual-risk acceptance.                             |
| Enhanced     | Sensitive data, regulated use, executive decisions, broad exposure or high reputational risk. | Formal sign-off, detailed control evidence, monitoring thresholds, incident process, budget approval, audit trail, capacity model and governance cadence. |

The output level should be agreed early in Phase 8. Over-documenting a narrow release slows delivery; under-documenting a material release creates operational and governance risk.

## 5 Core production-readiness activities

### 5.1 Confirm production scope and release boundary

**Purpose:** Define exactly what can be considered for controlled production release.

**Core activities:**

- Confirm the target production users, user groups and access route.

- Confirm the approved data domains, sources, metrics, dimensions, joins, filters and caveats in scope.

- Define supported question types, answer types, follow-up behaviour and refusal conditions.

- Confirm explicit exclusions, including users, domains, questions, outputs and integrations not ready for release.

- Check that the proposed release boundary is supported by Phase 7 evidence, not only by user demand.

- Identify cost and capacity implications of the proposed release boundary.

**Output:**

- Final production release boundary.

- In-scope and out-of-scope user, data and question list.

- Release assumptions and constraints.

- Boundary-to-evidence mapping.

- Initial cost and capacity implications.

**Red flags:**

- Production scope expands to include all pilot demand.

- Popular but weakly tested questions are included because users asked for them.

- The release boundary is clear to the project team but not to users or support teams.

- New domains, users or answer types are added without data, semantic or support evidence.

- Scope is approved without understanding the cost or capacity impact.

**Practitioner note:**  
Production scope should be earned, not inherited. A narrow release backed by evidence is stronger than a broad release held together by caveats, goodwill and manual support.

### 5.2 Triage pilot findings and production-readiness backlog

**Purpose:** Convert Phase 7 findings into explicit release decisions.

**Core activities:**

- Review pilot issues, user feedback, hot fixes, support findings, access issues, monitoring gaps and known limitations.

- Classify each material item as a production blocker, pre-release fix, release constraint, accepted residual risk, monitored risk, Phase 9 backlog item, later enhancement or redesign signal.

- Confirm which issues must be fixed during Phase 8 before release can proceed.

- Identify items that require scope narrowing, additional controls, user guidance, monitoring or risk acceptance.

- Separate genuine production-readiness work from future product improvement.

- Estimate the cost, effort and capacity impact of each material issue category.

**Output:**

- Production-readiness issue disposition register.

- Pre-release fix and hardening backlog.

- Release constraints and monitored-risk list.

- Residual-risk acceptance candidates.

- Phase 9 backlog and roadmap candidates.

**Red flags:**

- Issues are left in a generic backlog with no release implication.

- “Minor” defects affect trust, access, auditability, cost or support.

- Fixes are accepted without clear owner, evidence or regression path.

- User requests are treated as production requirements.

- The backlog is used to hide a structural data, semantic, architecture or operating-model weakness.

**Practitioner note:**  
The point of triage is not to make the backlog look manageable. It is to decide what the release can genuinely live with. Not all issues are equal: a minor defect in an executive workflow may matter more than a new feature for a low-risk analyst use case

### 5.3 Complete pre-release hardening and regression checks

**Purpose:** Fix release-critical issues and confirm that fixes do not weaken production readiness.

**Core activities:**

- Prioritise production blockers and pre-release fixes from the Phase 8 triage.

- Fix release-critical defects, control gaps, support gaps, documentation gaps and onboarding gaps.

- Confirm whether each fix changes behaviour, scope, prompts, models, data logic, access rules, monitoring or user guidance.

- Run targeted regression checks on affected question types, data assets, prompts, tools, controls and user flows.

- Update release notes, known limitations, runbooks and onboarding material where behaviour has changed.

- Confirm cost, effort and capacity impact of the hardening work and any remaining unresolved items.

**Output:**

- Completed pre-release hardening backlog.

- Fix evidence and targeted regression results.

- Behaviour-change record, release notes and known limitations.

- Reserved fix and regression capacity plan.

- Remaining unresolved issue list with release implication.

**Red flags:**

- Fixes are made without regression checks.

- Prompt, model or data-logic changes alter behaviour but are not communicated.

- The team keeps adding improvements instead of closing release-critical fixes.

- “Temporary” fixes create manual support or monitoring debt.

- New issues appear faster than release-critical issues are closed.

**Practitioner note:**  
Phase 8 needs a hardening window, not an endless improvement loop. Reserve the people needed for critical fixes, regression checks and early-life support before the delivery team is reassigned. Non-regression is critical: a small fix can change prompts, retrieval behaviour, SQL generation, answer wording, access enforcement, cost or latency.

### 5.4 Confirm production control readiness

**Purpose:** Confirm that the release boundary is governed, enforceable and safe to expose in production.

**Core activities:**

- Confirm that production data assets, metrics, dimensions, joins, filters, caveats, metadata and refresh rules are approved and support the release boundary.

- Confirm that access rules, row / column controls, masking, permissions and revocation processes work for production users.

- Check that audit trails, traceability and evidence retention are sufficient for support, governance and review.

- Confirm that security, privacy, compliance, audit and data-owner conditions have been reviewed, signed off where required, and reflected in the production flow.

- Identify any production-control gaps that require fixing, release constraints, monitoring or risk acceptance.

- Capture the cost and capacity impact of maintaining these controls after release.

**Output:**

- Production control readiness summary.

- Approved production data, semantic, metadata and refresh scope.

- Access, security and audit-control evidence.

- Control-owner review / sign-off record.

- Production-control gap list with release implications.

**Red flags:**

- Pilot access rules are reused without confirming production provisioning and revocation.

- Metric, caveat or join ownership is unclear once the project team steps away.

- Controls exist in design documents but are not enforceable in the production flow.

- Audit logs exist but cannot explain who asked what, which data was used, and why an answer was produced.

- Control maintenance depends on manual checks with no owner, cadence or capacity.

**Practitioner note:**  
Production control readiness is not a governance meeting. It is evidence that the approved rules are enforceable in the live release boundary. If a control depends on someone remembering to check a spreadsheet, it is not a production control unless that manual process is owned, funded and time-bound.

### 5.5 Confirm operational reliability and observability

**Purpose:** Confirm that the released system can be monitored, supported and controlled when users rely on it.

**Core activities:**

- Confirm expected usage, concurrency, latency, timeout, availability and cost assumptions for the release boundary.

- Check that logs, traces, dashboards and alerts cover user questions, metadata retrieval, model calls, query execution, answer generation, errors, cost and access decisions.

- Define operational thresholds for latency, failures, cost spikes, data freshness, unsupported questions and repeated user issues.

- Confirm incident response, escalation, pause, rollback and user-communication routes.

- Test that monitoring and alerting work before release, not only that they are documented.

- Capture the cost and capacity required to operate monitoring, incident response and early-life support.

**Output:**

- Operational reliability and observability summary.

- Usage, latency, availability and cost thresholds.

- Monitoring, logging and alerting evidence.

- Incident, escalation, pause and rollback process.

- Operational gaps with release implications.

**Red flags:**

- Dashboards exist but nobody is accountable for reviewing or acting on them.

- Alerts are too noisy, too late or routed to the wrong owner.

- Cost is monitored after the fact rather than controlled before it becomes a problem.

- Support teams cannot trace a user complaint back to the question, data, query, model call and answer.

- There is no agreed trigger for pausing or narrowing the release.

**Practitioner note:**  
A T2D system is not production-ready because it usually works. It is production-ready when the team can see when it stops working, understand why, know who owns the response, and communicate clearly before trust is damaged.

### 5.6 Prepare support, documentation, onboarding and controlled adoption readiness

**Purpose:** Confirm that users, support teams and owners are ready for the first controlled production release.

**Core activities:**

- Refresh user, support, technical and governance documentation against the final release boundary.

- Update release notes, known limitations, supported questions, exclusions, behaviour changes and responsible-use guidance.

- Confirm onboarding material for first production users, including what to trust, what not to use the system for and how to raise issues.

- Confirm support routes, runbooks, escalation paths, incident communication and pause / rollback communication.

- Check that documentation is accessible, versioned, owned and aligned with the latest fixes, constraints and residual risks.

- Capture the cost and capacity required for onboarding, support, documentation maintenance and early-life user assistance.

**Output:**

- Production documentation readiness summary.

- Updated release notes, known limitations and responsible-use guidance.

- User onboarding and controlled adoption material.

- Support runbooks and escalation routes.

- Documentation ownership and maintenance plan.

**Red flags:**

- Users are given access without understanding the supported scope and limitations.

- Support teams cannot explain common failures, constraints or escalation routes.

- Documentation describes the pilot version rather than the production release.

- Behaviour changes from Phase 8 fixes are not reflected in release notes or onboarding.

- Documentation maintenance depends on the delivery team with no post-release owner.

**Practitioner note:**  
Phase 8 documentation is not a writing exercise. It is a readiness check. Users need to know what they can rely on, support teams need to know what to do, and owners need to know what they are accountable for after release.

### 5.7 Consolidate operating model, budget and roadmap capacity

**Purpose:** Confirm that the release has enough funded capacity to run, fix, improve and evolve after go-live.

**Core activities:**

- Consolidate cost and capacity implications from all Phase 8 activities into a role-based operating model for early-life operation.

- Separate capacity needed for run support, bug fixes, controlled improvements and roadmap expansion.

- Estimate run costs across model usage, infrastructure, monitoring, logging, evaluation, data refresh, support and change activity.

- Confirm budget owner, funding route, review cadence and escalation trigger for cost or capacity pressure.

- Identify capacity gaps that may require release constraints, delayed expansion or additional funding.

- Define the Phase 9 roadmap using evidence, capacity and readiness constraints, not only user demand.

**Output:**

- Production operating model and capacity estimate.

- Run-cost and change-budget view.

- Run / fix / improve / expand roadmap.

- Budget owner, funding route and review cadence.

- Capacity gaps and release implications.

**Red flags:**

- Release is approved but support and improvement capacity are assumed rather than reserved.

- Cost estimate covers model usage but ignores people, monitoring, testing, support and change control.

- The roadmap is driven by user demand without checking data, semantic, control or support readiness.

- The original delivery team is expected to provide indefinite operational cover.

- Expansion is planned before the first release has stabilised.

**Practitioner note:**  
Cost and capacity should not appear for the first time in Activity 7. Every Phase 8 activity creates run, fix, support or roadmap implications. Activity 7 consolidates those signals into a funded operating model and a realistic Phase 9 roadmap.

### 5.8 Approve and execute controlled release, residual-risk acceptance and Phase 9 handover

**Purpose:** Make the final controlled release decision and hand over the live capability with explicit conditions.

**Core activities:**

- Confirm that release-critical fixes, regression checks, controls, support, onboarding, monitoring and budget conditions are complete or explicitly constrained.

- Review residual risks and confirm who accepts them, under which conditions and with which review triggers.

- Approve the final release outcome: release, release with constraints, further hardening, narrow, return to earlier phase, redesign, pause or stop.

- Confirm who can approve scope changes, production changes, pause, rollback, user expansion and roadmap prioritisation after release.

- Execute the controlled release or hand over the approved release package to the formal release-management process.

- Transfer Phase 9 ownership for run support, monitoring, incidents, cost review, backlog management, adoption and selective scaling.

**Output:**

- Controlled release decision record.

- Residual-risk acceptance record.

- Final release package and release conditions.

- Phase 9 handover pack with owners, cadence and escalation routes.

- Post-release review and expansion criteria.

**Red flags:**

- Release is approved verbally but not captured with scope, constraints, risks and owners.

- Residual risks are noted by the project team but not accepted by accountable owners.

- Go-live happens before support, monitoring, onboarding or incident routes are active.

- Nobody is empowered to pause, roll back or narrow the release if early issues appear.

- Phase 9 starts with adoption pressure but no agreed run, fix, improve and expand discipline.

**Practitioner note:**  
A controlled release is not a launch announcement. It is an accountable decision to let users rely on the system within a defined boundary. If the organisation cannot name who owns the release, accepts the risk, pays for the run model and can stop the service when needed, the release is not ready.

## 6 Controlled release decision pack

Phase 8 should produce a clear release package, not a loose collection of documents. The outputs should allow stakeholders to understand what is being released, what has been fixed, what remains constrained, who owns the live capability, what it will cost, and how Phase 9 will operate, improve and selectively scale it.

The main output is the **controlled production release pack**. It should be proportionate to the release exposure. A narrow controlled release does not need heavy governance theatre, but it does need enough evidence to show that users can rely on the system within the approved boundary.

### 6.1 Controlled production release pack

The controlled production release pack should include:

| Output                                | What it should prove                                                                                                       |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| **Release decision record**           | The agreed outcome: release, release with constraints, harden further, narrow, return, redesign, pause or stop.            |
| **Final release boundary**            | Users, domains, questions, answer types, exclusions, usage limits and support conditions approved for production.          |
| **Issue disposition register**        | Phase 7 and Phase 8 findings classified as blockers, fixes, constraints, monitored risks, residual risks or backlog items. |
| **Hardening and regression evidence** | Release-critical fixes completed and tested without introducing material regression.                                       |
| **Production control evidence**       | Data, semantic, metadata, access, security, audit, compliance and refresh controls are enforceable and owned.              |
| **Operational readiness evidence**    | Monitoring, alerting, logging, cost tracking, incident response, pause / rollback and support routes are active.           |
| **Support and onboarding material**   | Users and support teams understand scope, limitations, responsible use, escalation and issue reporting.                    |
| **Operating model and budget view**   | Run, fix, improve and expand capacity is sized, funded and owned.                                                          |
| **Residual-risk acceptance record**   | Remaining risks are accepted by accountable owners, with conditions, monitoring and review triggers.                       |
| **Phase 9 handover pack**             | Ownership, review cadence, backlog, roadmap lanes, expansion conditions and post-release review criteria are clear.        |

The release pack should be usable by both delivery and operating stakeholders. If it can only be understood by the project team, it is not ready for handover.

### 6.2 Release pack quality test

Before Phase 8 closes, the outputs should be tested against a simple quality standard.

| Test                      | Question                                                                                             |
|---------------------------|------------------------------------------------------------------------------------------------------|
| **Decision clarity**      | Can a senior stakeholder understand the release outcome and rationale in plain language?             |
| **Boundary clarity**      | Can users, support teams and owners explain what is in and out of scope?                             |
| **Fix evidence**          | Are release-critical fixes linked to regression evidence and release notes?                          |
| **Control evidence**      | Are production controls enforceable, not only documented?                                            |
| **Operational readiness** | Are monitoring, support, incident and pause routes live before release?                              |
| **Ownership clarity**     | Are product, data, semantic, platform, support, finance and risk owners named?                       |
| **Cost clarity**          | Is the release funded beyond go-live, including people, monitoring, support, fixes and roadmap work? |
| **Risk clarity**          | Are residual risks accepted by the right owners, with review triggers?                               |
| **Handover quality**      | Can Phase 9 start operating the capability without relying on informal project knowledge?            |

A Phase 8 output should not be considered complete because a template has been filled. It is complete when it can support a release decision, survive handover, and guide the first weeks of production operation.

## 7 Exit criteria and handover

Phase 8 should close with an explicit release decision and a usable handover. Exit does not always mean go-live. It may mean controlled release, release with constraints, further hardening, narrowed scope, return to an earlier phase, redesign, pause or stop.

The key test is whether the organisation has enough evidence, ownership and operating capacity to act on the decision.

### 7.1 Required exit outputs

The required exit output is the controlled release decision pack described in Section 6, completed to the standard required by release exposure and risk.

The exit decision should confirm whether the capability is approved for release, approved with constraints, delayed for further hardening, narrowed, returned to an earlier phase, redesigned, paused or stopped. It should also identify the final release boundary, issue disposition, hardening evidence, production-control evidence, operational readiness, residual risks, operating model, budget view and Phase 9 handover route.

If the release is not approved, the exit pack should still record what happens next: harden further, narrow scope, return to a previous phase, redesign, pause or stop.

### 7.2 Handover to Phase 9

Where controlled release is approved, Phase 8 hands over to Phase 9 operation, adoption, monitoring and selective scaling. It should confirm:

- what is live, what is constrained and what remains out of scope;

- who owns product value, support, platform operation, data, semantics, security, risk, cost and roadmap;

- which incidents, alerts, access changes, support tickets and user feedback routes are active;

- what early-life review cadence applies;

- which issues are in the **run**, **fix**, **improve** and **expand** lanes;

- what must be true before users, domains, question types or integrations are added;

- what triggers pause, rollback, scope narrowing or return to a previous phase.

Phase 9 should not start by rediscovering the release. It should inherit a clear operating position: live scope, known risks, support model, cost model, backlog, owners and decision rights.

### 7.3 Exit decision wording

The Phase 8 decision should be written clearly enough for business, technical, support and governance stakeholders to understand.

Suggested wording:

| Decision                 | Suggested wording                                                                                                                         |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Release                  | “The capability is approved for controlled production release within the agreed boundary.”                                                |
| Release with constraints | “The capability is approved for production release only under the stated user, data, question, usage, support or monitoring constraints.” |
| Further hardening        | “Release is delayed until the specified fixes, controls, regression checks or support gaps are closed.”                                   |
| Narrow scope             | “The broader release is not approved, but a smaller controlled release remains viable.”                                                   |
| Return to earlier phase  | “A material blocker requires renewed work on data, semantics, architecture, validation or pilot evidence before release can proceed.”     |
| Redesign                 | “The current solution pattern is not suitable for production without material redesign.”                                                  |
| Pause / stop             | “Production release is not justified at this stage due to value, risk, cost, ownership, support or readiness concerns.”                   |

Every decision should include the reason, owner, next action, target date and review route.

### 7.4 Practitioner note

A weak Phase 8 handover creates a fragile Phase 9. The common failure is to celebrate release while leaving support, ownership, monitoring, cost and backlog management vague.

The handover should make the next phase boring in the right way: users know the boundary, support knows what to do, owners know what they own, and governance knows which risks have been accepted. If Phase 9 depends on informal project knowledge or goodwill from a reassigned delivery team, Phase 8 has not really finished.

## 8 Key risks and failure modes

Phase 8 often fails when a successful pilot creates pressure to release before the organisation is ready to operate the capability. The main risk is not that the system has defects. The main risk is that defects, constraints, ownership gaps, cost pressure and support needs are not made explicit before users start relying on the system.

| Risk / failure mode                                   | Why it matters                                                                                                   | Likely response                                                            |
|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| **Pilot success is treated as production readiness**  | Users liked the pilot, but the system may not yet be supportable, monitored, funded or owned.                    | Reconfirm minimum production conditions before release.                    |
| **Release scope expands silently**                    | Pilot demand turns into broad production access without data, semantic, control or support evidence.             | Narrow release boundary and require expansion criteria.                    |
| **Release-critical issues are deferred to Phase 9**   | Phase 9 becomes a firefighting phase instead of run, adopt and improve.                                          | Fix blockers in Phase 8 or release only with explicit constraints.         |
| **Residual risks are noted but not accepted**         | Risk remains with the project team rather than accountable business, data, risk or product owners.               | Require named owner, rationale, condition and review trigger.              |
| **Support is assumed, not designed**                  | Users may have access but no clear route for incidents, wrong answers, access issues or confusion.               | Confirm runbooks, escalation, support capacity and early-life cadence.     |
| **Monitoring exists but is not actionable**           | Dashboards without owners, thresholds or response routes do not protect trust.                                   | Define alert owners, thresholds, incident route and pause criteria.        |
| **Cost is underestimated**                            | Model usage is only one part of cost; support, monitoring, logging, testing and improvement also consume budget. | Consolidate full run and change-cost view before approval.                 |
| **Ownership is fragmented**                           | Data, product, platform, support and risk teams each own a piece, but nobody owns the live outcome.              | Confirm accountable operating owner and decision rights.                   |
| **Documentation reflects the pilot, not the release** | Users and support teams misunderstand scope, limitations or changed behaviour.                                   | Refresh release notes, known limitations, onboarding and support material. |
| **The delivery team disappears too early**            | Critical fixes, regression checks and early-life support depend on people already reassigned.                    | Reserve capacity for hardening, release support and early defects.         |
| **Manual controls become permanent by accident**      | Manual reviews may work for a narrow release but collapse under volume or staff changes.                         | Time-bound manual controls and add automation conditions to roadmap.       |
| **Roadmap becomes a wish list**                       | Expansion is driven by demand rather than readiness, capacity and risk.                                          | Split roadmap into run, fix, improve and expand lanes.                     |

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
