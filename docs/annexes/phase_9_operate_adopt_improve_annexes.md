# Talk-to-Data Delivery Blueprint — Phase 9 Annexes: Operate, Adopt & Improve

*Daniel Brule · Talk-to-Data Delivery Blueprint · v1.0 · June 2026*

---

**Table of contents**

- [1 How to use this annex](#1-how-to-use-this-annex)
- [2 Activity 1: Activate early-life support and operating cadence](#2-activity-1-activate-early-life-support-and-operating-cadence)
  - [2.1 Early-life operating start checklist](#21-early-life-operating-start-checklist)
  - [2.2 Early-life operating cadence template](#22-early-life-operating-cadence-template)
  - [2.3 Early-life signal review checklist](#23-early-life-signal-review-checklist)
  - [2.4 Upstream change review route](#24-upstream-change-review-route)
  - [2.5 Pause, rollback and narrowing trigger examples](#25-pause-rollback-and-narrowing-trigger-examples)
  - [2.6 Transition to stable operation criteria](#26-transition-to-stable-operation-criteria)
  - [2.7 First operating review agenda](#27-first-operating-review-agenda)
  - [2.8 Common mistakes to avoid](#28-common-mistakes-to-avoid)
  - [2.9 Evidence to retain](#29-evidence-to-retain)
- [3 Activity 2: Monitor production usage, quality, trust, reliability and cost](#3-activity-2-monitor-production-usage-quality-trust-reliability-and-cost)
  - [3.1 Production monitoring view](#31-production-monitoring-view)
  - [3.2 Monitoring threshold template](#32-monitoring-threshold-template)
  - [3.3 Unsupported-question log](#33-unsupported-question-log)
  - [3.4 Trust and interpretation check](#34-trust-and-interpretation-check)
  - [3.5 Monitoring review agenda](#35-monitoring-review-agenda)
  - [3.6 Evidence to retain](#36-evidence-to-retain)
- [4 Activity 3: Manage incidents, support requests and feedback-to-trace diagnosis](#4-activity-3-manage-incidents-support-requests-and-feedback-to-trace-diagnosis)
  - [4.1 Incident, support and feedback log](#41-incident-support-and-feedback-log)
  - [4.2 Feedback-to-trace register](#42-feedback-to-trace-register)
  - [4.3 Root-cause classification guide](#43-root-cause-classification-guide)
  - [4.4 T2D versus upstream fix decision](#44-t2d-versus-upstream-fix-decision)
  - [4.5 Communication note template](#45-communication-note-template)
  - [4.6 Evidence to retain](#46-evidence-to-retain)
- [5 Activity 4: Maintain access lifecycle and protect the release boundary](#5-activity-4-maintain-access-lifecycle-and-protect-the-release-boundary)
  - [5.1 Access lifecycle log](#51-access-lifecycle-log)
  - [5.2 Release boundary exception log](#52-release-boundary-exception-log)
  - [5.3 Temporary shortcut register](#53-temporary-shortcut-register)
  - [5.4 Boundary review checklist](#54-boundary-review-checklist)
  - [5.5 Evidence to retain](#55-evidence-to-retain)
- [6 Activity 5: Run live governance, residual-risk and decision-rights cadence](#6-activity-5-run-live-governance-residual-risk-and-decision-rights-cadence)
  - [6.1 Live governance cadence](#61-live-governance-cadence)
  - [6.2 Decision-rights matrix](#62-decision-rights-matrix)
  - [6.3 Residual-risk review log](#63-residual-risk-review-log)
  - [6.4 Upstream change impact record](#64-upstream-change-impact-record)
  - [6.5 Governance review agenda](#65-governance-review-agenda)
  - [6.6 Evidence to retain](#66-evidence-to-retain)
- [7 Activity 6: Maintain BAU service, data, semantic, metadata and documentation](#7-activity-6-maintain-bau-service-data-semantic-metadata-and-documentation)
  - [7.1 Automated BAU check register](#71-automated-bau-check-register)
  - [7.2 Upstream change impact checklist](#72-upstream-change-impact-checklist)
  - [7.3 Currency update log](#73-currency-update-log)
  - [7.4 Human review prompt](#74-human-review-prompt)
  - [7.5 User check-in guide](#75-user-check-in-guide)
  - [7.6 BAU regression check trigger](#76-bau-regression-check-trigger)
  - [7.7 Evidence to retain](#77-evidence-to-retain)
- [8 Activity 7: Manage the run / fix / improve / expand backlog and capacity](#8-activity-7-manage-the-run-fix-improve-expand-backlog-and-capacity)
  - [8.1 Backlog classification guide](#81-backlog-classification-guide)
  - [8.2 Run / fix / improve / expand backlog](#82-run-fix-improve-expand-backlog)
  - [8.3 Ownership and dependency check](#83-ownership-and-dependency-check)
  - [8.4 Adjacent-needs routing log](#84-adjacent-needs-routing-log)
  - [8.5 Capacity view](#85-capacity-view)
  - [8.6 Prioritisation questions](#86-prioritisation-questions)
  - [8.7 Evidence to retain](#87-evidence-to-retain)
- [9 Activity 8: Control service development, regression testing and version deployment](#9-activity-8-control-service-development-regression-testing-and-version-deployment)
  - [9.1 Change intake record](#91-change-intake-record)
  - [9.2 Change impact checklist](#92-change-impact-checklist)
  - [9.3 Model review record](#93-model-review-record)
  - [9.4 Regression checklist](#94-regression-checklist)
  - [9.5 Version and release record](#95-version-and-release-record)
  - [9.6 Post-release review](#96-post-release-review)
  - [9.7 Evidence to retain](#97-evidence-to-retain)
- [10 Activity 9: Drive controlled adoption and responsible use within approved scope](#10-activity-9-drive-controlled-adoption-and-responsible-use-within-approved-scope)
  - [10.1 User onboarding checklist](#101-user-onboarding-checklist)
  - [10.2 Representative user check-in guide](#102-representative-user-check-in-guide)
  - [10.3 Responsible-use issue log](#103-responsible-use-issue-log)
  - [10.4 Adoption signal summary](#104-adoption-signal-summary)
  - [10.5 Scope reminder template](#105-scope-reminder-template)
  - [10.6 Evidence to retain](#106-evidence-to-retain)
- [11 Activity 10: Manage lifecycle, retirement and decommissioning readiness](#11-activity-10-manage-lifecycle-retirement-and-decommissioning-readiness)
  - [11.1 Lifecycle review checklist](#111-lifecycle-review-checklist)
  - [11.2 Lifecycle action guide](#112-lifecycle-action-guide)
  - [11.3 Retirement or decommissioning decision record](#113-retirement-or-decommissioning-decision-record)
  - [11.4 Decommissioning action checklist](#114-decommissioning-action-checklist)
  - [11.5 Evidence to retain](#115-evidence-to-retain)

---

## 1 How to use this annex

These annexes provide optional working templates for Phase 9: Operate, adopt and improve. They are intended to help teams run a controlled T2D production release, monitor real usage, manage incidents, govern change, improve safely and prepare for longer-term lifecycle decisions.

The templates are not all mandatory. Teams should select the artefacts that match the release scope, risk level, user population, data sensitivity and operating maturity of the service.

For a narrow internal release, a lightweight operating cadence, issue log and change record may be sufficient. For a broader, decision-critical or regulated release, monitoring, feedback-to-trace analysis, governance, access lifecycle, regression evidence, cost review and retirement planning should be treated more formally.

The annexes should support operation, not create bureaucracy. If a template does not help the team run, control, improve or safely stop the service, it should be simplified or skipped.

## 2 Activity 1: Activate early-life support and operating cadence

### 2.1 Early-life operating start checklist

Purpose: confirm that the service is ready to be operated after controlled release.

| Area                  | Confirmation question                                           | Status | Owner | Evidence / note |
|-----------------------|-----------------------------------------------------------------|--------|-------|-----------------|
| Release boundary      | Is the approved Phase 8 boundary understood?                    |        |       |                 |
| Known limitations     | Are limitations visible to users and support teams?             |        |       |                 |
| Support route         | Is the first-line support route active?                         |        |       |                 |
| Escalation route      | Are technical, data, semantic and security escalations clear?   |        |       |                 |
| Monitoring            | Are usage, quality, cost, latency and incident signals visible? |        |       |                 |
| Runbooks              | Are support and operator runbooks available?                    |        |       |                 |
| Access lifecycle      | Are onboarding, offboarding and role-change routes active?      |        |       |                 |
| Pause authority       | Is the pause, rollback or narrowing authority confirmed?        |        |       |                 |
| Governance cadence    | Are operating and governance reviews scheduled?                 |        |       |                 |
| Upstream change route | Is the upstream change check active?                            |        |       |                 |

Suggested status values: Ready / Ready with caveat / Gap / Blocked / Not applicable.

### 2.2 Early-life operating cadence template

| Item                         | Decision                                                                                 |
|------------------------------|------------------------------------------------------------------------------------------|
| Early-life support period    | Duration and review points.                                                              |
| Daily check owner            | Person or team reviewing live signals.                                                   |
| Weekly operating review      | Forum, attendees and agenda.                                                             |
| Governance review            | Forum for risk, cost, change and boundary decisions.                                     |
| Support channel              | Where users raise questions or issues.                                                   |
| Escalation route             | Route for incidents, data issues, semantic issues, access issues and misleading answers. |
| Monitoring dashboard         | Location of dashboard or evidence source.                                                |
| Issue triage route           | How issues are classified and assigned.                                                  |
| User communication route     | How users are informed of incidents, fixes or behaviour changes.                         |
| Stable-operation review date | Date when early-life support can be reduced or extended.                                 |

### 2.3 Early-life signal review checklist

| Signal                      | Review question                                                  | Typical owner                      |
|-----------------------------|------------------------------------------------------------------|------------------------------------|
| Usage                       | Are users using the service as expected?                         | Product / operating owner          |
| Unsupported questions       | Are users asking outside the approved scope?                     | Product / semantic owner           |
| Answer quality              | Are answers correct, caveated and understandable?                | Product / evaluation owner         |
| Refusals and clarifications | Are refusals and clarifications appropriate?                     | AI / product owner                 |
| Incidents                   | Are incidents handled within the expected route?                 | Operating / support owner          |
| Access issues               | Are users seeing only what they are allowed to see?              | Security / access owner            |
| Latency                     | Are response times within expected limits?                       | Platform / AI owner                |
| Cost                        | Are model, query and support costs within the expected envelope? | Product / finance / platform owner |
| Support load                | Is the support burden sustainable?                               | Support / operating owner          |
| User feedback               | Is feedback trace-linked and diagnosable?                        | Product / support owner            |

### 2.4 Upstream change review route

Purpose: detect changes in the analytical flow before they affect live T2D behaviour.

| Upstream area        | Change to watch                                           | T2D impact to assess                             | Owner                   |
|----------------------|-----------------------------------------------------------|--------------------------------------------------|-------------------------|
| Data ingestion       | Source, refresh, pipeline or schema change                | Missing, stale or inconsistent answers           | Data engineering        |
| Data modelling       | Table, view, join, grain or aggregation change            | Wrong query path or changed result               | Data modelling owner    |
| Semantic definitions | Metric, dimension, filter or caveat change                | Changed answer meaning                           | Semantic / metric owner |
| Metadata             | Catalogue, glossary, lineage or examples change           | Retrieval or grounding degradation               | Metadata owner          |
| Access rules         | Role, row, column, masking or aggregation policy change   | Exposure or refusal behaviour                    | Security / access owner |
| Reporting logic      | Dashboard or certified report change                      | Reconciliation mismatch                          | BI / reporting owner    |
| Platform             | Warehouse, model gateway, logging or orchestration change | Latency, cost, reliability or traceability issue | Platform owner          |

### 2.5 Pause, rollback and narrowing trigger examples

| Trigger                                         | Possible response                                        |
|-------------------------------------------------|----------------------------------------------------------|
| Incorrect access enforcement                    | Pause affected users or scope immediately.               |
| Materially misleading answer in supported scope | Pause affected question type and investigate root cause. |
| Missing or broken audit trace                   | Pause affected flow until traceability is restored.      |
| Cost spike beyond threshold                     | Constrain usage, model route or query pattern.           |
| Repeated unsupported use                        | Update guidance, constrain scope or review adoption.     |
| Upstream semantic change without T2D review     | Pause affected metric until retested.                    |
| Model or prompt change degrades behaviour       | Roll back to previous approved version.                  |

### 2.6 Transition to stable operation criteria

| Criterion       | Stable-operation expectation                                   |
|-----------------|----------------------------------------------------------------|
| Usage           | Usage pattern is understood and within expected scope.         |
| Incidents       | No unresolved blocking or recurring material incidents.        |
| Support         | Support route works without exceptional project-team effort.   |
| Access          | Onboarding, offboarding and role changes are controlled.       |
| Quality         | Answer-quality issues are visible, triaged and owned.          |
| Cost            | Cost and latency are understood and within agreed tolerance.   |
| Governance      | Change, risk and boundary decisions have an active forum.      |
| Upstream change | Upstream owners are engaged and material changes are reviewed. |

### 2.7 First operating review agenda

- Review usage, incidents, cost, latency and support signals.

- Review unsupported questions and user feedback.

- Review answer-quality or trust concerns.

- Review access changes and exceptions.

- Review upstream data, semantic, metadata, access or platform changes.

- Confirm fixes, constraints, communications or escalations required.

- Confirm whether early-life support remains adequate.

- Update issue log, decision log and next review actions.

### 2.8 Common mistakes to avoid

| Mistake                                            | Why it matters                                                         |
|----------------------------------------------------|------------------------------------------------------------------------|
| Assuming release approval means operation is ready | Phase 9 must test whether the operating model works in real use.       |
| Leaving support with the build team informally     | This hides the true operating cost and support model.                  |
| Reviewing usage without quality, trust or cost     | High usage can still create risk or unsustainable cost.                |
| Ignoring upstream changes                          | T2D behaviour can change even when the application has not changed.    |
| No pause or rollback owner                         | The team may be unable to act quickly when trust or access is at risk. |
| Treating early-life support as permanent           | The service should transition to stable operation or be redesigned.    |

### 2.9 Evidence to retain

- Operating start checklist.

- Early-life support plan.

- Named owner and escalation route.

- Monitoring dashboard or signal extract.

- Early-life issue and decision log.

- Upstream change review notes.

- Pause, rollback or narrowing decisions.

- First operating review minutes.

- Stable-operation transition decision.

## 3 Activity 2: Monitor production usage, quality, trust, reliability and cost

### 3.1 Production monitoring view

Purpose: define the minimum monitoring view needed to operate the live T2D service.

| Area        | Signals to review                                          | Owner                      | Review cadence        |
|-------------|------------------------------------------------------------|----------------------------|-----------------------|
| Usage       | Active users, question volume, follow-up depth, peak usage | Product / operating owner  | Weekly                |
| Scope       | Supported, unsupported and ambiguous questions             | Product / semantic owner   | Weekly                |
| Quality     | Failed answers, weak grounding, missing caveats, refusals  | Product / evaluation owner | Weekly                |
| Trust       | Over-reliance, misunderstood caveats, inappropriate use    | Product / adoption owner   | Fortnightly / monthly |
| Reliability | Errors, timeouts, failed tool calls, availability          | Platform / AI owner        | Daily / weekly        |
| Cost        | Model calls, query execution, logging, support effort      | Product / platform owner   | Weekly / monthly      |
| Access      | Denied access, permission issues, exposure concerns        | Security / access owner    | Weekly                |

### 3.2 Monitoring threshold template

| Signal                    | Expected range | Review trigger | Action owner | Response                                    |
|---------------------------|----------------|----------------|--------------|---------------------------------------------|
| Unsupported questions     |                |                |              | Update guidance / backlog / constrain scope |
| Failed answers            |                |                |              | Investigate and fix                         |
| High-latency interactions |                |                |              | Review routing, query or model pattern      |
| Cost per interaction      |                |                |              | Review model, query or follow-up behaviour  |
| Repeated rephrasing       |                |                |              | Review answer clarity or user guidance      |
| Access issue              |                |                |              | Escalate to access owner                    |
| Trust concern             |                |                |              | Follow up with user / review guidance       |

### 3.3 Unsupported-question log

| Date | User group | Question type | Example question | Reason unsupported                                                                      | Suggested route                                       |
|------|------------|---------------|------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------|
|      |            |               |                  | Data not ready / metric undefined / access issue / outside scope / higher-risk use case | Guidance / fix / improve / expand / separate use case |

Purpose: distinguish real demand from unsafe scope creep. Unsupported questions may reveal useful needs, but they should not automatically become part of the live T2D service.

### 3.4 Trust and interpretation check

Purpose: capture signals that are unlikely to appear clearly in logs.

| Check                                       | Evidence source                     | Concern found? | Action                             |
|---------------------------------------------|-------------------------------------|----------------|------------------------------------|
| Do users understand caveats?                | Feedback / interview / support call |                | Update answer wording or guidance  |
| Are users over-trusting answers?            | User follow-up / workflow review    |                | Reinforce responsible-use guidance |
| Are outputs used outside intended workflow? | User discussion / support review    |                | Clarify usage boundary             |
| Are refusals understood?                    | Feedback / support tickets          |                | Improve refusal wording            |
| Are users repeatedly rephrasing?            | Logs + user follow-up               |                | Review answer clarity or scope     |

### 3.5 Monitoring review agenda

- Review usage, cost, latency and reliability signals.

- Review unsupported questions and out-of-scope demand.

- Review answer-quality and trust concerns.

- Review access or exposure issues.

- Identify items for run, fix, improve, expand or constrain.

- Confirm owners and next actions.

### 3.6 Evidence to retain

- Monitoring dashboard or signal extract.

- Unsupported-question log.

- Threshold breach record.

- High-cost or high-latency review.

- Trust and interpretation check notes.

- Actions routed into the run / fix / improve / expand backlog.

## 4 Activity 3: Manage incidents, support requests and feedback-to-trace diagnosis

### 4.1 Incident, support and feedback log

Purpose: capture live issues in a structured way before diagnosis.

| Date | Source                        | User group | Issue summary | Severity                       | Owner | Status                      |
|------|-------------------------------|------------|---------------|--------------------------------|-------|-----------------------------|
|      | Incident / support / feedback |            |               | Low / Medium / High / Critical |       | Open / In progress / Closed |

### 4.2 Feedback-to-trace register

Purpose: link user-reported issues to the evidence needed for diagnosis.

| Issue | Question type | Trace / session ID | Answer output | Data asset | Model / prompt version | Initial diagnosis |
|-------|---------------|--------------------|---------------|------------|------------------------|-------------------|
|       |               |                    |               |            |                        |                   |

### 4.3 Root-cause classification guide

| Root cause      | Typical example                               | Likely owner            |
|-----------------|-----------------------------------------------|-------------------------|
| User guidance   | User asked outside scope or ignored caveat    | Product / adoption      |
| Data            | Missing, stale or incorrect data              | Data owner              |
| Modelling       | Wrong grain, join or aggregation              | Data modelling owner    |
| Semantics       | Metric, dimension or caveat unclear           | Semantic owner          |
| Metadata        | Wrong or missing retrieval context            | Metadata owner          |
| Access          | Permission or exposure issue                  | Security / access       |
| Orchestration   | Wrong routing, tool use or context handling   | AI / solution architect |
| Model behaviour | Poor reasoning, overstatement or weak refusal | AI owner                |
| UI / experience | Output unclear or misleading                  | Product / UX            |
| Cost / latency  | Expensive or slow interaction pattern         | Platform / AI           |
| Support process | Escalation or ownership unclear               | Operating owner         |

### 4.4 T2D versus upstream fix decision

Purpose: avoid patching the symptom in the wrong layer.

| Question                                                                               | Decision                                           |
|----------------------------------------------------------------------------------------|----------------------------------------------------|
| Is the issue caused by answer wording, prompt behaviour, clarification or UI guidance? | Likely T2D-layer fix.                              |
| Is the issue caused by data, modelling, metric definition, metadata or access rules?   | Likely upstream fix.                               |
| Is a temporary T2D constraint needed while upstream fix is pending?                    | Constrain, caveat, pause or refuse affected scope. |
| Does the fix change production behaviour?                                              | Trigger regression test and change record.         |

### 4.5 Communication note template

| Item             | Content                                                                      |
|------------------|------------------------------------------------------------------------------|
| Issue summary    | What happened, in plain language.                                            |
| Affected scope   | Users, questions, metrics, domains or answer types affected.                 |
| User action      | Continue use / verify answers / avoid affected scope / wait for fix.         |
| Resolution       | Fix applied, constraint added, upstream remediation pending or issue closed. |
| Behaviour change | Any change users or support teams should notice.                             |

### 4.6 Evidence to retain

- Incident, support and feedback log.

- Feedback-to-trace register.

- Root-cause classification.

- T2D versus upstream fix decision.

- Escalation and ownership record.

- User or support communication note.

- Regression or retest evidence where behaviour changed.

## 5 Activity 4: Maintain access lifecycle and protect the release boundary

### 5.1 Access lifecycle log

Purpose: track user access changes after release.

| Date | User / group | Change                                 | Reason | Approved by | Status                                 |
|------|--------------|----------------------------------------|--------|-------------|----------------------------------------|
|      |              | Add / remove / role change / exception |        |             | Open / approved / rejected / completed |

### 5.2 Release boundary exception log

Purpose: capture where usage starts to drift beyond the approved boundary.

| Date | Exception                                        | Source                      | Risk                | Decision                                          | Owner |
|------|--------------------------------------------------|-----------------------------|---------------------|---------------------------------------------------|-------|
|      | New user / question / domain / export / workflow | User / support / monitoring | Low / medium / high | Allow temporarily / constrain / reject / escalate |       |

### 5.3 Temporary shortcut register

Purpose: allow small-cohort adoption shortcuts without letting them become permanent.

| Shortcut          | Why allowed             | Risk                        | Expiry / review date | Owner | Final decision           |
|-------------------|-------------------------|-----------------------------|----------------------|-------|--------------------------|
| Manual onboarding | Speed up early adoption | Access process not scalable |                      |       | Formalise / fix / remove |

Suggested rule: any shortcut must be visible, time-bound, owned and reviewed.

### 5.4 Boundary review checklist

| Check      | Question                                                        |
|------------|-----------------------------------------------------------------|
| Users      | Are all active users inside the approved release group?         |
| Roles      | Do roles still match the approved access model?                 |
| Questions  | Are users staying within supported question types?              |
| Data       | Are only approved domains, assets, metrics and dimensions used? |
| Exports    | Are answers being reused only in approved workflows?            |
| Exceptions | Are temporary shortcuts still justified?                        |
| Drift      | Is repeated support creating informal scope expansion?          |

### 5.5 Evidence to retain

- Access lifecycle log.

- Approved user and role list.

- Boundary exception log.

- Temporary shortcut register.

- Access or exposure issue records.

- Boundary change decisions.

- Updated user guidance where needed.

## 6 Activity 5: Run live governance, residual-risk and decision-rights cadence

### 6.1 Live governance cadence

Purpose: define how often governance reviews are held and who attends.

| Review                  | Typical cadence      | Core attendees                                          | Focus                                               |
|-------------------------|----------------------|---------------------------------------------------------|-----------------------------------------------------|
| Early adoption review   | Weekly / fortnightly | Product, operating, support, AI, data, semantic, access | Usage, incidents, risks, fixes, adoption            |
| Stable operation review | Monthly / quarterly  | Product, operating, platform, governance                | Service health, cost, backlog, change               |
| Material change review  | As needed            | Relevant owners                                         | Scope, model, data, semantic, access or risk change |
| Lifecycle review        | Periodic             | Sponsor, product, governance, finance                   | Continue, expand, constrain, retire or decommission |

### 6.2 Decision-rights matrix

| Decision                     | Typical owner / forum        | Evidence required                                   |
|------------------------------|------------------------------|-----------------------------------------------------|
| Minor fix                    | Product / technical owner    | Issue record, test evidence                         |
| Material behaviour change    | Governance forum             | Impact assessment, regression evidence              |
| Model or routing change      | AI owner + governance        | Evaluation, cost, latency and quality comparison    |
| Boundary change              | Product owner + governance   | Value, risk, capacity and control evidence          |
| Access exception             | Access owner                 | User need, approval, expiry date                    |
| Pause or rollback            | Operating owner / risk owner | Incident, risk or degradation evidence              |
| Expansion                    | Sponsor / governance forum   | Production evidence, funding, support and readiness |
| Retirement / decommissioning | Sponsor / governance forum   | Value, cost, usage, risk and replacement assessment |

### 6.3 Residual-risk review log

| Risk | Accepted condition | Current signal | Still acceptable?  | Action                                     |
|------|--------------------|----------------|--------------------|--------------------------------------------|
|      |                    |                | Yes / No / Monitor | Continue / mitigate / constrain / escalate |

### 6.4 Upstream change impact record

Purpose: capture upstream changes before they affect live T2D behaviour.

| Change                                                          | Upstream owner | Potential T2D impact                                         | Review decision                                         | Action owner |
|-----------------------------------------------------------------|----------------|--------------------------------------------------------------|---------------------------------------------------------|--------------|
| Metric update / schema change / access change / platform change |                | Answer, caveat, access, cost, latency or traceability impact | No impact / test / constrain / deploy update / escalate |              |

### 6.5 Governance review agenda

- Review service health, incidents, cost and support load.

- Review residual risks and any threshold breaches.

- Review upcoming upstream changes.

- Review material fixes, model changes or boundary requests.

- Confirm decisions, owners and evidence required.

- Escalate structural issues to the right owner or earlier phase.

- Update decision log and next review actions.

### 6.6 Evidence to retain

- Governance attendance and review notes.

- Residual-risk review log.

- Decision-rights matrix.

- Material change and boundary decision log.

- Upstream change impact records.

- Pause, rollback, expansion or lifecycle decisions.

## 7 Activity 6: Maintain BAU service, data, semantic, metadata and documentation

### 7.1 Automated BAU check register

Purpose: track routine checks that protect the live T2D service from upstream drift.

| Check           | What is tested                                           | Frequency | Owner | Alert route |
|-----------------|----------------------------------------------------------|-----------|-------|-------------|
| Freshness       | Source refreshed within expected window                  |           |       |             |
| Schema / format | Tables, columns and data types unchanged                 |           |       |             |
| Volume          | Row counts and volumes within expected range             |           |       |             |
| Quality         | Nulls, duplicates, completeness, reconciliation          |           |       |             |
| Access          | Row, column, masking and role rules still apply          |           |       |             |
| Metadata        | Required metric, dimension and caveat metadata available |           |       |             |

### 7.2 Upstream change impact checklist

Purpose: assess whether an upstream change affects live T2D behaviour.

| Change area             | Impact question                                           | Action                               |
|-------------------------|-----------------------------------------------------------|--------------------------------------|
| Data source             | Does the change affect freshness, coverage or quality?    | No action / test / update / escalate |
| Data model              | Does the change affect grain, joins or aggregation?       | No action / test / update / escalate |
| Metric / semantic logic | Does the change affect meaning, filters or caveats?       | No action / test / update / escalate |
| Metadata                | Does the change affect retrieval, grounding or examples?  | No action / test / update / escalate |
| Access                  | Does the change affect visibility, refusal or exposure?   | No action / test / update / escalate |
| Reporting logic         | Does the change affect reconciliation to trusted outputs? | No action / test / update / escalate |

### 7.3 Currency update log

| Date | Asset / artefact                                            | Change | User impact                   | Owner | Status                        |
|------|-------------------------------------------------------------|--------|-------------------------------|-------|-------------------------------|
|      | Metric / dimension / caveat / metadata / guidance / runbook |        | None / internal / user-facing |       | Open / updated / communicated |

### 7.4 Human review prompt

Purpose: capture judgement-based checks that automation will not reliably detect.

| Question                                                         | Review note |
|------------------------------------------------------------------|-------------|
| Is the metric still business-appropriate?                        |             |
| Is the caveat still understandable to users?                     |             |
| Could users misinterpret the answer after this change?           |             |
| Does the anomaly reflect a real business movement or data issue? |             |
| Should user guidance or support material be updated?             |             |

### 7.5 User check-in guide

Purpose: validate interpretation and usefulness with users.

| Topic          | Question                                                      |
|----------------|---------------------------------------------------------------|
| Caveats        | Are limitations clear when you read the answer?               |
| Trust          | Do you know when to rely on the answer and when to verify it? |
| Interpretation | Have any answers been confusing or misleading?                |
| Workflow       | Are you using outputs in the intended workflow?               |
| Gaps           | Are there repeated questions the service cannot answer?       |

This can be done through structured focus groups, but informal check-ins with representatives of key user groups are often enough.

### 7.6 BAU regression check trigger

| Trigger                             | Regression needed?                         |
|-------------------------------------|--------------------------------------------|
| Source schema, grain or join change | Usually yes                                |
| Metric, filter or caveat change     | Yes                                        |
| Metadata or example update          | Yes if retrieval or grounding may change   |
| Access-rule change                  | Yes                                        |
| Documentation-only wording change   | Only if user-facing interpretation changes |

### 7.7 Evidence to retain

- Automated BAU check results.

- Upstream change impact checklist.

- Currency update log.

- Human review notes.

- User check-in notes.

- BAU regression check results.

- Updated guidance, caveats, metadata or support material.

## 8 Activity 7: Manage the run / fix / improve / expand backlog and capacity

### 8.1 Backlog classification guide

Purpose: separate different types of work before prioritisation.

| Type      | Meaning                                                    | Typical route           |
|-----------|------------------------------------------------------------|-------------------------|
| Run       | Normal support, monitoring, access or documentation work   | Operating cadence       |
| Fix       | Defect, incident, access issue or answer-quality failure   | Fix and retest          |
| Optimise  | Cost, latency, routing or support-effort reduction         | Prioritised improvement |
| Improve   | Better usability, caveats, guidance or answer format       | Product backlog         |
| Expand    | New users, domains, questions, data assets or integrations | Expansion governance    |
| Constrain | Reduce scope, usage or access to protect trust or cost     | Governance decision     |
| Defer     | Useful but not justified or resourced now                  | Roadmap / later review  |

### 8.2 Run / fix / improve / expand backlog

| Item | Source                                                       | Type                                                        | Owner | Priority            | Capacity need | Decision                       |
|------|--------------------------------------------------------------|-------------------------------------------------------------|-------|---------------------|---------------|--------------------------------|
|      | Monitoring / incident / feedback / governance / user request | Run / fix / optimise / improve / expand / constrain / defer |       | High / medium / low |               | Do / defer / reject / escalate |

### 8.3 Ownership and dependency check

| Question                                                                                | Answer             |
|-----------------------------------------------------------------------------------------|--------------------|
| Does the item belong in the current T2D service?                                        | Yes / No / unclear |
| Is it caused by upstream data, semantic, metadata, access or platform issue?            |                    |
| Does it require product, data, semantic, AI, platform, security or governance capacity? |                    |
| Is funding or dedicated capacity required?                                              |                    |
| Does it require controlled change and deployment?                                       |                    |
| Does it require expansion approval?                                                     |                    |

### 8.4 Adjacent-needs routing log

Purpose: capture needs revealed by T2D without absorbing them automatically.

| Need identified | Evidence                                                               | Best route                                                                                     | Owner | Decision |
|-----------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|-------|----------|
|                 | User feedback / unsupported questions / support pattern / workflow gap | Current T2D / new T2D / dashboard / data fix / semantic work / workflow change / other product |       |          |

### 8.5 Capacity view

| Capacity area         | Current demand | Available capacity | Gap / risk |
|-----------------------|----------------|--------------------|------------|
| Product               |                |                    |            |
| Support               |                |                    |            |
| Engineering           |                |                    |            |
| Data                  |                |                    |            |
| Semantic / metadata   |                |                    |            |
| AI / orchestration    |                |                    |            |
| Platform              |                |                    |            |
| Governance / security |                |                    |            |

### 8.6 Prioritisation questions

- Is this needed to keep the current release safe and trusted?

- Does it fix a defect or improve an already-approved scope?

- Does it reduce cost, latency or support load?

- Does it create new scope or exposure?

- Is the required owner and capacity available?

- What happens if the item is not done now?

### 8.7 Evidence to retain

- Classified backlog.

- Ownership and dependency check.

- Capacity view.

- Adjacent-needs routing log.

- Expansion candidate list.

- Prioritisation and decision notes.

## 9 Activity 8: Control service development, regression testing and version deployment

### 9.1 Change intake record

Purpose: confirm that each change has an approved route before development starts.

| Change | Source                                    | Type                                             | Approval route                 | Owner | Status                         |
|--------|-------------------------------------------|--------------------------------------------------|--------------------------------|-------|--------------------------------|
|        | Backlog / incident / governance / hot fix | Code / prompt / model / UI / config / monitoring | Backlog / governance / hot fix |       | Proposed / approved / rejected |

### 9.2 Change impact checklist

| Impact area    | Question                                                                |
|----------------|-------------------------------------------------------------------------|
| Answers        | Could the change alter answer wording, caveats, refusals or confidence? |
| Retrieval      | Could it affect metadata retrieval or grounding?                        |
| Access         | Could it affect what users can see or ask?                              |
| Cost / latency | Could it change model calls, query cost or response time?               |
| Support        | Do support teams need updated guidance?                                 |
| Auditability   | Are traces, logs and versions still captured?                           |
| Users          | Does the change need release notes or user communication?               |

### 9.3 Model review record

Purpose: assess whether model, routing or inference changes are justified.

| Option reviewed                                               | Expected benefit                                 | Risk                                                       | Evidence needed                     | Decision                    |
|---------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------|-------------------------------------|-----------------------------|
| New model / smaller model / specialist model / routing change | Quality / cost / latency / reliability / control | Behaviour change / weaker reasoning / refusals / grounding | Evaluation / regression / cost test | Use / reject / test further |

### 9.4 Regression checklist

| Test area                   | Required? | Result      |
|-----------------------------|-----------|-------------|
| Golden questions            | Yes / No  | Pass / fail |
| Known edge cases            | Yes / No  | Pass / fail |
| Access scenarios            | Yes / No  | Pass / fail |
| Refusals and clarifications | Yes / No  | Pass / fail |
| Caveat handling             | Yes / No  | Pass / fail |
| Cost and latency            | Yes / No  | Pass / fail |
| Logging and traceability    | Yes / No  | Pass / fail |

### 9.5 Version and release record

| Item                   | Detail                                                        |
|------------------------|---------------------------------------------------------------|
| Release version        |                                                               |
| Changed components     | Code / prompt / model / config / UI / monitoring / dependency |
| Test evidence          |                                                               |
| Release note required? | Yes / No                                                      |
| Rollback route         |                                                               |
| Release approver       |                                                               |
| Release date           |                                                               |

### 9.6 Post-release review

| Signal  | Review question                        | Action                          |
|---------|----------------------------------------|---------------------------------|
| Quality | Did answer behaviour remain stable?    | Continue / fix / roll back      |
| Cost    | Did cost change materially?            | Continue / optimise / constrain |
| Latency | Did response time change materially?   | Continue / investigate          |
| Support | Did support tickets increase?          | Update guidance / fix           |
| Users   | Did users notice unexpected behaviour? | Communicate / roll back         |

### 9.7 Evidence to retain

- Change intake record.

- Impact checklist.

- Model review record, where relevant.

- Regression evidence.

- Version and release record.

- Release note or support communication.

- Post-release review.

- Rollback or constraint decision, if used.

## 10 Activity 9: Drive controlled adoption and responsible use within approved scope

### 10.1 User onboarding checklist

Purpose: confirm that approved users understand how to use the service responsibly.

| Area            | Confirmation question                                             | Status |
|-----------------|-------------------------------------------------------------------|--------|
| Supported scope | Do users know which questions, domains and outputs are supported? |        |
| Limitations     | Are caveats and known limitations clear?                          |        |
| Responsible use | Do users know when to rely, verify, challenge or escalate?        |        |
| Escalation      | Do users know where to raise issues or concerns?                  |        |
| Feedback        | Is the feedback route clear and usable?                           |        |
| Usage boundary  | Do users know where outputs can and cannot be reused?             |        |

### 10.2 Representative user check-in guide

Purpose: capture adoption and interpretation signals that logs may not reveal.

| Topic        | Question                                                  |
|--------------|-----------------------------------------------------------|
| Workflow fit | Is the service useful in your actual workflow?            |
| Friction     | Where does the experience slow you down or confuse you?   |
| Trust        | Do you know when the answer is reliable enough to use?    |
| Caveats      | Are limitations visible and understandable?               |
| Misuse risk  | Are outputs being used outside the intended workflow?     |
| Unmet needs  | What repeated needs are not covered by the current scope? |

### 10.3 Responsible-use issue log

| Date | User group | Issue                                                                        | Risk                | Action                                |
|------|------------|------------------------------------------------------------------------------|---------------------|---------------------------------------|
|      |            | Over-trust / caveat misunderstanding / unsupported use / inappropriate reuse | Low / medium / high | Guidance / fix / constrain / escalate |

### 10.4 Adoption signal summary

| Signal                         | Interpretation                                | Action                                   |
|--------------------------------|-----------------------------------------------|------------------------------------------|
| High usage inside scope        | Positive adoption signal                      | Continue monitoring                      |
| High usage outside scope       | Scope pressure or misuse                      | Clarify, constrain or route to backlog   |
| Low usage                      | Weak value, onboarding, trust or workflow fit | Review with users                        |
| Repeated unsupported questions | Adjacent need or scope gap                    | Route to backlog or separate initiative  |
| High support load              | Guidance or usability issue                   | Improve support material or product flow |

### 10.5 Scope reminder template

| Item                       | Content |
|----------------------------|---------|
| What the service supports  |         |
| What it does not support   |         |
| Key limitations            |         |
| When to verify or escalate |         |
| Where to give feedback     |         |

### 10.6 Evidence to retain

- Onboarding checklist.

- Representative user check-in notes.

- Responsible-use issue log.

- Adoption signal summary.

- Scope reminder or user communication.

- Requests routed to backlog, expansion or adjacent-needs log.

## 11 Activity 10: Manage lifecycle, retirement and decommissioning readiness

### 11.1 Lifecycle review checklist

Purpose: assess whether the service, or part of it, still has a justified role.

| Area        | Review question                                                     |
|-------------|---------------------------------------------------------------------|
| Value       | Does the service still support a useful workflow or decision cycle? |
| Usage       | Is usage meaningful, even if occasional or seasonal?                |
| Risk        | Are risks still within appetite?                                    |
| Cost        | Are run, model, support and change costs justified?                 |
| Ownership   | Are business, product and operating owners still active?            |
| Replacement | Has another tool, report, workflow or product replaced the need?    |
| Foundation  | Are data, semantic and metadata foundations still maintained?       |

### 11.2 Lifecycle action guide

| Action       | When appropriate                                                        |
|--------------|-------------------------------------------------------------------------|
| Continue     | Value, ownership, cost and risk remain justified.                       |
| Constrain    | Scope, usage, cost or risk needs tighter control.                       |
| Pause        | Temporary issue requires investigation before continued use.            |
| Retire part  | A user group, metric, question type or domain is no longer justified.   |
| Decommission | The service is replaced, unsupported, too costly or no longer valuable. |

### 11.3 Retirement or decommissioning decision record

| Item                                | Decision                                                                          |
|-------------------------------------|-----------------------------------------------------------------------------------|
| Scope affected                      | Full service / user group / domain / metric / question type / integration         |
| Reason                              | Low value / replacement / high cost / risk / weak ownership / obsolete foundation |
| Evidence                            | Usage, value, cost, risk, support or ownership evidence                           |
| Decision owner                      |                                                                                   |
| Effective date                      |                                                                                   |
| User communication needed?          | Yes / No                                                                          |
| Access changes needed?              | Yes / No                                                                          |
| Data, logs or audit actions needed? | Yes / No                                                                          |

### 11.4 Decommissioning action checklist

| Area         | Action                                                |
|--------------|-------------------------------------------------------|
| Users        | Communicate change, date and alternative route.       |
| Access       | Remove or restrict access.                            |
| Guidance     | Update user guidance and known limitations.           |
| Support      | Close or redirect support routes.                     |
| Monitoring   | Disable or adjust monitoring and alerts.              |
| Backlog      | Close, transfer or archive open items.                |
| Logs / audit | Retain required evidence under policy.                |
| Cost         | Stop avoidable run, model, storage or platform costs. |

### 11.5 Evidence to retain

- Lifecycle review notes.

- Retirement or decommissioning decision record.

- User and support communication.

- Access removal or restriction evidence.

- Monitoring, backlog and cost closure record.

- Log, trace and audit retention confirmation.

- Lessons learned for future T2D services.

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
