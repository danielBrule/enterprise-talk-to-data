# Talk-to-Data Delivery Blueprint — Phase 8 Annexes: Production Readiness & Controlled Release

*Daniel Brule · Talk-to-Data Delivery Blueprint · v1.0 · June 2026*

---

**Table of contents**

- [1 How to use this annex](#1-how-to-use-this-annex)
- [2 Activity 1: Confirm production scope and release boundary](#2-activity-1-confirm-production-scope-and-release-boundary)
  - [2.1 Production release boundary template](#21-production-release-boundary-template)
  - [2.2 Boundary-to-evidence mapping](#22-boundary-to-evidence-mapping)
  - [2.3 Suggested release boundary statuses](#23-suggested-release-boundary-statuses)
  - [2.4 Illustrative example: controlled production boundary](#24-illustrative-example-controlled-production-boundary)
  - [2.5 Scope challenge questions](#25-scope-challenge-questions)
  - [2.6 Common boundary mistakes](#26-common-boundary-mistakes)
  - [2.7 Evidence to retain](#27-evidence-to-retain)
- [3 Activity 2: Triage pilot findings and production-readiness backlog](#3-activity-2-triage-pilot-findings-and-production-readiness-backlog)
  - [3.1 Production-readiness issue disposition register](#31-production-readiness-issue-disposition-register)
  - [3.2 Issue disposition guide](#32-issue-disposition-guide)
  - [3.3 Priority assessment matrix](#33-priority-assessment-matrix)
  - [3.4 Illustrative examples](#34-illustrative-examples)
  - [3.5 Pre-release hardening backlog template](#35-pre-release-hardening-backlog-template)
  - [3.6 Release constraint log](#36-release-constraint-log)
  - [3.7 Residual-risk candidate template](#37-residual-risk-candidate-template)
  - [3.8 Triage meeting agenda](#38-triage-meeting-agenda)
  - [3.9 Common triage mistakes](#39-common-triage-mistakes)
  - [3.10 Evidence to retain](#310-evidence-to-retain)
- [4 Activity 3: Complete pre-release hardening and regression checks](#4-activity-3-complete-pre-release-hardening-and-regression-checks)
  - [4.1 Pre-release hardening backlog template](#41-pre-release-hardening-backlog-template)
  - [4.2 Fix classification guide](#42-fix-classification-guide)
  - [4.3 Regression check template](#43-regression-check-template)
  - [4.4 Suggested non-regression coverage](#44-suggested-non-regression-coverage)
  - [4.5 Illustrative examples](#45-illustrative-examples)
  - [4.6 Fix and regression capacity plan](#46-fix-and-regression-capacity-plan)
  - [4.7 Behaviour-change record](#47-behaviour-change-record)
  - [4.8 Hardening cut-off rule](#48-hardening-cut-off-rule)
  - [4.9 Common hardening mistakes](#49-common-hardening-mistakes)
  - [4.10 Evidence to retain](#410-evidence-to-retain)
- [5 Activity 4: Confirm production control readiness](#5-activity-4-confirm-production-control-readiness)
  - [5.1 Production control readiness checklist](#51-production-control-readiness-checklist)
  - [5.2 Production control review record](#52-production-control-review-record)
  - [5.3 Data, semantic and refresh readiness template](#53-data-semantic-and-refresh-readiness-template)
  - [5.4 Access lifecycle readiness template](#54-access-lifecycle-readiness-template)
  - [5.5 Audit and traceability evidence checklist](#55-audit-and-traceability-evidence-checklist)
  - [5.6 Illustrative example: production control gap](#56-illustrative-example-production-control-gap)
  - [5.7 Control readiness status guide](#57-control-readiness-status-guide)
  - [5.8 Common control-readiness mistakes](#58-common-control-readiness-mistakes)
  - [5.9 Evidence to retain](#59-evidence-to-retain)
- [6 Activity 5: Confirm operational reliability and observability](#6-activity-5-confirm-operational-reliability-and-observability)
  - [6.1 Operational readiness checklist](#61-operational-readiness-checklist)
  - [6.2 Monitoring coverage matrix](#62-monitoring-coverage-matrix)
  - [6.3 Operational threshold template](#63-operational-threshold-template)
  - [6.4 Incident severity guide](#64-incident-severity-guide)
  - [6.5 Alert routing template](#65-alert-routing-template)
  - [6.6 Pause and rollback decision guide](#66-pause-and-rollback-decision-guide)
  - [6.7 Feedback-to-trace template](#67-feedback-to-trace-template)
  - [6.8 Early-life support monitoring cadence](#68-early-life-support-monitoring-cadence)
  - [6.9 Common observability mistakes](#69-common-observability-mistakes)
  - [6.10 Evidence to retain](#610-evidence-to-retain)
- [7 Activity 6: Prepare support, documentation, onboarding and controlled adoption readiness](#7-activity-6-prepare-support-documentation-onboarding-and-controlled-adoption-readiness)
  - [7.1 Documentation readiness checklist](#71-documentation-readiness-checklist)
  - [7.2 Documentation set by audience](#72-documentation-set-by-audience)
  - [7.3 User onboarding checklist](#73-user-onboarding-checklist)
  - [7.4 Release notes template](#74-release-notes-template)
  - [7.5 Known limitations template](#75-known-limitations-template)
  - [7.6 Support runbook outline](#76-support-runbook-outline)
  - [7.7 Controlled adoption readiness plan](#77-controlled-adoption-readiness-plan)
  - [7.8 Issue communication examples](#78-issue-communication-examples)
  - [7.9 Documentation ownership plan](#79-documentation-ownership-plan)
  - [7.10 Common documentation and onboarding mistakes](#710-common-documentation-and-onboarding-mistakes)
  - [7.11 Evidence to retain](#711-evidence-to-retain)
- [8 Activity 7: Consolidate operating model, budget and roadmap capacity](#8-activity-7-consolidate-operating-model-budget-and-roadmap-capacity)
  - [8.1 Operating model capacity worksheet](#81-operating-model-capacity-worksheet)
  - [8.2 Run / fix / improve / expand roadmap model](#82-run-fix-improve-expand-roadmap-model)
  - [8.3 Cost and capacity estimate template](#83-cost-and-capacity-estimate-template)
  - [8.4 Capacity reservation template](#84-capacity-reservation-template)
  - [8.5 Roadmap prioritisation guide](#85-roadmap-prioritisation-guide)
  - [8.6 Funding and approval record](#86-funding-and-approval-record)
  - [8.7 Illustrative example: capacity-aware roadmap](#87-illustrative-example-capacity-aware-roadmap)
  - [8.8 Common operating-model and budget mistakes](#88-common-operating-model-and-budget-mistakes)
  - [8.9 Evidence to retain](#89-evidence-to-retain)
- [9 Activity 8: Approve and execute controlled release, residual-risk acceptance and Phase 9 handover](#9-activity-8-approve-and-execute-controlled-release-residual-risk-acceptance-and-phase-9-handover)
  - [9.1 Controlled release decision record](#91-controlled-release-decision-record)
  - [9.2 Final release approval checklist](#92-final-release-approval-checklist)
  - [9.3 Residual-risk acceptance record](#93-residual-risk-acceptance-record)
  - [9.4 Release package contents](#94-release-package-contents)
  - [9.5 Release execution or handover plan](#95-release-execution-or-handover-plan)
  - [9.6 Pause, rollback and narrowing authority](#96-pause-rollback-and-narrowing-authority)
  - [9.7 Phase 9 handover template](#97-phase-9-handover-template)
  - [9.8 Post-release review criteria](#98-post-release-review-criteria)
  - [9.9 Expansion criteria](#99-expansion-criteria)
  - [9.10 Common release approval mistakes](#910-common-release-approval-mistakes)
  - [9.11 Evidence to retain](#911-evidence-to-retain)

---

## 1 How to use this annex

These annexes provide optional working templates for **Phase 8: Production readiness and controlled release**. They are intended to help teams convert pilot evidence into a controlled production release decision, not to create a mandatory checklist or a parallel delivery methodology.

The main Phase 8 guide explains the release logic: what can go live, what must be fixed before release, what constraints apply, who owns the capability, what risks are accepted, what budget and support capacity are required, and how the capability should move into Phase 9 operation, adoption and improvement.

This annex provides reusable working material for that process. Teams should select only the templates that match the delivery intent, risk level, organisational maturity and production exposure of the release.

For a narrow controlled release, some templates may be lightweight. For a higher-risk release, broader user exposure, sensitive data, regulated use cases or executive decision support, the evidence, sign-off, support, monitoring, risk acceptance and cost material should be treated more formally.

The annexes are especially useful for:

- classifying issues from the pilot and deciding which must be fixed before release;

- defining the final production release boundary;

- tracking pre-release hardening, fixes and regression evidence;

- confirming production controls, monitoring and operational readiness;

- preparing support, documentation, onboarding and escalation material;

- sizing support, bug-fix, improvement and roadmap capacity;

- recording release approval, residual-risk acceptance and Phase 9 handover.

The templates should be adapted, not copied mechanically. A team should be able to explain why each selected artefact is needed for the release decision. If a template does not help decide, support, control or operate the production release, it should be simplified or skipped.

The central test for Phase 8 documentation is practical: can users understand what they can rely on, can support teams diagnose and respond to issues, can owners fund and govern the capability, and can decision-makers defend the release boundary and residual risks.

**  
**

## 2 Activity 1: Confirm production scope and release boundary

### 2.1 Production release boundary template

| Area                        | Production release decision                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| Release objective           | What the first controlled production release is intended to enable.         |
| Target users                | Named user groups included in release.                                      |
| Excluded users              | User groups not included and why.                                           |
| Data domains                | Approved domains included in production scope.                              |
| Data assets                 | Production data assets, views, marts, APIs or semantic assets in scope.     |
| Metrics                     | Approved metrics available for production use.                              |
| Dimensions                  | Approved dimensions, hierarchies and filters.                               |
| Question types              | Supported question patterns.                                                |
| Answer types                | Number, table, chart, narrative, caveated answer, clarification or refusal. |
| Follow-up behaviour         | Which follow-ups are supported and which are refused or clarified.          |
| Explicit exclusions         | Questions, domains, users, outputs or integrations excluded from release.   |
| Known limitations           | Limitations users and support teams must understand.                        |
| Evidence basis              | Phase 7 evidence supporting inclusion.                                      |
| Release constraints         | Conditions under which the release is allowed.                              |
| Cost / capacity implication | Expected support, usage, monitoring or change impact.                       |
| Owner                       | Person or group accountable for the release boundary.                       |
| Approval status             | Draft / reviewed / approved / rejected.                                     |

### 2.2 Boundary-to-evidence mapping

| Release item              | Included? | Phase 7 evidence                                      | Production concern                                   | Decision                             |
|---------------------------|-----------|-------------------------------------------------------|------------------------------------------------------|--------------------------------------|
| Regional sales managers   | Yes       | High usage, repeated workflow fit, few support issues | Needs onboarding and clear limitation guidance       | Include                              |
| Revenue by region         | Yes       | Frequently used, trusted, low issue rate              | Current-month data caveat required                   | Include with caveat                  |
| Margin by product         | No        | High demand but inconsistent interpretation           | Metric definition not production-ready               | Exclude / roadmap                    |
| Customer-level drill-down | Limited   | Useful but raised access concerns                     | Requires stricter access checks                      | Include for analysts only            |
| Forecasting questions     | No        | Users requested it, but not tested                    | Unsupported answer type and high interpretation risk | Exclude                              |
| Executive summary answers | Limited   | Valued by pilot users                                 | Risk of overstatement                                | Include only with source and caveats |

### 2.3 Suggested release boundary statuses

| Status                  | Meaning                                                                  |
|-------------------------|--------------------------------------------------------------------------|
| Include                 | Supported by evidence and ready for controlled production release.       |
| Include with caveat     | Usable in production only with visible limitation or usage condition.    |
| Include with constraint | Usable only for defined users, domains, volumes or support conditions.   |
| Fix before inclusion    | Valuable but requires Phase 8 hardening before release.                  |
| Monitor after release   | Acceptable only with threshold, owner and response route.                |
| Exclude from release    | Not safe or mature enough for first production release.                  |
| Move to Phase 9 roadmap | Useful future candidate, but not needed for first release.               |
| Return to earlier phase | Requires renewed data, semantic, architecture, validation or pilot work. |

### 2.4 Illustrative example: controlled production boundary

Example — illustrative

| Area                        | Decision                                                                             |
|-----------------------------|--------------------------------------------------------------------------------------|
| Release objective           | Enable regional sales managers to ask governed questions on revenue performance.     |
| Target users                | 20 regional sales managers and 3 sales operations analysts.                          |
| Excluded users              | Finance, executives, account executives and external users.                          |
| Data domains                | Sales revenue and pipeline summary.                                                  |
| Data assets                 | sales_revenue_mart, region_dimension, pipeline_summary_view.                         |
| Metrics                     | Net revenue, customer count, pipeline conversion.                                    |
| Excluded metrics            | Margin, profitability, forecast revenue, salesperson performance.                    |
| Question types              | KPI lookup, trend, comparison, variance by region or segment.                        |
| Answer types                | Number, table, short narrative, caveated answer, clarification and refusal.          |
| Follow-up behaviour         | Follow-ups allowed within same domain and approved dimensions.                       |
| Known limitations           | Current-month revenue is provisional; pipeline refresh is daily, not real time.      |
| Release constraints         | No customer-level profitability, no forecasting, no individual performance analysis. |
| Cost / capacity implication | Expected 100–150 questions per week; daily support review for first two weeks.       |
| Owner                       | Sales operations product owner.                                                      |

### 2.5 Scope challenge questions

Use these questions before approving the release boundary:

- Is each included question type supported by Phase 7 evidence?

- Is the release scope smaller than or equal to the evidence-proven pilot boundary?

- Are any items included mainly because users requested them?

- Are all included metrics approved, owned and explainable?

- Are all included joins, filters, caveats and dimensions safe for production use?

- Can support teams explain what is in and out of scope?

- Can users understand the limitations without reading a technical document?

- Would the release still be safe if usage doubled?

- Does the proposed scope create additional cost, monitoring or support needs?

- Is there a named owner for every included domain, metric and release constraint?

### 2.6 Common boundary mistakes

| Mistake                                        | Why it matters                                                                                |
|------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Including everything that worked once in pilot | One successful interaction is not production evidence.                                        |
| Letting user demand define production scope    | Demand proves interest, not readiness.                                                        |
| Treating caveats as a substitute for controls  | Caveats do not fix weak semantics, unsafe joins or missing ownership.                         |
| Expanding to senior users too early            | Decision impact and reputational risk increase sharply.                                       |
| Including unsupported follow-ups               | Multi-turn behaviour can silently expand scope.                                               |
| Forgetting support impact                      | A broader boundary creates more incidents, questions and interpretation support.              |
| Ignoring cost impact                           | More users and broader question types can increase model, query, monitoring and support cost. |

### 2.7 Evidence to retain

- Approved production release boundary.

- In-scope and out-of-scope list.

- Boundary-to-evidence mapping.

- Known limitations and release constraints.

- Data, semantic and access owners for included scope.

- Cost and capacity assumptions.

- Decision record approving or rejecting the proposed boundary.

## 3 Activity 2: Triage pilot findings and production-readiness backlog

### 3.1 Production-readiness issue disposition register

| Item                   | Description                                                                                                                                 |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Issue ID               | Unique reference for tracking.                                                                                                              |
| Source                 | Pilot feedback, support ticket, monitoring alert, hot fix, access issue, cost finding, governance review, user interview.                   |
| Description            | Clear description of the finding or issue.                                                                                                  |
| Affected user group    | Users impacted by the issue.                                                                                                                |
| Affected workflow      | Business workflow or decision context impacted.                                                                                             |
| Affected component     | Data, semantics, access, prompt, model, query generation, UI, monitoring, support, documentation, cost, governance.                         |
| Frequency              | One-off, occasional, repeated, frequent.                                                                                                    |
| Severity               | Low / medium / high / critical.                                                                                                             |
| Visibility             | Low-risk internal, business user, senior stakeholder, executive, regulatory / audit-facing.                                                 |
| Decision impact        | None, low, moderate, high, material decision impact.                                                                                        |
| Current status         | Open, in review, fixed, accepted, deferred, rejected.                                                                                       |
| Proposed disposition   | Blocker, pre-release fix, release constraint, accepted residual risk, monitored risk, Phase 9 backlog, enhancement, redesign / stop signal. |
| Required action        | Fix, constrain, monitor, accept, document, defer, return to earlier phase, stop.                                                            |
| Owner                  | Named owner accountable for resolution or acceptance.                                                                                       |
| Cost / capacity impact | Expected effort, people or budget implication.                                                                                              |
| Release implication    | Can release proceed? Under what condition?                                                                                                  |
| Evidence required      | Test, regression result, sign-off, monitoring rule, documentation, risk acceptance.                                                         |
| Review date            | Date for decision or follow-up.                                                                                                             |

### 3.2 Issue disposition guide

| Disposition            | Use when                                                                                             | Release implication                                 |
|------------------------|------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| Production blocker     | The issue makes production unsafe, ungoverned or unsupportable.                                      | Fix before release, narrow, redesign or stop.       |
| Pre-release fix        | The issue is fixable and required before controlled release.                                         | Add to Phase 8 hardening backlog.                   |
| Release constraint     | The issue can be managed by limiting users, scope, question types, volume or support conditions.     | Release only with explicit constraint.              |
| Accepted residual risk | The issue is known, understood and accepted by the accountable owner.                                | Record rationale, owner and review condition.       |
| Monitored risk         | The issue is acceptable only if actively watched.                                                    | Add monitoring threshold, owner and response route. |
| Phase 9 backlog        | The issue is not required for first release but should be improved after go-live.                    | Add to run / fix / improve backlog.                 |
| Later enhancement      | The item is valuable but outside release readiness.                                                  | Add to roadmap, not release decision.               |
| Redesign / stop signal | The issue exposes structural weakness in data, semantics, architecture, controls or operating model. | Return to earlier phase, redesign, pause or stop.   |

### 3.3 Priority assessment matrix

Issue priority should not be based on technical severity alone.

| Dimension                | Low                              | Medium                                       | High                                                                |
|--------------------------|----------------------------------|----------------------------------------------|---------------------------------------------------------------------|
| User impact              | Few users, workaround available. | Multiple users or repeated friction.         | Critical user group or no practical workaround.                     |
| Decision impact          | Informational only.              | Supports operational or tactical decision.   | Supports senior, financial, regulatory or high-visibility decision. |
| Trust impact             | Annoying but explainable.        | Could create hesitation or confusion.        | Could damage confidence in the whole release.                       |
| Access / security impact | No exposure risk.                | Permission ambiguity or unclear audit trail. | Data exposure, bypass risk or unauthorised access.                  |
| Support impact           | Easy to explain or resolve.      | Requires specialist support.                 | Likely to create repeated incidents or escalation.                  |
| Cost impact              | Negligible.                      | Noticeable but manageable.                   | Could exceed budget, monitoring or support capacity.                |
| Visibility               | Internal delivery team.          | Business users.                              | Executive, audit, regulator or external stakeholder.                |

### 3.4 Illustrative examples

| Issue                                                  | Technical severity | Production priority | Reason                                                     | Disposition                            |
|--------------------------------------------------------|--------------------|---------------------|------------------------------------------------------------|----------------------------------------|
| Occasional formatting issue in analyst table export    | Low                | Low                 | Does not affect interpretation or decision quality.        | Phase 9 backlog                        |
| Wrong caveat missing from executive revenue answer     | Medium             | High                | Could lead senior users to over-trust provisional numbers. | Pre-release fix                        |
| Popular request for margin analysis                    | Not a defect       | Medium              | Strong demand, but metric not production-ready.            | Exclude / roadmap                      |
| Access removal takes three days                        | Medium             | High                | Weak access lifecycle for production users.                | Pre-release fix or release constraint  |
| High-cost query triggered by broad follow-up           | Medium             | High                | Could create cost spikes and performance issues.           | Fix / monitor / constrain              |
| Minor typo in onboarding guide                         | Low                | Low                 | Does not affect safe use.                                  | Fix if easy, otherwise Phase 9 backlog |
| Users repeatedly ask unsupported forecasting questions | Not a defect       | Medium              | Scope misunderstanding may create trust risk.              | Onboarding update and refusal rule     |
| SQL generation fails for a supported metric            | High               | High                | Supported production question cannot be relied on.         | Production blocker                     |

### 3.5 Pre-release hardening backlog template

| Fix ID  | Issue linked | Required fix                                         | Owner                 | Priority | Effort | Regression required       | Release dependency         | Status |
|---------|--------------|------------------------------------------------------|-----------------------|----------|--------|---------------------------|----------------------------|--------|
| FIX-001 | ISS-014      | Add missing caveat to current-month revenue answer   | Product / engineering | High     | Small  | Answer-format regression  | Required before release    | Open   |
| FIX-002 | ISS-021      | Tighten follow-up query cost guardrail               | Engineering           | High     | Medium | Cost and query regression | Required before release    | Open   |
| FIX-003 | ISS-032      | Update onboarding to clarify unsupported forecasting | Product / adoption    | Medium   | Small  | Documentation review      | Required before onboarding | Open   |

### 3.6 Release constraint log

| Constraint                            | Reason                                     | Applies to                | Owner          | User communication needed? | Monitoring needed?        | Review trigger         |
|---------------------------------------|--------------------------------------------|---------------------------|----------------|----------------------------|---------------------------|------------------------|
| No forecasting questions              | Not validated and high interpretation risk | All users                 | Product owner  | Yes                        | Unsupported-question rate | Phase 9 roadmap review |
| Customer drill-down only for analysts | Access and interpretation risk             | Sales operations analysts | Data owner     | Yes                        | Access logs               | After access review    |
| Usage cap of 150 questions / week     | Cost and support capacity                  | First release cohort      | Platform owner | Yes                        | Cost dashboard            | After four weeks       |

### 3.7 Residual-risk candidate template

| Risk                                                | Why not fixed before release?                          | Release condition                                 | Accountable owner  | Monitoring / control           | Review date             |
|-----------------------------------------------------|--------------------------------------------------------|---------------------------------------------------|--------------------|--------------------------------|-------------------------|
| Current-month revenue may be provisional            | Source refresh timing cannot be changed before release | Caveat must be displayed in every relevant answer | Finance data owner | Caveat presence check          | Monthly                 |
| Some unsupported questions likely during first week | Users are still learning scope                         | Refusal wording and onboarding material updated   | Product owner      | Unsupported-question dashboard | Two weeks after release |

### 3.8 Triage meeting agenda

- Confirm release boundary under consideration.

- Review new and open Phase 7 findings.

- Classify each material issue by disposition.

- Identify production blockers and pre-release fixes.

- Confirm release constraints and monitored risks.

- Separate Phase 9 backlog items from later enhancements.

- Review cost, support and capacity implications.

- Confirm owners, evidence required and decision dates.

- Escalate structural blockers or unresolved risk acceptances.

- Update the release recommendation.

### 3.9 Common triage mistakes

| Mistake                                        | Why it matters                                                                                        |
|------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Treating all bugs by technical severity        | Business impact depends on user, workflow, decision and visibility.                                   |
| Hiding issues in a generic backlog             | Release decisions require disposition, ownership and conditions.                                      |
| Accepting fixes without regression evidence    | A fix can change model behaviour, prompts, SQL or answer interpretation.                              |
| Treating user requests as release requirements | Demand proves interest, not readiness.                                                                |
| Deferring support issues to Phase 9            | Support gaps become production incidents once users rely on the system.                               |
| Ignoring executive visibility                  | A small defect in a senior workflow can damage trust more than a larger issue in a low-risk workflow. |
| Assuming all residual risks are equal          | Residual risk must be accepted by the right owner, not just noted by the project team.                |

### 3.10 Evidence to retain

- Production-readiness issue disposition register.

- Pre-release hardening backlog.

- Release constraint log.

- Residual-risk candidate list.

- Monitored-risk list with thresholds and owners.

- Phase 9 backlog and roadmap candidates.

- Triage decision record.

- Evidence requirements for each release-critical fix.

**  
**

## 4 Activity 3: Complete pre-release hardening and regression checks

### 4.1 Pre-release hardening backlog template

| Item                | Description                                                                                                                      |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Fix ID              | Unique reference for the fix.                                                                                                    |
| Linked issue        | Issue ID from the production-readiness issue disposition register.                                                               |
| Fix description     | What needs to change.                                                                                                            |
| Fix type            | Bug, control gap, documentation gap, onboarding gap, support gap, monitoring gap, cost issue, access issue.                      |
| Affected component  | Data, semantics, metadata, prompt, model, retrieval, SQL generation, validation, UI, access, monitoring, support, documentation. |
| Release dependency  | Required before release / required before onboarding / required before wider release / optional.                                 |
| Owner               | Named person or team accountable for the fix.                                                                                    |
| Support required    | Engineering, data owner, semantic owner, product, support, security, finance, other.                                             |
| Effort              | Small / medium / large.                                                                                                          |
| Risk if unfixed     | Impact on release if the fix is not completed.                                                                                   |
| Regression required | Test or check required after the fix.                                                                                            |
| Evidence required   | Test result, trace, screenshot, log, approval, updated documentation, monitoring rule.                                           |
| Status              | Open / in progress / fixed / regression passed / accepted / deferred / blocked.                                                  |
| Decision            | Release, release with constraint, delay, narrow, return to earlier phase, stop.                                                  |

### 4.2 Fix classification guide

| Fix type                       | Examples                                                                    | Typical evidence                                                   |
|--------------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------|
| Answer behaviour fix           | Missing caveat, unclear refusal, overconfident wording, weak clarification. | Before / after answer examples, trace, answer-quality review.      |
| Query or execution fix         | Unsafe query pattern, slow query, missing limit, wrong aggregation.         | SQL test, execution log, performance check, regression case.       |
| Data / semantic fix            | Metric caveat, incorrect join, missing dimension, stale metadata.           | Data-owner sign-off, metric test, reconciliation, metadata update. |
| Access / security fix          | Incorrect permission, slow revocation, weak masking, missing audit trail.   | Access test, audit log, permission-change evidence.                |
| Monitoring fix                 | Missing alert, weak threshold, incomplete trace, cost blind spot.           | Dashboard update, alert test, log sample, threshold approval.      |
| Support fix                    | Missing runbook, unclear escalation, no owner for common issue.             | Updated runbook, support acceptance, escalation test.              |
| Documentation / onboarding fix | Known limitation unclear, unsupported questions not explained.              | Updated guide, release note, onboarding review.                    |
| Cost fix                       | Expensive query pattern, uncontrolled model route, usage spike.             | Cost estimate, guardrail test, budget impact note.                 |

### 4.3 Regression check template

| Item              | Description                                                                                                        |
|-------------------|--------------------------------------------------------------------------------------------------------------------|
| Regression ID     | Unique reference.                                                                                                  |
| Fix linked        | Fix ID being tested.                                                                                               |
| Test objective    | What the regression check is proving.                                                                              |
| Affected flow     | User question, access check, retrieval, SQL generation, answer generation, support flow, monitoring, cost control. |
| Test input        | Question, user profile, data condition, access scenario or operational event tested.                               |
| Expected result   | What should happen.                                                                                                |
| Actual result     | What happened.                                                                                                     |
| Pass / fail       | Result of the regression check.                                                                                    |
| Evidence retained | Logs, trace, generated SQL, answer output, screenshot, monitoring event, approval.                                 |
| Owner             | Person accountable for the check.                                                                                  |
| Re-test trigger   | What future change should trigger this test again.                                                                 |

### 4.4 Suggested non-regression coverage

| Change made             | Minimum regression checks                                                             |
|-------------------------|---------------------------------------------------------------------------------------|
| Prompt change           | Supported questions, refusals, caveats, answer format, overstatement check.           |
| Model change            | Golden questions, latency, cost, answer quality, refusal behaviour.                   |
| Retrieval change        | Metadata selection, metric matching, caveat retrieval, unsupported-question handling. |
| SQL generation change   | Query correctness, join safety, aggregation, filters, limits, execution guardrails.   |
| Data or semantic change | Metric reconciliation, dimensions, caveats, lineage, sample questions.                |
| Access rule change      | Allowed user, denied user, revoked user, row / column restriction, audit log.         |
| Monitoring change       | Alert trigger, alert routing, dashboard visibility, severity classification.          |
| UI or onboarding change | Scope visibility, limitation visibility, feedback route, support route.               |
| Cost control change     | Usage threshold, query cap, model-routing cost, high-cost question path.              |

### 4.5 Illustrative examples

| Fix                                                  | Why required before release                                     | Regression check                                                                                                   | Release decision           |
|------------------------------------------------------|-----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|----------------------------|
| Add current-month caveat to revenue answers          | Without the caveat, users may over-trust provisional numbers.   | Run revenue questions across month-to-date, prior month and trend examples. Confirm caveat appears where required. | Required before release    |
| Tighten follow-up limits for broad questions         | Broad follow-ups may trigger expensive or slow queries.         | Test broad follow-ups, unsupported filters and high-volume queries. Confirm refusal, clarification or cap.         | Required before release    |
| Update onboarding to explain unsupported forecasting | Users repeatedly asked for forecasts during pilot.              | Review onboarding material and refusal wording. Check unsupported forecasting questions are refused consistently.  | Required before onboarding |
| Improve table export formatting                      | Useful but does not affect answer trust or operational support. | Basic UI check.                                                                                                    | Phase 9 backlog            |
| Add dashboard link to every answer                   | Valuable but not required for first controlled release.         | Not needed for release.                                                                                            | Later enhancement          |

### 4.6 Fix and regression capacity plan

| Role / skill            | Needed for                                       | Estimated capacity | Timing     | Reserved? | Risk if unavailable                        |
|-------------------------|--------------------------------------------------|--------------------|------------|-----------|--------------------------------------------|
| Engineering             | Prompt, model, orchestration, query and UI fixes | 5 days             | Week 1–2   | Yes / No  | Fixes delayed or untested.                 |
| Data owner              | Metric, caveat and data-quality sign-off         | 2 days             | Week 1     | Yes / No  | Release boundary cannot be approved.       |
| Semantic owner          | Definition, join and dimension checks            | 2 days             | Week 1–2   | Yes / No  | Unsupported questions may slip into scope. |
| Security / access owner | Access lifecycle and audit checks                | 1–2 days           | Week 2     | Yes / No  | Release blocked or constrained.            |
| Product owner           | Prioritisation, release notes, known limitations | 3 days             | Throughout | Yes / No  | Fixes lack release decision context.       |
| Support owner           | Runbook and escalation validation                | 2 days             | Week 2     | Yes / No  | Release not supportable.                   |

### 4.7 Behaviour-change record

| Change                                            | User-visible? | Support-visible? | Governance-visible? | Documentation update needed? | Release note needed? |
|---------------------------------------------------|---------------|------------------|---------------------|------------------------------|----------------------|
| Refusal wording changed for forecasting questions | Yes           | Yes              | No                  | Yes                          | Yes                  |
| Revenue caveat added to current-month answers     | Yes           | Yes              | Yes                 | Yes                          | Yes                  |
| Cost guardrail added for broad follow-ups         | Sometimes     | Yes              | Yes                 | Yes                          | Yes                  |
| Internal log tagging improved                     | No            | Yes              | Yes                 | No                           | No                   |
| Access revocation process changed                 | No            | Yes              | Yes                 | Yes                          | Yes                  |

### 4.8 Hardening cut-off rule

Before starting hardening, agree a cut-off rule to prevent Phase 8 becoming an open-ended improvement loop.

Suggested rule:

| Category            | Treatment after cut-off                                             |
|---------------------|---------------------------------------------------------------------|
| Production blocker  | Must be fixed, or release is delayed / narrowed / stopped.          |
| Pre-release fix     | Must be fixed unless formally reclassified.                         |
| Release constraint  | Can remain only if reflected in release boundary and user guidance. |
| Monitored risk      | Can remain only with threshold, owner and response route.           |
| Phase 9 improvement | Deferred to Phase 9 backlog.                                        |
| Later enhancement   | Deferred to roadmap.                                                |

### 4.9 Common hardening mistakes

| Mistake                                  | Why it matters                                                                     |
|------------------------------------------|------------------------------------------------------------------------------------|
| Fixing without regression                | The fix may break another supported question, control or user flow.                |
| Treating prompt changes as low risk      | Prompt changes can alter answer style, caveats, refusals, SQL and trust behaviour. |
| Reassigning the delivery team too early  | Critical fixes may be delayed or handled by people without system context.         |
| Adding enhancements during hardening     | The release target keeps moving and regression scope expands.                      |
| Updating behaviour without release notes | Users and support teams cannot explain changed behaviour.                          |
| Deferring support fixes to Phase 9       | Support gaps become live incidents after release.                                  |
| Ignoring cost impact of fixes            | A safer fix may increase latency, model usage, monitoring or support effort.       |

### 4.10 Evidence to retain

- Pre-release hardening backlog.

- Fix evidence and linked issue IDs.

- Regression test results.

- Behaviour-change and control-change record.

- Updated release notes and known limitations.

- Updated runbooks, onboarding material or support guidance.

- Capacity reservation record for fixes and regression checks.

- Remaining unresolved issue list with release implication.

## 5 Activity 4: Confirm production control readiness

### 5.1 Production control readiness checklist

| Control area         | Readiness questions                                                                          | Evidence to retain                                          |
|----------------------|----------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| Data assets          | Are all production data assets approved for the release boundary?                            | Approved asset list, owner sign-off, lineage reference.     |
| Refresh              | Are refresh frequency, latency and freshness expectations clear?                             | Refresh schedule, freshness threshold, failure response.    |
| Metrics              | Are included metrics approved, implemented and explainable?                                  | Metric cards, reconciliation evidence, owner approval.      |
| Dimensions           | Are dimensions, hierarchies and filters production-ready?                                    | Dimension register, hierarchy rules, filter rules.          |
| Joins and grain      | Are approved joins, grains and aggregation rules enforceable?                                | Join rules, grain checks, sample query evidence.            |
| Caveats              | Are mandatory caveats visible where needed?                                                  | Caveat matrix, answer examples, caveat test evidence.       |
| Metadata             | Is runtime metadata complete enough for supported questions?                                 | Metadata coverage check, retrieval test evidence.           |
| Access               | Are provisioning, permission changes and revocation ready?                                   | Access test evidence, access lifecycle process.             |
| Security             | Are masking, row / column controls and exposure limits enforced?                             | Security test evidence, policy mapping, logs.               |
| Auditability         | Can the organisation trace who asked what, which data was used and what answer was produced? | Trace logs, audit log sample, retention decision.           |
| Compliance / privacy | Are required compliance, privacy and data-owner conditions reflected in the system?          | Review record, sign-off where required, residual-risk note. |

### 5.2 Production control review record

| Area           | Owner                     | Review required? | Sign-off required? | Status       | Conditions / comments                     |
|----------------|---------------------------|------------------|--------------------|--------------|-------------------------------------------|
| Data owner     | Sales analytics owner     | Yes              | Yes                | Approved     | Revenue mart approved for regional users. |
| Semantic owner | Finance BI lead           | Yes              | Yes                | Conditional  | Current-month caveat must be displayed.   |
| Security       | Security architect        | Yes              | Yes                | Approved     | Row-level access test passed.             |
| Privacy        | Privacy officer           | Yes              | No                 | Reviewed     | No personal data in release boundary.     |
| Compliance     | Compliance representative | Yes              | Conditional        | Pending      | Needs final release note review.          |
| Audit          | Internal audit            | Optional         | No                 | Not required | Audit log retained for review.            |
| Platform owner | Data platform lead        | Yes              | Yes                | Approved     | Monitoring and access logs available.     |

### 5.3 Data, semantic and refresh readiness template

| Item                           | Production decision                                                   |
|--------------------------------|-----------------------------------------------------------------------|
| Data asset                     | Name of table, view, mart, API or semantic layer asset.               |
| Release use                    | Which question types or user groups depend on it.                     |
| Owner                          | Data or semantic owner.                                               |
| Approved for release?          | Yes / no / conditional.                                               |
| Refresh frequency              | Real time, hourly, daily, weekly, monthly, manual.                    |
| Acceptable freshness threshold | Maximum tolerated delay before caveat, alert or pause.                |
| Caveat required?               | Yes / no.                                                             |
| Quality checks                 | Completeness, reconciliation, freshness, schema, volume, anomaly.     |
| Access controls                | User groups, row / column rules, masking, aggregation limits.         |
| Metadata readiness             | Complete / partial / insufficient.                                    |
| Release implication            | Include, include with caveat, constrain, fix before release, exclude. |

### 5.4 Access lifecycle readiness template

| Scenario                         | Expected behaviour                                         | Evidence required                 | Owner                    | Status |
|----------------------------------|------------------------------------------------------------|-----------------------------------|--------------------------|--------|
| New approved user added          | User receives correct access only within release boundary. | Provisioning log and access test. | Support / IAM owner      |        |
| User changes role                | Access changes to match new role.                          | Role-change test.                 | IAM owner                |        |
| User leaves pilot / organisation | Access removed within agreed timeframe.                    | Revocation log.                   | IAM owner                |        |
| User requests unsupported domain | Access denied or answer refused.                           | Refusal trace and access log.     | Product / engineering    |        |
| User lacks row-level permission  | Restricted data not returned.                              | Row-level access test.            | Data platform owner      |        |
| Support investigates issue       | Support can view required logs without overexposure.       | Support access review.            | Security / support owner |        |

### 5.5 Audit and traceability evidence checklist

A production release should retain enough evidence to support diagnosis, governance and review.

| Evidence              | Minimum expectation                                    |
|-----------------------|--------------------------------------------------------|
| User identity         | Who asked the question.                                |
| Timestamp             | When the interaction occurred.                         |
| Question              | Original user question and relevant follow-up context. |
| Scope classification  | Supported, clarified, refused or out of scope.         |
| Retrieved metadata    | Metrics, dimensions, caveats or examples used.         |
| Generated query       | SQL or tool call generated, where applicable.          |
| Executed query        | Final executed query, with validation status.          |
| Data source           | Data assets used.                                      |
| Answer                | Final answer shown to the user.                        |
| Caveats / limitations | Caveats displayed or missing.                          |
| Cost / latency        | Runtime, model calls, query cost or cost proxy.        |
| Access decision       | Allowed, denied, constrained or refused.               |
| Error / incident link | Link to support ticket or incident if relevant.        |

### 5.6 Illustrative example: production control gap

| Finding                                                                 | Release implication                                    | Response                                                                     |
|-------------------------------------------------------------------------|--------------------------------------------------------|------------------------------------------------------------------------------|
| Revenue metric approved, but current-month refresh can lag by 24 hours. | Release possible with caveat and freshness monitoring. | Display current-month caveat, add freshness alert, review after first month. |
| Customer drill-down works technically but access review is incomplete.  | Cannot release to all users.                           | Restrict to sales operations analysts until access review is complete.       |
| Audit logs record the answer but not retrieved metadata.                | Weak traceability for support and governance.          | Fix before release or constrain use to lower-risk questions.                 |
| Metric owner has approved pilot use but not production use.             | Ownership gap.                                         | Obtain production approval or exclude metric from release.                   |
| Revocation process is manual and untested.                              | Production access lifecycle risk.                      | Test revocation before release and assign owner / SLA.                       |

### 5.7 Control readiness status guide

| Status                | Meaning                                                             | Release implication                               |
|-----------------------|---------------------------------------------------------------------|---------------------------------------------------|
| Ready                 | Control is approved, enforceable and owned.                         | Release can proceed for this area.                |
| Ready with caveat     | Control is acceptable with visible limitation or monitoring.        | Release with condition.                           |
| Ready with constraint | Control works only for specific users, domains or usage levels.     | Constrain release boundary.                       |
| Fix before release    | Control gap is material but fixable.                                | Add to hardening backlog.                         |
| Accept residual risk  | Control gap remains but is knowingly accepted by accountable owner. | Record risk acceptance and review date.           |
| Not ready             | Control gap makes release unsafe or ungoverned.                     | Exclude, narrow, return to earlier phase or stop. |

### 5.8 Common control-readiness mistakes

| Mistake                                    | Why it matters                                                                         |
|--------------------------------------------|----------------------------------------------------------------------------------------|
| Treating pilot access as production access | Pilot access is often manually managed and not lifecycle-ready.                        |
| Approving data without refresh rules       | Users may rely on stale or provisional data without knowing it.                        |
| Assuming caveats solve control gaps        | Caveats help interpretation; they do not replace access, quality or semantic controls. |
| Missing owner sign-off                     | Production controls need accountable owners after the project team leaves.             |
| Logging too little context                 | Support cannot diagnose issues without query, metadata, answer and access traces.      |
| Making controls manual without capacity    | Manual controls fail unless owned, scheduled, monitored and funded.                    |
| Forgetting cost of controls                | Monitoring, audit retention, access management and quality checks all create run cost. |

### 5.9 Evidence to retain

- Production control readiness summary.

- Approved data, semantic, metadata and refresh scope.

- Access lifecycle test evidence.

- Security, privacy, compliance, audit and data-owner review record.

- Audit and traceability evidence sample.

- Production-control gap list with release implications.

- Control ownership and maintenance responsibilities.

## 6 Activity 5: Confirm operational reliability and observability

### 6.1 Operational readiness checklist

| Area                  | Readiness questions                                                         | Evidence to retain                                          |
|-----------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------|
| Usage                 | What user volume and question volume are expected for the release boundary? | Usage assumption, pilot usage baseline, volume estimate.    |
| Concurrency           | How many users or requests may run at the same time?                        | Concurrency assumption, load / stress check where relevant. |
| Latency               | What response time is acceptable for supported question types?              | Latency threshold, pilot latency evidence, timeout rule.    |
| Availability          | What level of service availability is expected for first release?           | Service expectation, support hours, downtime process.       |
| Cost                  | What cost level is expected and what would trigger review?                  | Cost estimate, cost threshold, budget owner.                |
| Data freshness        | What freshness level is required for each production data asset?            | Freshness threshold, refresh log, alert rule.               |
| Failures              | What failure types need monitoring and escalation?                          | Error taxonomy, alert route, incident trigger.              |
| Unsupported questions | How will repeated unsupported questions be detected?                        | Unsupported-question dashboard or review process.           |
| User issues           | How will feedback, complaints and support tickets be linked to traces?      | Feedback-to-trace process.                                  |
| Pause / rollback      | Who can pause, narrow or roll back the release?                             | Pause / rollback decision route.                            |

### 6.2 Monitoring coverage matrix

| Component          | What to monitor                                              | Example signal                                             |
|--------------------|--------------------------------------------------------------|------------------------------------------------------------|
| User interaction   | Questions asked, user group, scope classification.           | Supported / clarified / refused / failed.                  |
| Metadata retrieval | Retrieved metric, dimension, caveat or example.              | Retrieval success, missing metadata, low-confidence match. |
| Model calls        | Model route, latency, cost, errors.                          | Token use, failed call, unexpected model path.             |
| Query generation   | SQL generated, validation status, blocked queries.           | Unsafe SQL blocked, validation failure.                    |
| Query execution    | Runtime, scanned data, failures, timeout.                    | Slow query, high-cost query, execution error.              |
| Answer generation  | Caveat inclusion, answer format, refusal behaviour.          | Missing caveat, empty result, overlong answer.             |
| Access decision    | Allowed, denied, constrained or revoked access.              | Denied access, role mismatch, revoked-user attempt.        |
| Cost               | Model cost, query cost, monitoring cost, support cost proxy. | Daily cost, cost per interaction, threshold breach.        |
| Support            | Tickets, issue type, response time, repeated user problems.  | Open incidents, repeated unsupported questions.            |
| Data freshness     | Last refresh, failed refresh, stale asset.                   | Freshness breach, missing source update.                   |

### 6.3 Operational threshold template

| Metric / signal          | Normal range  | Warning threshold             | Critical threshold            | Owner                    | Response                                                   |
|--------------------------|---------------|-------------------------------|-------------------------------|--------------------------|------------------------------------------------------------|
| Average response latency | \< 10 seconds | \> 20 seconds                 | \> 45 seconds                 | Platform owner           | Investigate slow path, narrow heavy queries if needed.     |
| Failed interactions      | \< 2%         | \> 5%                         | \> 10%                        | Product / engineering    | Review traces, classify issue, escalate if repeated.       |
| Unsupported questions    | \< 10%        | \> 20%                        | \> 30%                        | Product owner            | Update onboarding, refusal wording or roadmap.             |
| Daily model / query cost | Within budget | 80% of daily threshold        | 100% of daily threshold       | Finance / platform owner | Review usage, apply cap, adjust routing.                   |
| Data freshness delay     | Within SLA    | 1 missed refresh              | 2 missed refreshes            | Data owner               | Add caveat, notify users, pause affected domain if needed. |
| Access failures          | None expected | Repeated denied-user attempts | Incorrect access granted      | Security / IAM owner     | Investigate immediately, consider pause.                   |
| Missing caveat rate      | 0             | Any repeated issue            | Any issue on high-risk metric | Product / data owner     | Fix before continued use if material.                      |

### 6.4 Incident severity guide

| Severity | Example                                                                                                              | Expected response                                                           |
|----------|----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Critical | Unauthorised data exposure, incorrect access, materially wrong executive answer, uncontrolled cost spike.            | Immediate escalation, consider pause / rollback, notify accountable owners. |
| High     | Repeated wrong answers for supported questions, missing caveats on material metrics, major latency failures.         | Same-day investigation, fix or constrain release.                           |
| Medium   | Repeated unsupported questions, confusing answer format, intermittent failures, support burden higher than expected. | Triage, monitor, update guidance or backlog.                                |
| Low      | Minor formatting issue, isolated unclear wording, low-impact UI problem.                                             | Fix if easy or add to Phase 9 backlog.                                      |

### 6.5 Alert routing template

| Alert                          | Trigger                                       | First owner          | Escalation owner | User communication needed?                    |
|--------------------------------|-----------------------------------------------|----------------------|------------------|-----------------------------------------------|
| Data freshness breach          | Asset misses agreed freshness threshold.      | Data owner           | Product owner    | Yes, if affected answers are still available. |
| Cost threshold breach          | Usage exceeds warning or critical threshold.  | Platform owner       | Finance owner    | Only if usage is capped or degraded.          |
| Access anomaly                 | Denied, revoked or unexpected access pattern. | Security / IAM owner | Risk owner       | Yes, if user access is affected.              |
| High failure rate              | Failed interactions exceed threshold.         | Engineering owner    | Product owner    | Yes, if issue affects supported questions.    |
| Missing caveat                 | Caveat not shown for required metric.         | Product / data owner | Governance owner | Yes, if users may have relied on answer.      |
| Repeated unsupported questions | Unsupported-question threshold exceeded.      | Product owner        | Adoption lead    | Possibly; update onboarding or guidance.      |

### 6.6 Pause and rollback decision guide

| Trigger                                  | Possible response                                               |
|------------------------------------------|-----------------------------------------------------------------|
| Confirmed unauthorised data exposure     | Pause affected capability immediately and escalate.             |
| Repeated material wrong answers          | Disable affected question type, domain or metric until fixed.   |
| Cost spike beyond agreed threshold       | Apply usage cap, narrow scope or switch routing if safe.        |
| Data freshness breach on material domain | Add warning, disable affected answers or pause domain.          |
| Support capacity exceeded                | Narrow user group, slow onboarding or increase support cover.   |
| Monitoring unavailable                   | Delay release or pause until minimum observability is restored. |
| Owner unavailable for critical response  | Pause affected release component until ownership is restored.   |

### 6.7 Feedback-to-trace template

| Item               | Description                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| Feedback ID        | Unique user feedback or support ticket reference.                                     |
| User group         | User or group raising the issue.                                                      |
| Original question  | User question or interaction.                                                         |
| Trace ID           | Link to logs / trace.                                                                 |
| Generated query    | Query or tool call, where applicable.                                                 |
| Data assets used   | Source assets, metrics and dimensions.                                                |
| Answer shown       | Answer and caveats shown to the user.                                                 |
| Issue type         | Wrong answer, unclear answer, unsupported question, latency, access, cost, UI, other. |
| Severity           | Low / medium / high / critical.                                                       |
| Owner              | Person or team accountable for response.                                              |
| Response           | Fix, explain, constrain, monitor, defer, escalate.                                    |
| User communication | What was communicated back to the user.                                               |

### 6.8 Early-life support monitoring cadence

| Period              | Recommended cadence            | Focus                                                                            |
|---------------------|--------------------------------|----------------------------------------------------------------------------------|
| First 48 hours      | Daily or twice daily review.   | Access issues, failures, user confusion, cost spikes, major trust issues.        |
| First two weeks     | Daily or every other day.      | Repeated questions, unsupported scope, latency, support burden, onboarding gaps. |
| First month         | Weekly.                        | Trends, cost, issue closure, roadmap candidates, support capacity.               |
| After stabilisation | Monthly or governance cadence. | Adoption, quality, cost, risk, improvement and expansion readiness.              |

### 6.9 Common observability mistakes

| Mistake                                     | Why it matters                                                                            |
|---------------------------------------------|-------------------------------------------------------------------------------------------|
| Monitoring only infrastructure              | T2D failures often sit in semantics, retrieval, caveats, access or interpretation.        |
| No named alert owner                        | Alerts without owners become noise.                                                       |
| Cost review after month-end only            | Cost spikes can occur quickly with broad questions, expensive models or repeated retries. |
| Logs not linked to user feedback            | Support cannot diagnose what happened.                                                    |
| No pause trigger                            | Teams hesitate during incidents because nobody knows when to stop the release.            |
| Dashboards built for the delivery team only | Support, product and owners need operational views they can act on.                       |
| Missing unsupported-question tracking       | Repeated unsupported demand is often the first signal that scope or onboarding is weak.   |

### 6.10 Evidence to retain

- Operational reliability and observability summary.

- Usage, latency, availability, freshness and cost thresholds.

- Monitoring dashboard or log evidence.

- Alert routing and owner matrix.

- Incident severity and escalation guide.

- Pause / rollback decision route.

- Feedback-to-trace evidence.

- Early-life support cadence.

- Operational gaps with release implications.

## 7 Activity 6: Prepare support, documentation, onboarding and controlled adoption readiness

### 7.1 Documentation readiness checklist

| Documentation area  | Readiness question                                                   | Evidence to retain                                 |
|---------------------|----------------------------------------------------------------------|----------------------------------------------------|
| Release boundary    | Does the documentation explain what is in and out of scope?          | Final release boundary, user-facing scope summary. |
| Supported questions | Are supported question types clear and understandable?               | Supported-question guide, examples.                |
| Exclusions          | Are unsupported domains, questions and answer types explicit?        | Exclusion list, refusal examples.                  |
| Known limitations   | Are limitations visible without requiring technical knowledge?       | Known limitations page, onboarding material.       |
| Responsible use     | Do users understand what the system can and cannot be relied on for? | Responsible-use guide.                             |
| Behaviour changes   | Are Phase 8 fixes and behaviour changes documented?                  | Release notes, behaviour-change record.            |
| Support route       | Do users know how to raise issues and where to get help?             | Support route, escalation guide.                   |
| Runbooks            | Can support teams diagnose common issues?                            | Support runbook, incident playbook.                |
| Governance evidence | Can owners defend the release decision and residual risks?           | Approval record, residual-risk log.                |
| Versioning          | Is documentation versioned and aligned to the production release?    | Version history, owner record.                     |
| Maintenance         | Is there an owner and cadence for keeping documentation current?     | Documentation ownership plan.                      |

### 7.2 Documentation set by audience

| Audience                      | Documentation needed                                                                                        | Main purpose                                     |
|-------------------------------|-------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| Users                         | Quick-start guide, supported questions, known limitations, responsible-use guidance, issue-reporting route. | Help users understand what they can rely on.     |
| Support teams                 | Runbook, triage guide, common issues, escalation path, pause / rollback communication.                      | Help support teams diagnose and respond.         |
| Product / delivery owners     | Release notes, backlog, roadmap, behaviour-change record, regression evidence.                              | Manage release, fixes and improvement.           |
| Data / semantic owners        | Approved metrics, caveats, refresh rules, data scope, semantic constraints.                                 | Maintain trusted data and definitions.           |
| Platform / engineering owners | Deployment notes, monitoring dashboards, alert routes, logs, technical dependencies.                        | Operate and maintain the service.                |
| Governance / risk owners      | Release boundary, residual-risk acceptance, access controls, audit evidence, sign-off record.               | Defend the release decision and oversight model. |

### 7.3 User onboarding checklist

| Area               | What users should understand                                                   |
|--------------------|--------------------------------------------------------------------------------|
| Purpose            | What the controlled production release is for.                                 |
| Scope              | Which questions, domains and answer types are supported.                       |
| Limitations        | Which questions are not supported and why.                                     |
| Trust              | How to interpret answers, caveats, clarifications and refusals.                |
| Evidence           | Where sources, caveats or traces are visible, if exposed to users.             |
| Responsible use    | What decisions the system can support and where human review remains required. |
| Feedback           | How to report wrong, unclear, slow or unexpected answers.                      |
| Support            | Who to contact and expected response route.                                    |
| Changes from pilot | What has changed since Phase 7.                                                |
| Roadmap            | What may come later and what is deliberately not included now.                 |

### 7.4 Release notes template

| Item                    | Description                                     |
|-------------------------|-------------------------------------------------|
| Release version         | Version or release identifier.                  |
| Release date            | Planned or actual release date.                 |
| Release objective       | What this release enables.                      |
| Users in scope          | User groups included.                           |
| Data / domains in scope | Domains and assets included.                    |
| Supported questions     | Question types supported.                       |
| Key exclusions          | Questions, users, domains or features excluded. |
| Behaviour changes       | Changes since pilot or previous release.        |
| Fixed issues            | Release-critical issues fixed in Phase 8.       |
| Known limitations       | Remaining limitations users should understand.  |
| Release constraints     | Conditions under which the release is allowed.  |
| Support route           | How users raise issues.                         |
| Owner                   | Product or release owner.                       |

### 7.5 Known limitations template

| Limitation                                | User impact                                     | Required user behaviour                     | Owner                  | Review trigger                |
|-------------------------------------------|-------------------------------------------------|---------------------------------------------|------------------------|-------------------------------|
| Current-month revenue may be provisional. | Answers may change after source refresh.        | Treat current-month figures as indicative.  | Finance data owner     | Month-end close.              |
| Forecasting questions are not supported.  | System will refuse or redirect these questions. | Use existing forecasting process.           | Product owner          | Phase 9 roadmap review.       |
| Customer drill-down limited to analysts.  | Managers may not see customer-level details.    | Ask sales operations for detailed analysis. | Data owner             | Access review complete.       |
| Pipeline data refreshed daily.            | Same-day changes may not appear.                | Use operational CRM for real-time updates.  | Sales operations owner | Refresh improvement approved. |

### 7.6 Support runbook outline

| Section                | Content                                                                                             |
|------------------------|-----------------------------------------------------------------------------------------------------|
| Service overview       | What the released capability does and who uses it.                                                  |
| Release boundary       | Supported users, domains, questions and exclusions.                                                 |
| Common issues          | Wrong answer, unclear answer, refusal, latency, access issue, missing caveat, unsupported question. |
| First checks           | User, question, trace ID, data asset, metric, generated query, answer, caveats, timestamp.          |
| Triage route           | Product, data, semantic, engineering, access, support or governance owner.                          |
| Severity guide         | Low / medium / high / critical with examples.                                                       |
| Escalation path        | Who to contact and when.                                                                            |
| Pause / rollback route | Conditions and decision owner.                                                                      |
| User communication     | How to respond to users during incidents.                                                           |
| Evidence retention     | What must be logged and where.                                                                      |

### 7.7 Controlled adoption readiness plan

| Item                             | Decision                                                                                   |
|----------------------------------|--------------------------------------------------------------------------------------------|
| First production cohort          | Which users are onboarded first.                                                           |
| Onboarding format                | Live session, recording, written guide, office hours, embedded support.                    |
| Onboarding owner                 | Person or team responsible.                                                                |
| Support model during first weeks | Office hours, dedicated channel, service desk, named support owner.                        |
| Feedback route                   | How users report issues or requests.                                                       |
| Adoption signals                 | Usage, repeat usage, unsupported questions, support tickets, satisfaction, trust feedback. |
| Review cadence                   | Daily / weekly / monthly review during early-life period.                                  |
| Expansion condition              | What must be true before more users are added.                                             |

### 7.8 Issue communication examples

| Scenario                          | User-facing communication                                                                                                                                                             |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Unsupported question              | “This question is not supported in the current release. The release currently supports revenue and pipeline questions by region and segment, but not forecasting or margin analysis.” |
| Known data freshness caveat       | “This answer uses daily refreshed pipeline data. Same-day CRM updates may not be reflected.”                                                                                          |
| Incident affecting answer quality | “We have identified an issue affecting answers for current-month revenue. Please do not rely on this answer type until we confirm resolution.”                                        |
| Release constraint                | “Customer-level drill-down is available only to sales operations analysts in this release because access controls are still being reviewed for wider users.”                          |
| Behaviour change after fix        | “Current-month revenue answers now include a provisional-data caveat. This was added to avoid over-reliance before month-end close.”                                                  |

### 7.9 Documentation ownership plan

| Document                 | Owner                      | Review cadence               | Update trigger                                   |
|--------------------------|----------------------------|------------------------------|--------------------------------------------------|
| User guide               | Product owner              | Monthly during early life    | Scope change, user confusion, new limitation.    |
| Known limitations        | Product / data owner       | Weekly during first month    | New caveat, data issue, release constraint.      |
| Support runbook          | Support owner              | Weekly during first month    | New incident, escalation change, repeated issue. |
| Release notes            | Release owner              | Every release                | Fix, behaviour change, scope change.             |
| Responsible-use guide    | Product / governance owner | Quarterly or on major change | Risk change, new user group, new answer type.    |
| Monitoring / alert guide | Platform owner             | Monthly                      | New alert, threshold change, incident learning.  |

### 7.10 Common documentation and onboarding mistakes

| Mistake                                      | Why it matters                                                                         |
|----------------------------------------------|----------------------------------------------------------------------------------------|
| Treating documentation as user guidance only | Support, governance, product and platform teams also need release-ready documentation. |
| Reusing pilot material unchanged             | Pilot documents may not reflect final fixes, constraints or production ownership.      |
| Hiding limitations in technical language     | Users need plain-language boundaries to avoid over-reliance.                           |
| No support route in user material            | Users will escalate informally or stop trusting the system.                            |
| No release notes for behaviour changes       | Users and support teams cannot explain why answers changed.                            |
| No documentation owner                       | Documentation becomes stale as soon as Phase 9 begins.                                 |
| Onboarding too broad                         | Users may assume the system supports more than the controlled release boundary.        |

### 7.11 Evidence to retain

- Production documentation readiness summary.

- User onboarding material.

- Release notes and behaviour-change record.

- Known limitations and responsible-use guidance.

- Support runbook and escalation route.

- Controlled adoption readiness plan.

- Documentation ownership and maintenance plan.

- Evidence that users and support teams were onboarded before access.

## 8 Activity 7: Consolidate operating model, budget and roadmap capacity

### 8.1 Operating model capacity worksheet

| Area                             | Capacity question                                                                    | Evidence / input                                             |
|----------------------------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------|
| Run support                      | Who will handle day-to-day user issues, access questions and service checks?         | Support model, pilot support findings, expected user volume. |
| Bug fixing                       | Who will fix production defects after release?                                       | Phase 8 hardening backlog, unresolved issue list.            |
| Data / semantic maintenance      | Who will maintain metrics, caveats, metadata, refresh rules and data-quality issues? | Data owner sign-off, semantic scope, control gaps.           |
| Platform / engineering           | Who will maintain orchestration, model routing, deployment, logging and monitoring?  | Architecture owner, operational readiness findings.          |
| Monitoring and incident response | Who reviews alerts, investigates incidents and communicates impact?                  | Alert routing, incident process, early-life support plan.    |
| Onboarding and adoption support  | Who supports first users and captures early-life feedback?                           | Onboarding plan, controlled adoption plan.                   |
| Governance and risk review       | Who reviews residual risks, constraints, changes and expansion requests?             | Risk acceptance, governance cadence.                         |
| Roadmap delivery                 | Who delivers approved improvements and expansion?                                    | Phase 9 roadmap, capacity plan.                              |

### 8.2 Run / fix / improve / expand roadmap model

| Lane    | Purpose                                                                   | Typical work                                                                        | Capacity owner                          |
|---------|---------------------------------------------------------------------------|-------------------------------------------------------------------------------------|-----------------------------------------|
| Run     | Keep the live release stable.                                             | Support, access changes, monitoring review, incident response, cost review.         | Support / platform / product.           |
| Fix     | Resolve production defects and known issues.                              | Bug fixes, regression checks, control fixes, documentation corrections.             | Engineering / data / product.           |
| Improve | Make the current release better without expanding scope materially.       | Better onboarding, clearer caveats, better monitoring, answer-quality improvements. | Product / engineering / support.        |
| Expand  | Add new users, domains, questions, integrations or higher-risk use cases. | New data scope, new semantic work, new controls, new validation, broader rollout.   | Product / data / platform / governance. |

### 8.3 Cost and capacity estimate template

| Cost / capacity area            | Estimate | Owner                   | Funding route | Review cadence            | Notes                                            |
|---------------------------------|----------|-------------------------|---------------|---------------------------|--------------------------------------------------|
| Model usage                     |          | Platform / finance      |               | Weekly during early life  | Include expected and threshold usage.            |
| Query / warehouse cost          |          | Data platform           |               | Weekly / monthly          | Include high-cost query risk.                    |
| Infrastructure                  |          | Platform owner          |               | Monthly                   | Hosting, orchestration, storage, networking.     |
| Monitoring and logging          |          | Platform owner          |               | Monthly                   | Dashboards, alerting, log retention.             |
| Support capacity                |          | Support owner           |               | Weekly during early life  | First-line and second-line support.              |
| Engineering fixes               |          | Engineering owner       |               | Weekly                    | Reserved capacity for early defects.             |
| Data / semantic maintenance     |          | Data / semantic owner   |               | Weekly / monthly          | Metric, caveat, metadata and refresh issues.     |
| Onboarding and adoption support |          | Product / adoption lead |               | Weekly during early life  | User guidance, office hours, feedback.           |
| Governance / risk review        |          | Governance owner        |               | Monthly or decision-based | Residual risk, constraints, expansion approvals. |
| Roadmap delivery                |          | Product owner           |               | Monthly / quarterly       | Improvements and expansion.                      |

### 8.4 Capacity reservation template

| Role / team     | Required for                                               | Minimum capacity | Duration | Reserved? | Risk if not reserved                   |
|-----------------|------------------------------------------------------------|------------------|----------|-----------|----------------------------------------|
| Product owner   | Release decisions, prioritisation, user feedback, roadmap  |                  |          | Yes / No  | No clear trade-off owner.              |
| Engineering     | Fixes, regression, orchestration changes, monitoring fixes |                  |          | Yes / No  | Defects remain unresolved.             |
| Data owner      | Data issues, refresh exceptions, source changes            |                  |          | Yes / No  | Data risks remain unowned.             |
| Semantic owner  | Metric, caveat, dimension and definition changes           |                  |          | Yes / No  | Answer trust degrades.                 |
| Support owner   | User support, incident triage, communication               |                  |          | Yes / No  | Users escalate informally.             |
| Platform owner  | Monitoring, cost, reliability, deployment                  |                  |          | Yes / No  | Operational issues are not acted on.   |
| Security / risk | Access issues, risk review, residual-risk decisions        |                  |          | Yes / No  | Control issues delay or block release. |

### 8.5 Roadmap prioritisation guide

| Candidate item                        | Run / fix / improve / expand | Evidence basis                    | Capacity needed              | Cost impact | Decision                               |
|---------------------------------------|------------------------------|-----------------------------------|------------------------------|-------------|----------------------------------------|
| Add missing caveat monitoring         | Fix                          | Phase 8 control gap               | Engineering + product        | Low         | Include before or soon after release.  |
| Add finance users                     | Expand                       | User demand, not yet piloted      | Data + semantic + support    | Medium      | Defer until readiness confirmed.       |
| Improve unsupported-question guidance | Improve                      | Pilot confusion                   | Product / onboarding         | Low         | Include in early Phase 9.              |
| Automate access revocation report     | Improve / control            | Manual access process             | Platform / IAM               | Medium      | Prioritise if release cohort expands.  |
| Add margin analysis                   | Expand                       | High demand but metric unresolved | Data + semantic + validation | High        | Roadmap only after semantic readiness. |

### 8.6 Funding and approval record

| Item                    | Decision                                                        |
|-------------------------|-----------------------------------------------------------------|
| Budget owner            | Named owner accountable for run and change funding.             |
| Approved run budget     | Budget for operating the first release.                         |
| Approved change budget  | Budget for bug fixes, improvements and controlled roadmap work. |
| Cost review cadence     | Weekly / monthly / quarterly.                                   |
| Cost escalation trigger | Threshold that requires review or intervention.                 |
| Capacity owner          | Person accountable for securing required people.                |
| Funding gaps            | Unfunded areas that may constrain release or roadmap.           |
| Release implication     | Proceed, constrain, delay, narrow or stop.                      |

### 8.7 Illustrative example: capacity-aware roadmap

| Lane    | Item                                        | Timing        | Capacity assumption                       | Release implication                  |
|---------|---------------------------------------------|---------------|-------------------------------------------|--------------------------------------|
| Run     | Daily monitoring review for first two weeks | Week 1–2      | Product + platform 30 minutes / day       | Required for release.                |
| Fix     | Resolve missing caveat edge cases           | Week 1        | Engineering 2 days + product review       | Required before release.             |
| Improve | Add better examples to onboarding guide     | Week 2–3      | Product 1 day                             | Can happen after release.            |
| Expand  | Add finance user group                      | Month 2+      | Data, semantic, support and access review | Only after first release stabilises. |
| Expand  | Add margin questions                        | Later roadmap | Metric definition and validation required | Return to semantic readiness first.  |

### 8.8 Common operating-model and budget mistakes

| Mistake                                        | Why it matters                                                                                    |
|------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Treating model cost as the whole cost          | People, monitoring, support, testing, data refresh and governance often cost more than inference. |
| Assuming the delivery team will stay available | Teams often move on before hardening, early-life support and roadmap work are complete.           |
| Funding release but not support                | Users get access, but no one owns issues after go-live.                                           |
| Mixing fixes and enhancements                  | Release-critical defects compete with nice-to-have roadmap items.                                 |
| Expanding before stabilising                   | New users and domains multiply support, cost and trust risks.                                     |
| Ignoring data and semantic capacity            | T2D roadmap expansion usually depends on data and semantic work, not only engineering.            |
| No cost trigger                                | Teams discover cost pressure only after the budget is already exceeded.                           |

### 8.9 Evidence to retain

- Operating model and capacity estimate.

- Run-cost and change-budget view.

- Capacity reservation record.

- Run / fix / improve / expand roadmap.

- Funding and approval record.

- Cost and capacity gap log.

- Roadmap prioritisation record.

- Release implication of any unfunded capacity gaps.

## 9 Activity 8: Approve and execute controlled release, residual-risk acceptance and Phase 9 handover

### 9.1 Controlled release decision record

| Item                              | Decision                                                                                            |
|-----------------------------------|-----------------------------------------------------------------------------------------------------|
| Release decision                  | Release / release with constraints / further hardening / narrow / return / redesign / pause / stop. |
| Decision date                     | Date of decision.                                                                                   |
| Release version                   | Version or release identifier.                                                                      |
| Release boundary                  | Users, domains, questions, answer types and usage limits approved.                                  |
| Main rationale                    | Why this decision is appropriate.                                                                   |
| Conditions                        | Conditions that must remain true for release to proceed.                                            |
| Constraints                       | Scope, user, data, support, cost or monitoring constraints.                                         |
| Release-critical fixes completed? | Yes / no / conditional.                                                                             |
| Residual risks accepted?          | Yes / no / pending.                                                                                 |
| Budget approved?                  | Yes / no / conditional.                                                                             |
| Support accepted?                 | Yes / no / conditional.                                                                             |
| Monitoring active?                | Yes / no / conditional.                                                                             |
| Onboarding complete?              | Yes / no / scheduled.                                                                               |
| Decision owner                    | Accountable owner approving release.                                                                |
| Review date                       | First post-release review date.                                                                     |

### 9.2 Final release approval checklist

| Area             | Release question                                                     | Status | Owner                     |
|------------------|----------------------------------------------------------------------|--------|---------------------------|
| Scope            | Is the final release boundary approved and documented?               |        | Product owner             |
| Fixes            | Are release-critical fixes complete and regression-tested?           |        | Engineering / product     |
| Controls         | Are data, semantic, access, security and audit controls enforceable? |        | Data / security owner     |
| Observability    | Are monitoring, logging, alerting and thresholds active?             |        | Platform owner            |
| Support          | Are runbooks, escalation routes and incident paths ready?            |        | Support owner             |
| Onboarding       | Have first production users been onboarded?                          |        | Product / adoption lead   |
| Cost             | Are run cost, thresholds and budget owner confirmed?                 |        | Finance / platform owner  |
| Residual risk    | Have residual risks been accepted by accountable owners?             |        | Risk / business owner     |
| Change rights    | Are change, expansion, pause and rollback rights clear?              |        | Release owner             |
| Phase 9 handover | Are owners, cadence, backlog and roadmap transferred?                |        | Product / operating owner |

### 9.3 Residual-risk acceptance record

| Risk                                          | Why it remains                                       | Release condition                       | Accountable owner    | Monitoring / control                   | Review trigger                          |
|-----------------------------------------------|------------------------------------------------------|-----------------------------------------|----------------------|----------------------------------------|-----------------------------------------|
| Current-month revenue may be provisional.     | Source refresh cannot be accelerated before release. | Caveat shown in all relevant answers.   | Finance data owner   | Caveat check and freshness monitoring. | Month-end close or caveat failure.      |
| Unsupported questions expected in first week. | Users are still learning release boundary.           | Refusal wording and onboarding updated. | Product owner        | Unsupported-question dashboard.        | Threshold breach or repeated confusion. |
| Manual access review during early life.       | Automation not ready for first release.              | Named owner and weekly review.          | IAM / security owner | Access-change log.                     | Cohort expansion request.               |

### 9.4 Release package contents

| Section                | Content                                                                            |
|------------------------|------------------------------------------------------------------------------------|
| Release decision       | Decision, rationale, date, approvers and conditions.                               |
| Release boundary       | Users, domains, questions, answer types, exclusions and constraints.               |
| Fix evidence           | Completed hardening items and regression evidence.                                 |
| Control evidence       | Data, semantic, access, security, audit and compliance evidence.                   |
| Observability evidence | Monitoring, alerts, logs, thresholds and incident route.                           |
| Support evidence       | Runbooks, escalation paths, support owners and service expectations.               |
| Onboarding evidence    | User guidance, known limitations, responsible-use guidance and communication plan. |
| Cost evidence          | Budget, cost thresholds, review cadence and owner.                                 |
| Risk evidence          | Residual risks, accepted risks, monitored risks and review triggers.               |
| Phase 9 handover       | Owners, cadence, backlog, roadmap and expansion criteria.                          |

### 9.5 Release execution or handover plan

| Step                                | Description                                              | Owner                        | Status |
|-------------------------------------|----------------------------------------------------------|------------------------------|--------|
| Final release approval              | Confirm decision and release conditions.                 | Release owner                |        |
| Production deployment or enablement | Deploy release or enable access for approved users.      | Platform / engineering       |        |
| User access activation              | Add approved users only.                                 | IAM / support                |        |
| Monitoring activation               | Confirm dashboards, alerts and logs are active.          | Platform owner               |        |
| User communication                  | Send release note, scope, limitations and support route. | Product / adoption lead      |        |
| Support readiness check             | Confirm support channel and escalation owners are live.  | Support owner                |        |
| First-day review                    | Review usage, errors, access, cost and user issues.      | Product / platform / support |        |
| Early-life cadence                  | Confirm daily / weekly review rhythm.                    | Operating owner              |        |

### 9.6 Pause, rollback and narrowing authority

| Trigger                              | Possible action                                                | Decision owner           | Communication required |
|--------------------------------------|----------------------------------------------------------------|--------------------------|------------------------|
| Unauthorised data exposure           | Pause affected capability immediately.                         | Security / release owner | Yes                    |
| Repeated material wrong answers      | Disable affected question type or domain.                      | Product / data owner     | Yes                    |
| Cost threshold breach                | Apply usage cap, model-routing change or temporary constraint. | Finance / platform owner | If user impact         |
| Monitoring unavailable               | Delay, pause or narrow release.                                | Platform / release owner | If service affected    |
| Support capacity exceeded            | Slow onboarding, narrow users or increase support cover.       | Support / product owner  | Yes                    |
| Data freshness breach                | Add warning, disable affected domain or pause answers.         | Data / product owner     | Yes                    |
| Owner unavailable for critical issue | Pause affected release area.                                   | Release owner            | If user impact         |

### 9.7 Phase 9 handover template

| Area                    | Handover decision                                                       |
|-------------------------|-------------------------------------------------------------------------|
| Live release boundary   | What is live and what remains excluded.                                 |
| Operating owner         | Owner accountable for the live capability.                              |
| Product owner           | Owner accountable for user value, backlog and roadmap.                  |
| Support owner           | Owner accountable for user support and issue triage.                    |
| Platform owner          | Owner accountable for service reliability, monitoring and cost.         |
| Data / semantic owners  | Owners accountable for data assets, metrics, caveats and refresh rules. |
| Risk / governance owner | Owner accountable for residual-risk review and change governance.       |
| Review cadence          | Daily / weekly / monthly operating rhythm.                              |
| Run backlog             | Items needed to keep the service stable.                                |
| Fix backlog             | Known defects and production issues to resolve.                         |
| Improve backlog         | Improvements to current release experience or controls.                 |
| Expand backlog          | Potential new users, domains, questions or integrations.                |
| Expansion conditions    | What must be true before scope grows.                                   |

### 9.8 Post-release review criteria

| Area        | Review question                                                      |
|-------------|----------------------------------------------------------------------|
| Usage       | Are the right users using the system at the expected level?          |
| Trust       | Are users relying on the answers appropriately?                      |
| Quality     | Are supported questions answered correctly and consistently?         |
| Scope       | Are users repeatedly asking out-of-scope questions?                  |
| Support     | Is support demand manageable?                                        |
| Cost        | Is usage within budget and cost thresholds?                          |
| Reliability | Are latency, failures and incidents within agreed thresholds?        |
| Controls    | Are access, audit, data and semantic controls holding in production? |
| Roadmap     | Should Phase 9 focus on run, fix, improve or expand?                 |

### 9.9 Expansion criteria

- Before adding users, domains, question types or integrations, confirm:

- the first production release is stable enough to absorb more usage;

- known production defects are not blocking trust or support;

- data and semantic readiness exists for the proposed expansion;

- access, security and audit controls can support the wider scope;

- monitoring and cost thresholds can handle additional volume;

- support and onboarding capacity is available;

- residual risks are reviewed and accepted by the right owners;

- the expansion is funded and prioritised against run, fix and improve work.

### 9.10 Common release approval mistakes

| Mistake                             | Why it matters                                                                      |
|-------------------------------------|-------------------------------------------------------------------------------------|
| Treating release as a ceremony      | The decision must record scope, risks, owners and conditions.                       |
| Accepting residual risk informally  | Risk acceptance needs accountable ownership, not project-team acknowledgement.      |
| Releasing before support is live    | Users will escalate informally or lose trust.                                       |
| No pause authority                  | Teams hesitate during incidents because nobody can stop or narrow the release.      |
| Handover without budget             | Phase 9 starts with responsibility but no capacity.                                 |
| Expanding immediately after go-live | Early demand can hide unresolved support, cost or control issues.                   |
| Losing the release boundary         | Users and stakeholders start treating a controlled release as general availability. |

### 9.11 Evidence to retain

- Controlled release decision record.

- Final release approval checklist.

- Residual-risk acceptance records.

- Final release package.

- Release execution or handover plan.

- Pause, rollback and narrowing authority.

- Phase 9 handover record.

- Post-release review criteria.

- Expansion criteria and first review date.

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
