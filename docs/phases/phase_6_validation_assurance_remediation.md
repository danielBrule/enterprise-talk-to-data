# Talk-to-Data Delivery Blueprint — Phase 6: Validation, Assurance & Remediation

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
- [3 Validation decision and delivery implications](#3-validation-decision-and-delivery-implications)
  - [3.1 Possible Phase 6 outcomes](#31-possible-phase-6-outcomes)
  - [3.2 Minimum conditions to proceed](#32-minimum-conditions-to-proceed)
  - [3.3 Common reasons to remediate, constrain, narrow or pause](#33-common-reasons-to-remediate-constrain-narrow-or-pause)
  - [3.4 How Phase 6 shapes later phases](#34-how-phase-6-shapes-later-phases)
- [4 Validation and assurance activities overview](#4-validation-and-assurance-activities-overview)
  - [4.1 Activity sequence](#41-activity-sequence)
  - [4.2 Activity logic](#42-activity-logic)
  - [4.3 Assurance-depth expectations](#43-assurance-depth-expectations)
  - [4.4 Practitioner note](#44-practitioner-note)
- [5 Core validation, assurance and remediation activities](#5-core-validation-assurance-and-remediation-activities)
  - [5.1 Reconfirm validation scope, stakeholders and assurance route](#51-reconfirm-validation-scope-stakeholders-and-assurance-route)
  - [5.2 Finalise evaluation set, protocol and acceptance thresholds](#52-finalise-evaluation-set-protocol-and-acceptance-thresholds)
  - [5.3 Validate identity, access and authorisation enforcement](#53-validate-identity-access-and-authorisation-enforcement)
  - [5.4 Validate sensitive-data, leakage and inference controls](#54-validate-sensitive-data-leakage-and-inference-controls)
  - [5.5 Validate SQL generation, query constraints and execution safety](#55-validate-sql-generation-query-constraints-and-execution-safety)
  - [5.6 Validate input data quality, answer quality, grounding and caveat handling](#56-validate-input-data-quality-answer-quality-grounding-and-caveat-handling)
  - [5.7 Validate safe failure, clarification and escalation behaviour](#57-validate-safe-failure-clarification-and-escalation-behaviour)
  - [5.8 Validate logging, auditability, documentation and repeatability](#58-validate-logging-auditability-documentation-and-repeatability)
  - [5.9 Validate performance, cost and operational limits](#59-validate-performance-cost-and-operational-limits)
  - [5.10 Classify failures, remediate blockers and approve pilot constraints](#510-classify-failures-remediate-blockers-and-approve-pilot-constraints)
- [6 Validation evidence decision pack](#6-validation-evidence-decision-pack)
  - [6.1 Validation evidence pack](#61-validation-evidence-pack)
  - [6.2 Evidence pack quality test](#62-evidence-pack-quality-test)
- [7 Exit criteria and handover](#7-exit-criteria-and-handover)
  - [7.1 Required exit outputs](#71-required-exit-outputs)
  - [7.2 Handover to Phase 7](#72-handover-to-phase-7)
  - [7.3 Exit decision wording](#73-exit-decision-wording)
  - [7.4 Practitioner note](#74-practitioner-note)
- [8 Key risks and failure modes](#8-key-risks-and-failure-modes)
  - [8.1 Practitioner note](#81-practitioner-note)

---

7

## 1 Executive summary

Phase 6 validates whether the bounded Talk-to-Data MVP is safe, reliable and evidenced enough for controlled pilot use.

This phase should not be the first time the system is tested. Most controls should already have been framed, designed, built and exercised during earlier phases: evaluation thinking in Phase 1, answerability and golden-question eligibility in Phase 2, governed foundation checks in Phase 3, orchestration evaluation design in Phase 4, and MVP test harnesses in Phase 5. Phase 6 is the formal assurance point where those controls are tested against the implemented system and the agreed requirements.

The purpose of Phase 6 is not to prove that the system is production-ready, nor to prove that every possible failure has been eliminated. No test set can provide full coverage of user behaviour, data variation, business ambiguity, model behaviour or future change. This is especially true for GenAI-enabled systems, where outputs can vary across prompts, context, model versions and edge cases. Phase 6 should therefore provide proportionate assurance: enough evidence to decide whether the MVP can be exposed to the intended pilot users, questions, data and workflows within an explicit risk boundary.

The depth of Phase 6 should reflect the use case. For a narrow internal POC using low-risk data and expert testers, validation may be a short evidence review, regression run and access check. For a decision-critical, sensitive, regulated or broad-user MVP, Phase 6 should be more formal: stronger evaluation sets, adversarial and edge-case testing, security and privacy review, audit evidence, remediation tracking, retesting and explicit residual-risk acceptance. The aim is not exhaustive proof; it is to expose material weaknesses, test beyond the happy path and decide whether the pilot boundary is safe and justified.

Phase 6 should control the remediation decision process. Issues found during validation should be classified by severity, source and pilot impact. Blocking issues should be fixed and retested before live pilot use. Material issues may lead to a constrained pilot boundary. Lower-risk issues may be accepted, deferred or carried into the Phase 7 pilot backlog. The phase should avoid creating confusion by “sending the project back” to earlier phases; instead, it should manage remediation through the relevant artefact owners while keeping the evidence, retesting and pilot-readiness decision in the Phase 6 control process.

Phase 7 preparation may run in parallel with Phase 6, especially user selection, onboarding material and feedback processes. Live user testing should not begin until issues that could expose restricted data, bypass permissions, produce materially misleading answers or prevent auditability have been fixed, constrained or explicitly accepted.

By the end of Phase 6, stakeholders should be able to decide whether to proceed to controlled pilot, proceed with constraints, remediate further, narrow scope or pause. The main output is a validation evidence pack covering evaluation results, access and security assurance, failure classification, remediation and retest evidence, residual-risk decisions and the approved Phase 7 pilot boundary.

## 2 Phase overview

Phase 6 validates, assures and, where appropriate, remediates the bounded T2D MVP before controlled pilot use. It tests whether the implemented system is safe and reliable enough for the intended exposure level: users, questions, data, access, answer quality, auditability, cost and operational control.

The phase should start from evidence already produced in earlier phases, not restart the project. Phase 6 consolidates that evidence, performs final validation against the implemented MVP, classifies issues, remediates blockers, retests material fixes and defines the safe boundary for Phase 7 pilot use.

It should not be treated as a guarantee of correctness. No validation set can cover every user question, data state, model output, business ambiguity or future change. The purpose is to provide proportionate assurance, make residual risk explicit and decide whether controlled pilot exposure is justified.

### 2.1 Objective

The objective of Phase 6 is to determine whether the bounded MVP is safe, reliable and evidenced enough to proceed to controlled pilot use.

It should confirm:

- **Validation scope:** users, questions, datasets, answer types, environments and pilot assumptions.

- **Assurance route:** required validation forum, approvers, risk owners, evidence standard and decision process.

- **Evaluation readiness:** evaluation set, test protocol, scoring approach and acceptance thresholds.

- **Access and exposure controls:** identity, authorisation, row/column restrictions, masking, sensitive-data controls and inference-risk controls.

- **Query and answer safety:** SQL validity, query constraints, cost limits, answer correctness, grounding, caveats and safe failure.

- **Remediation and residual risk:** which issues must be fixed before pilot, piloted with constraints, deferred or explicitly accepted.

- **Auditability, observability and repeatability:** whether questions, context, model calls, SQL, validation outcomes, answers, errors and feedback can be reconstructed, and whether key validation checks can be repeated reliably as the system moves towards production.

The output is a validation and remediation evidence pack supporting a clear decision: proceed to controlled pilot, proceed with constraints, remediate further, narrow scope or pause.

### 2.2 Scope of the phase

Phase 6 should remain bounded to the MVP scope and intended pilot boundary. In scope are final validation, assurance review, failure classification, targeted remediation, retesting, residual-risk decisioning and pilot-boundary approval.

Phase 6 should not become an open-ended rebuild. Structural gaps in data, semantics, architecture or implementation should be remediated through the relevant artefact owners while remaining controlled through the Phase 6 remediation process.

### 2.3 What this phase does not do

Phase 6 does not approve the system for production. It validates readiness for controlled pilot use. Production-readiness validation, go-live approval, resilience testing, final support model, monitoring thresholds, rollback route and release approval belong in Phase 8.

It also does not provide exhaustive proof that the system will always answer correctly. The purpose is proportionate assurance for the next exposure level, not absolute certainty.

### 2.4 Expected duration and level of effort

The effort required depends on risk, maturity and intended exposure.

For a narrow internal POC or expert-user MVP using low-risk data, Phase 6 may be a short evidence review, evaluation run, access check, logging review and approval of a constrained pilot.

For a higher-risk MVP, Phase 6 should be more formal, with stronger evaluation coverage, adversarial testing, access and leakage checks, audit evidence, remediation tracking, retesting and explicit residual-risk acceptance.

The phase should be measured by whether the evidence justifies the intended pilot exposure, not by the number of tests run. Where the MVP may progress towards production, validation should be automated as much as practical so that access checks, regression tests, query controls, answer-quality checks, cost checks and audit evidence can be repeated after changes to data, prompts, models, metadata, permissions or orchestration logic.

### 2.5 Main participants and decision owners

Phase 6 requires product, business, data, AI, security, evaluation and operating participation. It should not be run as a purely technical test phase because the key decisions concern user exposure, residual risk, business trust and pilot readiness.

At minimum, named owners should cover pilot scope, business usefulness, data and semantic correctness, orchestration behaviour, access and leakage risk, evaluation scoring, remediation, supportability and pilot operation.

Every blocking or material issue should have an owner, severity, remediation decision, retest route and implication for the Phase 7 pilot boundary.

## 3 Validation decision and delivery implications

Phase 6 should end with a clear decision on whether the MVP is safe enough for controlled pilot use. The decision should be based on validation evidence, remediation status, documentation quality, residual risk and the proposed Phase 7 pilot boundary.

A proceed decision does not mean the system is production-ready. It means the MVP has enough evidence, controls and documentation to be exposed to the agreed pilot users, questions, data and workflows. Production readiness remains a later decision in Phase 8.

The decision should not be a generic pass/fail judgement. A T2D MVP may be suitable for a narrow expert-user pilot while still being unsuitable for broad business release. Phase 6 should therefore define the conditions of use: who can use the system, which questions are supported, which data is accessible, what caveats must be shown, which issues remain open, what documentation is available and what monitoring is required during pilot.

### 3.1 Possible Phase 6 outcomes

| Outcome                  | Meaning                                                               | Typical trigger                                                                                                                                    |
|--------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Proceed to pilot         | The MVP is validated enough for the agreed Phase 7 pilot boundary.    | Critical controls pass, answer quality is acceptable for scope, audit evidence is sufficient and no blocking issue remains.                        |
| Proceed with constraints | Pilot can start, but only within tighter limits.                      | Some issues remain, but they can be controlled through restricted users, questions, data, answer types, documentation, monitoring or human review. |
| Remediate before pilot   | Blocking issues must be fixed and retested before live user exposure. | Access, leakage, query safety, answer quality, logging, documentation or safe-failure issues create unacceptable pilot risk.                       |
| Narrow scope             | The pilot boundary must be reduced before proceeding.                 | Part of the MVP is valid, but some domains, questions, users or answer types are not safe or reliable enough.                                      |
| Pause                    | Pilot should not start until material uncertainty is resolved.        | Evidence is too weak, residual risk is not accepted, ownership is unclear or the system cannot be made safe within the current scope.              |

### 3.2 Minimum conditions to proceed

Phase 6 should proceed to controlled pilot only when the team can answer yes to the following confidence tests:

- **Pilot boundary is explicit:** users, questions, datasets, answer types, caveats and exclusions are clear.

- **Evaluation evidence is sufficient:** the MVP has been tested against agreed golden questions, edge cases, failure cases and acceptance thresholds.

- **Access and exposure controls work:** identity, authorisation, masking, sensitive-data controls, inference controls and prompt-injection protections behave as intended.

- **Queries are bounded:** generated queries use approved sources, joins, filters, limits and validation checks before execution.

- **Answers are grounded and caveated:** outputs use approved evidence, avoid unsupported explanations and surface relevant assumptions, caveats and limitations.

- **Safe failure works:** the system clarifies, refuses, escalates or constrains answers when requests are ambiguous, unsafe or outside scope.

- **Audit and documentation are usable:** questions, context, model calls, SQL, validation outcomes, answers, errors and feedback can be reconstructed, and pilot users / operators have enough documentation to use and support the MVP safely.

- **Residual risk is controlled:** blockers are resolved or retested, remaining issues have named owners, and any constraints are reflected in the Phase 7 pilot plan.

- **Formal approval route is complete:** the required validation document, evidence pack, committee submission or sign-off record has been reviewed by the appropriate decision owners for the intended pilot exposure.

### 3.3 Common reasons to remediate, constrain, narrow or pause

The team should avoid starting live pilot use where any of the following conditions apply without a clear mitigation:

- **Unclear pilot boundary:** users, questions, data, answer types or caveats are not defined tightly enough.

- **Weak evaluation evidence:** the test set is too narrow, too easy or not representative of expected pilot use.

- **Access or leakage risk remains:** permissions, masking, restricted data, small cohorts, logs or metadata exposure cannot be trusted.

- **Query validation is incomplete:** unsupported tables, joins, filters, large scans or unsafe SQL patterns are not reliably blocked.

- **Answers overclaim:** the system adds unsupported explanations, causal claims, recommendations or confidence beyond the evidence.

- **Safe failure is weak:** the system guesses when it should clarify, refuse, escalate or state a limitation.

- **Audit or documentation is insufficient:** the team cannot reconstruct how answers were produced, or users and operators do not understand the approved use, limitations and escalation route.

- **Ownership is unclear:** issues, residual risks, user support, monitoring and remediation do not have named owners.

### 3.4 How Phase 6 shapes later phases

Phase 6 defines the safe starting conditions for Phase 7. It should not only state whether pilot testing can begin; it should define how pilot testing must be run.  
For Phase 7, it should provide the approved pilot boundary, user groups, supported questions, known limitations, user guidance, feedback process, monitoring needs, residual risks and open issue backlog.

## 4 Validation and assurance activities overview

Phase 6 is organised around ten activities. They provide a structured way to validate the MVP, classify issues, remediate blockers and approve the controlled Phase 7 pilot boundary.

The activities should not be treated as a rigid waterfall. Some can run in parallel, especially evidence review, access testing, evaluation runs, documentation review and pilot preparation. The sequencing matters mainly for decision control: the team should not expose pilot users to the MVP until blocking risks have been fixed, constrained or formally accepted.

The depth of each activity should reflect the risk of the use case. A narrow internal MVP may require a short validation cycle. A sensitive, regulated, broad-user or decision-critical MVP requires stronger evidence, more formal approval and more repeatable testing.

### 4.1 Activity sequence

| Activity                                                                       | Main question                                                                                | Main output                                                                                     |
|--------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| 1\. Reconfirm validation scope, stakeholders and assurance route               | What exactly is being validated, who approves it, and what evidence is required?             | Confirmed validation scope, approvers, risk owners and decision route.                          |
| 2\. Finalise evaluation set, protocol and acceptance thresholds                | Is the evaluation set fit for the pilot decision?                                            | Final evaluation set, scoring approach and acceptance thresholds.                               |
| 3\. Validate identity, access and authorisation enforcement                    | Does the MVP enforce the right user permissions at runtime?                                  | Access validation results and unresolved access issues.                                         |
| 4\. Validate sensitive-data, leakage and inference controls                    | Can the system expose restricted data directly or indirectly?                                | Leakage, masking, prompt-injection and inference-risk findings.                                 |
| 5\. Validate SQL generation, query constraints and execution safety            | Are queries valid, bounded, authorised and safe to execute?                                  | SQL validation, execution safety and query-cost findings.                                       |
| 6\. Validate input data quality, answer quality, grounding and caveat handling | Are the queried inputs fit for use, and are answers correct, grounded and properly caveated? | Data-quality findings, answer-quality results and issue examples.                               |
| 7\. Validate safe failure, clarification and escalation behaviour              | Does the system fail safely when it cannot answer?                                           | Refusal, clarification and escalation test results.                                             |
| 8\. Validate logging, auditability, documentation and repeatability            | Can answers be reconstructed, explained and supported?                                       | Audit/logging review, documentation review and repeatability gaps.                              |
| 9\. Validate performance, cost and operational limits                          | Is the MVP viable for controlled pilot use?                                                  | Latency, cost, usage-limit and supportability findings.                                         |
| 10\. Classify failures, remediate blockers and approve pilot constraints       | What must be fixed, constrained, accepted or deferred before Phase 7?                        | Failure taxonomy, remediation log, retest evidence, approval record and approved pilot boundary |

### 4.2 Activity logic

The activities follow a simple assurance logic:

1.  **Confirm the decision route** before running tests, so the team knows who can approve, constrain or block pilot use.

2.  **Finalise the evidence standard** before scoring the MVP, so validation is not adjusted after seeing the results.

3.  **Validate hard controls first**, especially access, leakage, query boundaries and execution safety.

4.  **Validate answer behaviour next**, including input quality, correctness, grounding, caveats, safe failure and user-facing documentation.

5.  **Validate operability last**, including logs, traceability, performance, cost, repeatability, support and pilot monitoring.

6.  **Close with a decision**, not just a defect list: remediate blockers, constrain the pilot, accept residual risk or pause.

This logic is more important than the exact order. In practice, evaluation, security testing, documentation review and remediation may run in parallel. What matters is that the final pilot decision is evidence-based and that material changes are retested before exposure.

### 4.3 Assurance-depth expectations

The expected output should match the use case, risk and organisational maturity.

| Output level   | When appropriate                                                           | Expected evidence                                                                                                                                  |
|----------------|----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Lightweight    | Low-risk internal POC, expert testers, non-sensitive data.                 | Short evidence review, core test results, known limitations and constrained pilot decision.                                                        |
| Standard MVP   | Controlled business pilot, limited users, governed data.                   | Evaluation results, access/security checks, issue log, remediation evidence, user guidance and pilot boundary.                                     |
| High-assurance | Sensitive data, regulated context, broad users, decision-critical outputs. | Formal validation pack, stronger test coverage, adversarial tests, approval record, retest evidence, residual-risk acceptance and monitoring plan. |

### 4.4 Practitioner note

The hard part of Phase 6 is not only finding defects. It is deciding what level of evidence is enough for the next exposure level.

Legal, security and compliance stakeholders may push for stronger controls and lower risk. Product, business and operations stakeholders may push for speed, usability and learning. Phase 6 should make that tension explicit rather than hide it behind a generic pass/fail decision.

The practical discipline is to separate blockers from constraints. Issues that could expose restricted data, bypass permissions, produce materially misleading answers or prevent auditability should be fixed before live use. Other issues may be acceptable if the pilot scope is narrowed, users are briefed, outputs are caveated, monitoring is active and ownership is clear.

## 5 Core validation, assurance and remediation activities

### 5.1 Reconfirm validation scope, stakeholders and assurance route

**Purpose:** Confirm what is being validated, who can approve pilot exposure and what evidence is required for the Phase 6 decision.

**Core activities**

- Reconfirm the MVP boundary: users, datasets, metadata sources, tools, model components, supported questions, answer types, environments and exclusions.

- Compare the implemented MVP with the original scope from earlier phases and record material changes.

- Confirm the intended Phase 7 pilot boundary, including tester population, business use, data exposure, decision impact and monitoring expectations.

- Update the required assurance route: product approval, security review, data-governance review, legal/privacy review, architecture review, model-risk review, change approval or validation committee.

- Confirm approvers, risk owners and decision rights for proceed, proceed with constraints, remediate, narrow or pause.

- Confirm the expected validation document, evidence pack or committee submission required for sign-off.

- Align stakeholders on what T2D / GenAI validation can and cannot prove, including partial test coverage, probabilistic behaviour and residual risk

**Output**

- Phase 6 validation boundary showing what is included, excluded and changed since earlier phases.

- Pilot exposure statement covering users, use, data, decision impact and constraints.

- Assurance route showing approvers, risk owners, decision forum and required evidence.

- Validation document / evidence-pack requirements.

- Open ownership, sign-off or assurance blockers.

**Red flags**

- Pilot users, data scope or intended use have changed but validation scope has not.

- No one can clearly say who approves residual risk.

- Security / legal / governance / operating stakeholders appear for the first time in Phase 6.

- The team is running tests before knowing what evidence the approvers need.

- Stakeholders want assurance but avoid explicit ownership.

- Stakeholders expect validation to prove “zero risk” or full coverage.

**Practitioner note**  
This activity is not only procedural. It mixes legal requirements, governance expectations and organisational politics. In some organisations, T2D or GenAI validation will be new, and stakeholders may need education before they can make a responsible decision. The team should explain what validation can prove, what it cannot prove, and which residual risks remain. It should also make ownership explicit. A validation process where everyone reviews the evidence but no one accepts the risk is not a decision process.

### 5.2 Finalise evaluation set, protocol and acceptance thresholds

**Purpose:** Confirm that the evaluation set, scoring method and acceptance thresholds are fit to support the Phase 6 pilot-readiness decision.

**Core activities**

- Consolidate candidate golden questions, expected answers and failure cases identified during earlier phases.

- Confirm that the evaluation set covers the intended pilot scope: supported users, questions, metrics, dimensions, filters, caveats and access rules.

- Add edge cases, ambiguous questions, unsupported requests, unsafe requests, prompt-injection attempts and repeated follow-up scenarios.

- Define how each test will be scored, distinguishing pass/fail control checks from judgement-based answer-quality reviews.

- Confirm acceptance thresholds by risk area, including answer correctness, query validity, retrieval quality, safe failure, access control, leakage and auditability.

- Confirm who reviews disputed cases and how judgement-based findings will be resolved.

- Freeze the evaluation protocol before the main validation run, so the standard is not adjusted after seeing results.

**Output**

- Frozen Phase 6 evaluation set mapped to pilot scope and risk areas.

- Expected-answer evidence linked to trusted sources, SQL, reports or approved examples.

- Scoring protocol separating pass/fail controls from judgement-based quality checks.

- Acceptance thresholds by risk area.

- Disputed-case review route and retest rules.

**Red flags**

- The test set is dominated by easy happy-path questions.

- Expected answers are not linked to trusted evidence.

- Hard controls and answer-quality judgement are scored the same way.

- The evaluation standard changes after results are known.

- Unsafe, ambiguous or out-of-scope cases are missing.

**Practitioner note**  
Not all validation checks should be scored the same way. Rule-based controls should usually be assessed as pass/fail: users must not access unauthorised data, destructive queries must be blocked, restricted fields must not be exposed, and required logs must be created. These are not matters of style.

Other outputs require judgement-based scoring. The exact wording of an answer, the clarity of a caveat, the usefulness of a clarification question or the quality of an explanation may be acceptable even when not identical to an expected answer. The evaluation protocol should separate hard control failures from quality judgement. Otherwise, the team may either over-tolerate serious control failures or over-police harmless wording differences.

### 5.3 Validate identity, access and authorisation enforcement

**Purpose:** Confirm that the MVP enforces the right user identity, permissions and access boundaries at runtime.

**Core activities**

- Confirm how user identity is passed through the application, orchestration layer, query engine and logs.

- Confirm that pilot users have the correct access for the intended pilot scope, neither broader nor narrower than required.

- Test role, row and column restrictions using realistic pilot user profiles.

- Validate that generated SQL cannot bypass access controls through alternate tables, joins, views, cached outputs or metadata.

- Access-change handling evidence covering joiner, leaver, role-change and revocation scenarios, including expected and observed timing.

**Output**

- Access scenario results covering allowed, denied and constrained user journeys.

- Access exception log showing excessive, insufficient or untested access.

- Evidence that unauthorised requests are blocked before data exposure.

- Pilot constraints or remediation actions for unresolved access gaps.

**Red flags**

- Access changes are tested only as final states, without checking timing, stale permissions or transition behaviour.

- Pilot users have broader access than needed, increasing avoidable exposure.

- Pilot users have too little access, creating false failures that look like model or data-quality issues.

- Access rules work in direct SQL but can be bypassed through generated joins, alternate views, cached outputs, metadata or logs.

**Practitioner note**  
Access validation is a hard control, not a quality preference. A slightly awkward answer may be acceptable in a pilot; unauthorised data exposure is not. The team should validate both sides of access: users must not see data they are not allowed to see, but they must also have enough access to test the intended workflow. Access is not static during pilot; joiners, leavers, role changes and revocation should be owned, traceable and retested where material.

### 5.4 Validate sensitive-data, leakage and inference controls

**Purpose:** Confirm that the MVP does not expose restricted data directly, indirectly or through repeated interaction.

**Core activities**

- Confirm which data, columns, metrics, metadata and outputs are sensitive or restricted for the pilot scope.

- Test whether PII, restricted fields, commercially sensitive values and small cohorts are masked, blocked or refused as intended.

- Validate that prompt-injection or policy-bypass attempts cannot reveal hidden instructions, restricted metadata, SQL context or unauthorised data.

- Test inference risk through repeated filtering, drill-downs, small groups, comparisons, follow-up questions or combinations of individually allowed questions.

- Confirm that logs, traces, feedback records and exported outputs do not retain or display restricted information unnecessarily.

**Output**

- Sensitive-data validation findings covering direct exposure, metadata exposure, logs and generated answers.

- Leakage and inference issue log, with severity, owner and pilot impact.

- Evidence that restricted requests are blocked, masked, constrained or refused before exposure.

- Pilot constraints or remediation actions for unresolved exposure risks.

**Red flags**

- The system blocks restricted columns in SQL but still exposes them through answer text, metadata, logs or previous context.

- Aggregated answers allow users to infer restricted values through small cohorts, comparisons or repeated follow-up questions.

- Prompt-injection tests are treated as “security edge cases” rather than expected validation cases for a GenAI interface.

- Sensitive information is excluded from the answer but retained in traces, feedback exports or debugging views.

**Practitioner note**  
Sensitive-data validation should look beyond obvious PII. In T2D, leakage can happen through metadata, generated SQL, aggregates, cached context, logs, explanations and repeated questions. A user may not access restricted data directly, but may still infer it by asking several permitted questions, combining filters, narrowing cohorts or comparing totals. This is especially difficult to test manually because each question may look harmless in isolation. GenAI can help by generating adversarial question sequences and inference scenarios, but those tests should still be reviewed against business rules, access policy and real data sensitivity.

### 5.5 Validate SQL generation, query constraints and execution safety

**Purpose:** Confirm that generated queries are valid, bounded, authorised and safe to execute against the approved data layer.

**Core activities**

- Validate that generated SQL only uses approved tables, views, metrics, dimensions, joins, filters and aggregation rules.

- Confirm that unsafe commands, write operations, unrestricted exports, SELECT \*, unbounded scans and unsupported query patterns are blocked before execution.

- Test whether query limits, row limits, timeout rules, dry-run checks and cost thresholds behave as intended.

- Check that generated queries apply required security, date, cohort, caveat and standard exclusion rules.

- Validate that failed, invalid or high-risk queries are refused, repaired safely, routed for review or logged for remediation.

**Output**

- Query validation evidence covering supported, unsupported, unsafe and high-cost query scenarios.

- Query exception log showing blocked, repaired, constrained and failed queries.

- Evidence that mandatory filters, joins, limits and access constraints are applied before execution.

- Remediation actions or pilot constraints for unresolved query-safety gaps.

**Red flags**

- SQL validation focuses on syntax but not business logic, joins, grain, filters or access constraints.

- The model can generate queries against technically available assets that are not approved for pilot use.

- Expensive or broad queries are only discovered after execution, not blocked before execution.

- Failed SQL is automatically repaired in a way that changes the business meaning of the answer.

**Practitioner note**  
Query safety should be hard-tested with mostly boolean pass/fail checks. A generated query either uses approved assets, applies mandatory filters, respects permissions and stays within limits, or it does not. The team should deliberately test blocked commands, unsupported tables, unsafe joins, missing filters, excessive scans, small cohorts and access-bypass attempts. For pilot use, the default should be simple: if the query cannot be validated against approved assets, joins, filters, limits and permissions, it should not run.

### 5.6 Validate input data quality, answer quality, grounding and caveat handling

**Purpose:** Confirm that the data used is fit for the answer, and that generated answers are correct, grounded, caveated and not overstated.

**Core activities**

- Validate that answers use the approved data assets, metrics, dimensions, filters, caveats and expected-answer sources.

- Check key data-quality signals before judging the answer, including freshness, completeness, reconciliation, nulls, missing dimensions and known limitations.

- Compare generated answers against trusted SQL, reports, dashboards, metric cards or approved examples.

- Review whether answers preserve assumptions, caveats, uncertainty and scope limitations in language users can understand.

- Test that the system does not add unsupported explanations, causal claims, recommendations or confidence beyond the evidence.

**Output**

- Answer-quality findings linked to trusted expected-answer evidence.

- Data-quality exception log showing freshness, completeness, reconciliation or coverage issues affecting answers.

- Examples of correct, partial, misleading and overclaimed answers.

- Pilot constraints or remediation actions for unresolved data or answer-quality risks.

**Red flags**

- Answer evaluation starts with the wording, before checking whether the underlying data is fresh, complete and reconciled enough.

- The answer is numerically correct but hides a caveat that would change how a user should interpret it.

- The model explains a variance or recommends an action without evidence from the query result or approved context.

- Data-quality issues are treated as model failures, or model failures are blamed on data quality without evidence.

**Practitioner note**  
GenAI can help evaluate answers, especially by flagging missing caveats, overclaiming, unsupported explanations, weak wording or inconsistencies with the provided evidence. This can speed up review and help generate additional edge cases. However, it should not be the sole judge of answer correctness or safety. Numeric correctness, access controls, mandatory caveats and policy boundaries should be checked against trusted sources, deterministic rules or human review where required

### 5.7 Validate safe failure, clarification and escalation behaviour

**Purpose:** Confirm that refusal, clarification, constraint and escalation behaviours are consistent, understandable and usable for pilot users.

**Core activities**

- Review failure cases from access, leakage, SQL and answer-quality validation.

- Check whether the system’s response is understandable, not just technically safe.

- Confirm when the MVP should clarify, refuse, constrain or escalate.

- Validate that failure messages do not expose sensitive policy, metadata or system context.

- Confirm the escalation route, owner and user message for cases needing human review.

**Output**

- Safe-failure evidence showing when the MVP answered, clarified, refused, constrained or escalated.

- Examples of acceptable and unacceptable clarification / refusal behaviour.

- Escalation route for questions that require human review or analyst support.

- Pilot constraints or remediation actions for unsafe failure patterns.

**Red flags**

- The MVP guesses when the question is ambiguous because answering looks more helpful than clarifying.

- Refusals are safe but unusable, leaving users unclear on what they can ask instead.

- Similar unsupported questions produce inconsistent refusal or escalation behaviour.

- Follow-up questions inherit too much context and drift outside the approved pilot scope.

- Escalation exists in principle but no one owns the response path, timing or user message.

**Practitioner note**  
Safe failure is part of answer quality. A T2D system should not be rewarded for answering every question. It should be rewarded for knowing when to answer, when to ask for clarification, when to refuse and when to escalate. In pilot, this also protects trust: users are more likely to accept a limitation they understand than a confident answer that later proves wrong.

### 5.8 Validate logging, auditability, documentation and repeatability

**Purpose:** Confirm that pilot interactions can be reconstructed, explained, supported and retested.

**Core activities**

- Validate that questions, user identity, retrieved context, model calls, generated SQL, validation outcomes, answers, errors and feedback are logged at the right level.

- Confirm that logs and traces are usable for audit, debugging, issue investigation and remediation without exposing unnecessary sensitive data.

- Review whether pilot users and operators have enough documentation to understand approved use, limitations, caveats, escalation and support routes.

- Confirm that key validation checks can be repeated after changes to prompts, models, metadata, permissions, data assets or orchestration logic.

- Check that log retention, access to traces and documentation ownership are clear for the pilot period.

**Output**

- Traceability sample showing how a representative answer can be reconstructed end to end.

- Audit and logging gap log covering missing, excessive or sensitive trace capture.

- Pilot documentation pack covering user guidance, limitations, support and escalation.

- Repeatability plan for rerunning key validation checks after material changes.

**Red flags**

- The team can see the final answer but cannot reconstruct which data, SQL, model call or validation decision produced it.

- Logs capture sensitive prompts, SQL, raw results or user data that should not be retained or broadly visible.

- Documentation describes how the MVP works technically but not how users should use it safely.

- Validation depends on manual checks that cannot be repeated quickly after a prompt, model, data or permission change.

- Issue investigation relies on individual engineers’ memory rather than traceable evidence.

**Practitioner note**  
Auditability is not only about storing logs. Logs must be usable. Where appropriate, events should be tagged consistently with level, event type, tool, timestamp, user/session reference, execution ID, model version, prompt version, validation result, query ID, error type and environment.

Log retention should also be explicit: long enough to support pilot review, audit, debugging and improvement, but not longer or broader than privacy, security and policy allow.

### 5.9 Validate performance, cost and operational limits

**Purpose:** Confirm that the MVP can run within acceptable latency, cost, usage and support limits during controlled pilot use.

**Core activities**

- Test response time across representative questions, follow-ups, refusals and high-complexity cases.

- Validate query, model, retrieval, logging and infrastructure cost against expected pilot usage.

- Confirm usage limits, concurrency assumptions, timeouts, retry behaviour and stop conditions for expensive or slow interactions.

- Check whether operational monitoring can detect failures, latency spikes, cost spikes and repeated user issues.

- Confirm the pilot support route, including incident triage, escalation, ownership and suspension criteria.

**Output**

- Performance and cost profile for representative pilot interactions.

- Operational limit register covering latency, cost, concurrency, retries, timeouts and stop conditions.

- Monitoring and alerting gaps that could affect pilot control.

- Pilot support and escalation constraints for unresolved operational risks.

**Red flags**

- Pilot cost estimates only include model calls and ignore warehouse queries, retries, logging, traces and evaluation runs.

- Slow or expensive interactions are discovered only after execution, rather than constrained before or during runtime.

- The MVP works for single-user demos but has not been tested against realistic pilot concurrency or repeated follow-ups.

- Operational alerts exist, but no one owns the response path, threshold review or pilot suspension decision.

**  
**

### 5.10 Classify failures, remediate blockers and approve pilot constraints

**Purpose:** Turn validation findings into a clear remediation decision, residual-risk position and approved Phase 7 pilot boundary.

**Core activities**

- Classify validation findings by failure type, severity, owner and pilot impact.

- Separate blockers from issues that can be constrained, accepted, deferred or monitored during pilot.

- Decide whether blocking issues can be remediated within the pilot timeline and risk appetite; fix and retest where viable, or narrow, pause or stop where they cannot.

- Confirm pilot constraints: users, questions, data, answer types, caveats, monitoring, escalation and support route.

- Prepare the decision record for proceed, proceed with constraints, remediate further, narrow scope or pause.

**Output**

- Failure taxonomy showing issue type, severity, root cause and pilot impact.

- Remediation and retest log for blocking and material issues.

- Residual-risk record showing accepted risks, owners, rationale and controls.

- Approved Phase 7 pilot boundary and decision record.

**Red flags**

- The team treats all defects equally instead of separating blockers from pilot constraints.

- Issues are fixed without retesting, creating false confidence before user exposure.

- Residual risks are documented but no named owner accepts them.

- The pilot scope is approved verbally, but constraints are not reflected in user access, documentation, monitoring or support.

**Practitioner note**  
If earlier phases have been done properly, Phase 6 should not discover fundamental gaps for the first time. It may still find defects, edge cases and control weaknesses, but these should usually be bounded enough to fix, constrain or defer. If Phase 6 exposes unresolved metric ownership, unsafe access design, missing auditability or a fundamentally unreliable MVP, the right decision may be to narrow, pause or stop rather than force remediation into the pilot timeline.

## 6 Validation evidence decision pack

Phase 6 should produce a clear evidence base for the pilot-readiness decision. The outputs should not be a loose collection of test results. They should show what was validated, what failed, what was fixed, what remains constrained and who accepts the residual risk.

Where the MVP may progress beyond a short POC, the evidence pack should also identify which validation checks have been automated, which remain manual and which must be automated before pilot expansion or production readiness

The level of detail should match the use case. A low-risk internal MVP may need a lightweight validation pack. A sensitive, regulated or decision-critical MVP may require a formal validation document, committee submission or approval record.

### 6.1 Validation evidence pack

The main output is a validation and remediation evidence pack. It should contain enough evidence for decision owners to approve, constrain, pause or reject controlled pilot use.

The pack should include:

- **Validation scope:** MVP version, pilot users, supported questions, data assets, tools, model components, environments, exclusions and known limitations.

- **Assurance route:** approvers, risk owners, review forums, evidence standard and sign-off requirements.

- **Evaluation results:** golden-question results, edge cases, unsafe cases, access tests, leakage tests, safe-failure cases and acceptance thresholds.

- **Control validation:** access enforcement, sensitive-data controls, SQL safety, query limits, answer grounding, caveats, auditability, documentation and repeatability.

- **Failure taxonomy:** issue type, severity, root cause, owner and pilot impact.

- **Remediation and retest evidence:** fixes applied, constraints added, retest results and remaining open issues.

- **Residual-risk record:** risks accepted for pilot, rationale, owner, constraints and monitoring route.

- **Pilot boundary:** approved users, questions, data, answer types, caveats, usage limits, escalation route and pause conditions.

- **Automation and repeatability:** automated checks, manual checks, rerun triggers, regression coverage and gaps that must be automated before pilot expansion or production readiness.

### 6.2 Evidence pack quality test

Before Phase 6 closes, the outputs should pass a simple quality test:

- **Decision-ready:** the evidence supports a clear proceed, proceed with constraints, remediate, narrow, pause or stop decision.

- **Bounded:** the approved pilot boundary is explicit and reflected in access, documentation, monitoring and support.

- **Traceable:** material findings link back to tests, logs, traces, examples or reviewer decisions.

- **Owned:** blocking issues, residual risks, pilot constraints and support routes have named owners.

- **Retested:** material fixes have been retested, or the pilot scope has been constrained accordingly.

- **Usable:** pilot users and operators have enough guidance to understand supported use, caveats, refusals, escalation and feedback.

- **Proportionate:** the evidence standard is appropriate for the use case, data sensitivity, user group and business impact.

- **Repeatable:** key checks can be rerun after changes to prompts, models, metadata, permissions, data assets or orchestration logic.

If these conditions are not met, the phase should not close with a vague approval. The team should either remediate further, narrow the pilot boundary or pause until the decision can be made responsibly.

## 7 Exit criteria and handover

Phase 6 should close with a clear pilot-readiness decision. The phase is complete only when the validation evidence, remediation status, residual risk, backlog and pilot boundary are clear enough for the relevant decision owners to approve, constrain, pause or reject Phase 7 user testing.

A positive Phase 6 decision does not mean the system is production-ready. It means the MVP is sufficiently validated for the agreed pilot exposure, under the documented constraints and monitoring conditions.

### 7.1 Required exit outputs

The required exit output is the validation evidence decision pack described in Section 6, completed to the standard required for the intended pilot exposure.

The exit decision should confirm whether the MVP can proceed to pilot, proceed with constraints, remediate further, narrow scope, pause or stop. It should also identify the approved pilot boundary, residual risks, issue disposition, backlog, repeatability gaps and ownership route.

### 7.2 Handover to Phase 7

The handover to Phase 7 should make clear how controlled user testing must be run. It should not simply pass the MVP to users.

Phase 7 should receive:

- Approved pilot users and access groups.

- Supported and excluded question types.

- Known limitations, caveats and required user guidance.

- Monitoring signals, review cadence and escalation route.

- Issues fixed during Phase 6 and evidence of retest.

- Issues accepted for pilot with named owners and review points.

- Backlog items to address during pilot, before production readiness or in later releases.

- Feedback capture process and issue triage route.

- Conditions that would trigger pilot narrowing, suspension or rollback.

If the project moves forward, the backlog should become an active management artefact, not an archive. Phase 7 should use it to prioritise pilot fixes, interpret user feedback and decide what must be resolved before any Phase 8 production-readiness review.

### 7.3 Exit decision wording

The Phase 6 decision should be explicit. Suggested wording:

| Decision                 | Suggested wording                                                                                           |
|--------------------------|-------------------------------------------------------------------------------------------------------------|
| Proceed to pilot         | The MVP is approved for controlled Phase 7 pilot use within the documented boundary.                        |
| Proceed with constraints | The MVP may enter pilot only under the stated constraints, monitoring and residual-risk acceptance.         |
| Remediate further        | Pilot use should not begin until the listed blocking or material issues are fixed and retested.             |
| Narrow scope             | Pilot may proceed only with a reduced user, data, question or answer-type boundary.                         |
| Pause                    | Pilot should not begin until material uncertainty, ownership or assurance gaps are resolved.                |
| Stop                     | The MVP should not proceed to pilot because the risk, evidence gap or remediation burden is not acceptable. |

### 7.4 Practitioner note

A weak Phase 6 ends with “approved, subject to fixes”. A strong Phase 6 states what was fixed, what was constrained, what was accepted, what was moved to backlog, who owns each item and when it must be reviewed.

The handover should be operational, not symbolic. If pilot users, access groups, caveats, documentation, monitoring, support, backlog ownership and pause conditions are not ready, the system is not ready for controlled pilot use

## 8 Key risks and failure modes

Phase 6 can fail even when many tests have been run. The main risk is not only that defects remain. It is that validation creates false confidence, ownership is unclear, or the pilot starts with constraints that are documented but not operationally enforced.

| Risk / failure mode                               | Why it matters                                                                                                            | Likely response                                                                                                                                                    |
|---------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validation becomes a checklist exercise           | The MVP may pass a set of tests without being safe or useful for the intended pilot boundary.                             | Re-anchor validation to pilot users, data, question scope, residual risk and decision ownership.                                                                   |
| Evidence standards change after results are known | The team may lower the bar to justify moving forward.                                                                     | Freeze the evaluation protocol, scoring approach and acceptance thresholds before the formal validation run.                                                       |
| Happy-path testing dominates                      | The MVP may look reliable while failing on ambiguity, unsafe requests, access boundaries, caveats or follow-up questions. | Include edge cases, failure cases, adversarial prompts, unsupported questions and repeated interaction scenarios.                                                  |
| Safe failure is treated as failure                | The system may be pushed to answer when clarification, refusal or escalation would be safer.                              | Treat safe failure as a valid positive outcome where the question is ambiguous, unsafe, unsupported or outside scope.                                              |
| Remediation backlog becomes a dumping ground      | Issues may be deferred without ownership, priority or review trigger.                                                     | Split issues into fixed before pilot, constrained for pilot, accepted residual risk, Phase 7 backlog, Phase 8 production-readiness backlog and future-scope items. |
| Residual risk has no owner                        | Everyone may review the evidence, but no one accepts accountability for the pilot decision.                               | Require named ownership for accepted risks, pilot constraints, monitoring and escalation.                                                                          |
| Pilot boundary is not enforced operationally      | Constraints may exist in documentation but not in access, UI, logging, monitoring or support.                             | Reflect pilot constraints in permissions, user guidance, answer behaviour, alerts, support process and pause conditions.                                           |
| Automation is postponed too long                  | Validation becomes slow, manual and unreliable after changes to prompts, models, data, metadata or permissions.           | Identify checks that must become repeatable before pilot expansion or production readiness.                                                                        |

### 8.1 Practitioner note

A strong Phase 6 does not try to prove that the system is risk-free. It makes the risk visible, bounded and owned. The worst outcome is not finding issues before pilot. The worst outcome is finding issues and still proceeding with unclear constraints, weak ownership or no way to retest the system after change.

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
