# Talk-to-Data Delivery Blueprint — Phase 7: Controlled Pilot & User Testing

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
- [3 Pilot learning decision and delivery implications](#3-pilot-learning-decision-and-delivery-implications)
  - [3.1 Possible Phase 7 outcomes](#31-possible-phase-7-outcomes)
  - [3.2 Minimum conditions to proceed to Phase 8](#32-minimum-conditions-to-proceed-to-phase-8)
  - [3.3 Common reasons to extend, narrow, pause or stop](#33-common-reasons-to-extend-narrow-pause-or-stop)
  - [3.4 How Phase 7 shapes later phases](#34-how-phase-7-shapes-later-phases)
- [4 Controlled pilot activities overview](#4-controlled-pilot-activities-overview)
  - [4.1 Activity sequence](#41-activity-sequence)
  - [4.2 Pilot control model](#42-pilot-control-model)
  - [4.3 Activity logic](#43-activity-logic)
  - [4.4 Practitioner note](#44-practitioner-note)
- [5 Core pilot activities](#5-core-pilot-activities)
  - [5.1 Confirm pilot operating plan, cohort and control boundary](#51-confirm-pilot-operating-plan-cohort-and-control-boundary)
  - [5.2 Prepare user, support and operator guidance](#52-prepare-user-support-and-operator-guidance)
  - [5.3 Test pilot access, onboarding, role changes and offboarding](#53-test-pilot-access-onboarding-role-changes-and-offboarding)
  - [5.4 Run controlled pilot usage and monitored sessions](#54-run-controlled-pilot-usage-and-monitored-sessions)
  - [5.5 Capture feedback and monitor pilot signals](#55-capture-feedback-and-monitor-pilot-signals)
  - [5.6 Review answer quality, caveat understanding and user interpretation](#56-review-answer-quality-caveat-understanding-and-user-interpretation)
  - [5.7 Triage issues, manage backlog and controlled change](#57-triage-issues-manage-backlog-and-controlled-change)
  - [5.8 Assess adoption, workflow fit, supportability and Phase 8 implications](#58-assess-adoption-workflow-fit-supportability-and-phase-8-implications)
- [6 Consolidated Phase 7 outputs](#6-consolidated-phase-7-outputs)
  - [6.1 Pilot learning pack](#61-pilot-learning-pack)
  - [6.2 Output quality test](#62-output-quality-test)
  - [6.3 Minimum output set by pilot type](#63-minimum-output-set-by-pilot-type)
  - [6.4 Practitioner note](#64-practitioner-note)
- [7 Exit criteria and handover](#7-exit-criteria-and-handover)
  - [7.1 Required exit outputs](#71-required-exit-outputs)
  - [7.2 Handover to Phase 8](#72-handover-to-phase-8)
  - [7.3 Exit decision wording](#73-exit-decision-wording)
- [8 Key risks and failure modes](#8-key-risks-and-failure-modes)

---

## 1 Executive summary

Phase 7 tests the validated Talk-to-Data MVP with a controlled group of real users, inside the pilot boundary approved in Phase 6.

This phase is not production readiness, broad release or open beta. It should not re-run formal validation from scratch. Its purpose is to answer two practical questions: does the validated MVP work in controlled real use, and if not, what needs to change before it can safely progress?

“Works” should be interpreted broadly. The pilot should test whether users ask appropriate questions, understand caveats, trust the system at the right level and use it in real workflows. It should also test whether the operating conditions around the MVP are credible: onboarding, access changes, offboarding, support, monitoring, escalation, controlled change and issue triage. Where the answer is no, Phase 7 should identify whether the issue comes from the product, data, semantics, user guidance, access model, technology behaviour, support process, workflow fit or operating model.

Phase 7 should therefore connect pilot signals to evidence. Feedback should be linked to traces, user roles, question types, answer outputs, caveats, refusals, escalations, cost, latency and issue categories. Usage volume should be interpreted carefully. Low usage may reveal poor onboarding, weak trust, unclear value or the wrong user cohort. High usage may reveal strong demand, but it may also expose unsafe reliance, unsupported use cases, cost pressure or operational fragility.

The operating lens matters because a pilot that only works through informal support is not close to production. If the build team has to manually provision users, explain every answer, interpret every failure or fix issues outside change control, the pilot is exposing an operating gap, not proving readiness.

Phase 7 is iterative, but it must remain controlled. Quick improvements may be made during the pilot where they are low-risk, tested, communicated and remain inside the approved boundary. Material issues may require the pilot to be constrained or paused while fixes are made and retested. Changes to supported questions, datasets, user groups, access rules, answer logic or model behaviour should not happen silently.

By the end of Phase 7, stakeholders should be able to decide whether the capability should proceed to Phase 8, continue under constraints, extend the pilot, narrow scope, remediate, pause, redesign or stop. The main output is a pilot learning pack covering trace-linked feedback, adoption and trust signals, supportability, usage and risk patterns, controlled changes, backlog items and production-readiness implications.

The main output is a pilot learning pack: trace-linked feedback, adoption and trust signals, support and access findings, usage and risk patterns, issue taxonomy, controlled-change record, pilot backlog, pause or restart decisions, and the gaps that must be addressed before production readiness.

## 2 Phase overview

Phase 7 runs the validated T2D MVP with a controlled group of real users inside the pilot boundary approved at the end of Phase 6. It tests controlled real-world use: whether users can use the MVP responsibly, whether it helps real workflows, whether trust is calibrated correctly, and whether the team can support, monitor and improve the capability under pilot conditions.

Phase 7 is not another validation cycle. The MVP should already have passed the required Phase 6 assurance checks or entered pilot with explicit constraints and accepted residual risks. The focus now is how the system behaves with real users, real questions, real access conditions, real support requests and real operational friction.

The pilot should remain inside the approved boundary: users, data, questions, answer types, caveats, access rules, usage limits, monitoring, escalation routes and pause conditions. Iteration is allowed, but only through controlled change. Quick wins may be released during the pilot if they are low-risk, tested and communicated. Material changes should be reviewed and retested before affected usage continues.

### 2.1 Objective

The objective of Phase 7 is to determine whether the validated MVP can be used safely, usefully and supportably by real pilot users. It should assess:

- **User behaviour:** whether users ask appropriate questions, understand limitations and avoid over-trusting outputs.

- **Workflow fit:** whether the MVP supports real analysis or decision workflows, not only demonstration scenarios.

- **Trust calibration:** whether users know when to rely, challenge, verify or escalate answers.

- **Supportability:** whether support and operator teams can diagnose and resolve user questions, incidents, access issues and misunderstandings using logs, traces and escalation routes.

- **Technology behaviour:** whether the system retrieves the right data, applies the right permissions, logs the right traces and remains within expected cost and latency limits.

- **Process readiness:** whether triage, backlog management, change control, escalation, pause and restart processes work in practice.

The output is a pilot learning pack supporting a decision to proceed to production readiness, proceed with constraints, extend the pilot, narrow scope, remediate, pause or stop.

### 2.2 Scope of the phase

Phase 7 should remain bounded to the MVP and pilot constraints approved at the end of Phase 6. In scope are approved pilot users, supported and excluded questions, proportionate user documentation and guidance, monitored usage, feedback linked to traces, access lifecycle testing, support handling, controlled fixes, adoption assessment, workflow-fit assessment and Phase 8 production-readiness implications.

It is not broad release, open beta or uncontrolled adoption. Pilot users may ask natural questions, including questions outside the approved scope. The system should recognise when a question is unsupported and respond by clarifying, refusing, redirecting or explaining the current boundary. Unsupported demand should be logged as future scope evidence, not silently absorbed into the pilot.

### 2.3 What this phase does not do

Phase 7 does not approve the system for production. It produces evidence for Phase 8 production-readiness assessment.

Phase 7 should not re-run Phase 6 validation from scratch. Access controls, leakage checks, query validation, answer-quality validation, auditability and safe-failure behaviour should already have been tested before pilot exposure. Phase 7 observes whether those controls hold up under real user behaviour.

It also does not rebuild the data foundation, redesign the architecture or define the final operating model. Material issues may trigger remediation, redesign or Phase 8 backlog items, but the pilot itself should not become an uncontrolled rebuild with users attached.

### 2.4 Expected duration and level of effort

The duration of Phase 7 depends on pilot scope, workflow frequency, risk level and evidence required.

Directionally, a narrow expert-user pilot may run for one to two weeks. A controlled business pilot often requires three to six weeks; a decision-critical, sensitive or regulated pilot may require six to ten weeks or more.

For low-frequency workflows, elapsed time is less important than coverage of a meaningful business cycle. A monthly performance-review use case may need a longer pilot window than a daily sales-analysis use case.

Phase 7 should be measured by evidence sufficiency, not by a fixed number of days. The pilot may end early if a clear stop or pause signal emerges. It may be extended where usage is too low, behaviour is inconclusive, timing is unrepresentative or material fixes need retesting.

### 2.5 Main participants and decision owners

Phase 7 requires business, product, data, AI, support, operations, security and governance participation. It should not be treated as a UX test run by the product team alone.

At minimum, named owners should cover pilot scope, business usefulness, user feedback, data and semantic issues, AI/orchestration behaviour, support handling, access lifecycle, security review, evaluation evidence and operating implications.

Every material pilot issue should have an owner, severity, decision route and implication for the pilot boundary or Phase 8 backlog.

## 3 Pilot learning decision and delivery implications

Phase 7 should end with a delivery decision based on controlled real-use evidence, not a general statement that the pilot was useful. Usage volume and satisfaction are useful signals, but they are not enough. A popular pilot may still be unsafe or unsupported. A quiet pilot may reveal poor workflow fit, weak onboarding, low trust or the wrong user cohort.

### 3.1 Possible Phase 7 outcomes

Phase 7 should end with one of the following outcomes.

| Proceed to Phase 8       | Evidence is strong enough to start production-readiness assessment.                                                |
|--------------------------|--------------------------------------------------------------------------------------------------------------------|
| Proceed with constraints | Phase 8 can start, but with reduced users, questions, answer types, data scope or operating assumptions.           |
| Extend pilot             | More evidence is needed before a responsible decision can be made.                                                 |
| Narrow pilot             | The pilot remains useful, but the current boundary is too broad or risky.                                          |
| Pause and remediate      | Material issues must be fixed and retested before affected use continues.                                          |
| Redesign                 | A structural weakness in workflow, data, semantics, orchestration, access or support model requires design change. |
| Stop                     | The use case, risk profile, value case or operating model is not credible enough to continue.                      |

A proceed decision does not mean the system is production-ready. It means the pilot evidence justifies moving into Phase 8, where production controls, release governance, support model, resilience, monitoring thresholds, incident process, access administration, documentation, run cost, ownership and go-live decisioning are confirmed.

### 3.2 Minimum conditions to proceed to Phase 8

Proceed to Phase 8 only when the pilot has produced enough evidence across value, risk and operability.

Minimum conditions should include:

- **Controlled use:** users can use the MVP within the approved boundary without repeated unsafe behaviour.

- **Workflow value:** the MVP supports real analysis, decision support or operational activity.

- **Trust calibration:** users understand caveats, challenge surprising answers and know when to verify or escalate.

- **Supportability:** support and operator teams can diagnose common issues using logs, traces, monitoring and escalation routes.

- **Technology behaviour:** data retrieval, access control, response time, cost, logging and failure behaviour are acceptable for the tested scope.

- **Issue classification:** material issues are linked to traces, user context, question type, root cause, owner and decision route.

- **Phase 8 backlog:** unresolved items are owned, prioritised and suitable for production-readiness assessment or remediation.

If these conditions are not met, the right answer may be to extend, narrow, pause, remediate or redesign before deciding whether Phase 8 is justified.

### 3.3 Common reasons to extend, narrow, pause or stop

Phase 7 should not treat continuation as the default. The pilot should be actively managed through continue, constrain, pause, restart or stop decisions.

Extend where evidence is insufficient: low usage, unrepresentative timing, incomplete workflow coverage, limited support evidence or too few real questions.

Narrow where risk is concentrated: repeated unsupported questions in one domain, weak caveat understanding for specific answer types, excessive support load from one cohort, or risk concentrated in a subset of data, metrics or users.

Pause and remediate where continued exposure may be unsafe or misleading: materially wrong answers in supported scope, access or exposure issues, broken traceability, repeated over-trust, unresolved semantic ambiguity, unacceptable cost or latency, or poor incident diagnosis.

Redesign or stop where the problem is structural: weak business value, poor workflow fit, unreliable grounding, answer formats users systematically misunderstand, no credible operating owner, or evidence that another solution would be more appropriate.

A temporary pause should not be treated as failure. Pausing affected usage while fixing and retesting material issues is often the responsible decision.

### 3.4 How Phase 7 shapes later phases

Phase 7 provides the evidence base for Phase 8 production readiness. It should explain what the pilot proved, what it disproved and what remains uncertain.

The handover should shape production scope, exclusions, operating model, user enablement, technology hardening, evaluation backlog and release risk posture. The detailed Phase 8 handover is consolidated in [Section 7.2](#handover-to-phase-8).

The practical test is simple: Phase 8 should start with a clear production-readiness backlog, not rediscover pilot findings from meeting notes.

## 4 Controlled pilot activities overview

Phase 7 should run as a controlled learning loop, not a loose user trial. The pilot should expose the MVP to real users and workflows while keeping the approved Phase 6 boundary visible and enforceable.

The activities test four dimensions together: user behaviour, supportability, technology behaviour and process readiness. A pilot that only captures user feedback will miss whether access lifecycle works, support can diagnose issues, monitoring is usable, fixes can be controlled and Phase 8 can use the evidence.

### 4.1 Activity sequence

The activities should follow a practical sequence, although several will overlap during the pilot.

| Step | Activity                                                               | Main purpose                                                                                  |
|------|------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| 1    | Confirm pilot operating plan, cohort and control boundary              | Lock users, scope, controls and decision route.                                               |
| 2    | Prepare user guidance and onboard users, operators and support teams   | Make the pilot understandable and supportable.                                                |
| 3    | Test pilot access, onboarding, role changes and offboarding            | Confirm lifecycle and access behaviour.                                                       |
| 4    | Run controlled pilot usage and monitored sessions                      | Observe real use inside the boundary.                                                         |
| 5    | Capture feedback and monitor pilot signals                             | Link feedback, usage, trust, errors, refusals, cost, latency and support signals to evidence. |
| 6    | Review answer quality, caveat understanding and user interpretation    | Test whether answers are correct, understood and safely acted on.                             |
| 7    | Triage issues, manage backlog and controlled change                    | Classify issues, decide actions, manage hot fixes and prevent scope drift.                    |
| 8    | Assess adoption, workflow fit, supportability and Phase 8 implications | Decide what the pilot proves.                                                                 |

### 4.2 Pilot control model

The pilot needs an explicit control model. Users may ask natural questions, including outside-scope questions, but the system and team should not silently expand the pilot to answer them.

The control model should define the approved boundary, change route, monitoring cadence, escalation route and pause conditions. This includes who can approve quick fixes, constraints, pilot pauses, restarts and material changes.

Low-risk quick wins and hot fixes may be released during the pilot if they are tested, logged, communicated and remain inside the approved boundary. Material changes to data, access, supported question types, model behaviour, validation rules or answer logic should be reviewed and retested before affected usage continues.

### 4.3 Activity logic

The activity logic is iterative:

1.  **Set the boundary:** confirm who can use the system, for what purpose and under which constraints.

2.  **Prepare users and support:** make documentation, feedback and escalation routes clear.

3.  **Observe real use:** capture what users ask, how the system responds and how users interpret answers.

4.  **Link signals to evidence:** connect feedback, errors, refusals, escalations and support issues to traces.

5.  **Classify and act:** distinguish product, data, semantic, access, user, support and process issues, then continue, fix, constrain, pause, redesign or stop.

6.  **Package learning:** convert pilot findings into Phase 8 production-readiness evidence and backlog.

A controlled pilot is not frozen, but it should never become informal production or uncontrolled rebuild.

### 4.4 Practitioner note

A pilot is not successful only because users like the tool. It is successful when it shows whether the MVP creates real workflow value, can be used responsibly, can be supported realistically and can be improved safely.

Ideally, users understand caveats, stay within intended use, challenge surprising answers and use the system in the workflow it was designed for. If not, the finding is valuable: misunderstanding caveats, asking unsupported questions, over-trusting fluent answers, creating unexpected support load or revealing workflow mismatch are exactly the signals Phase 7 should surface before production.

## 5 Core pilot activities

### 5.1 Confirm pilot operating plan, cohort and control boundary

**Purpose:** Confirm that the pilot can start with a clear user cohort, operating model, control boundary and decision route.

**Core activities:**

- Confirm the approved pilot users, user groups, access roles and business workflows.

- Reconfirm the pilot boundary from Phase 6: supported questions, excluded questions, data assets, answer types, caveats, usage limits and pause conditions.

- Define the pilot operating rhythm, including review cadence, monitoring responsibilities, support route and escalation path.

- Confirm who can approve quick fixes, hot fixes, constraints, pilot pauses, restarts and material changes.

- Check that user guidance, support guidance, monitoring views and feedback routes are ready before live use.

- Confirm the decision forum and evidence required to proceed, extend, narrow, pause, redesign or stop.

**Output:**

- Pilot operating plan with users, scope, cadence, support route and decision owners.

- Confirmed pilot control boundary covering users, data, questions, answer types and exclusions.

- Pilot decision and escalation route, including pause and restart authority.

- Readiness checklist for user guidance, support guidance, monitoring and feedback capture.

- Initial pilot risk and constraint log.

**Red flags:**

- The pilot starts with unclear users, unclear decision owners or informal approval to expand scope.

- Support, monitoring and escalation routes are assumed rather than tested or assigned.

- Users are approved for access before the data, question and answer boundaries are clear.

- Quick fixes or hot fixes can be released without logging, testing or communication.

- Pause conditions exist on paper but no one is empowered to stop or constrain usage.

**Practitioner note:**  
This should be a quick confirmation task, not a new planning phase. Most of the scope, users, controls and constraints should already have been approved in Phase 6. If Activity 1 requires major debate, missing ownership or material redesign, the pilot is probably not ready to start.

### 5.2 Prepare user, support and operator guidance

**Purpose:** Ensure users, support teams and operators understand how the pilot should be used, supported and controlled.

**Core activities:**

- Prepare proportionate user documentation covering how to access the pilot, use the UI, ask supported questions, understand exclusions and caveats, use the system responsibly, provide feedback, escalate issues and respect usage / cost limits.

- Provide examples of good questions, unsupported questions, clarifications, refusals and caveated answers.

- Confirm support guidance for common user questions, access issues, misunderstood answers, incidents and escalation routes.

- Confirm technical and operator documentation is available and usable, including logs, traces, monitoring views, known limitations, release notes and pause / restart routes.

- Brief users, support teams and operators before live pilot use.

- Capture unclear guidance, repeated user questions and documentation gaps during onboarding.

**Output:**

- Pilot user guide or quick-start note with supported use, exclusions, caveats and feedback route.

- Example question set showing good / unsupported use, clarification / refusal behaviour.

- Support guide covering triage, escalation, access issues and common user confusion.

- Operator documentation checklist covering logs, traces, monitoring, known limitations and pause / restart routes.

- Onboarding completion record and documentation gap log.

- Usage and cost guidance, including expected use, limits, discouraged behaviours and escalation for heavy or unusual usage

**Red flags:**

- Users treat the pilot as production-ready or assume they can rely on answers without caveats.

- Support teams cannot explain what is in scope, what is out of scope or when to escalate.

- Technical documentation exists but is not usable by support or operators during incidents.

- Feedback is captured informally and cannot be linked to traces or issue categories.

- Documentation says “ask anything” while the approved answer boundary remains narrow.

**Practitioner note:**  
Documentation should be proportionate, not heavy by default. A small expert pilot may only need a quick-start note and a lightweight support route. A broader business pilot needs clearer user guidance, support instructions and operator documentation. If the pilot depends on the build team explaining every issue live, the operating model is not being properly tested.

### 5.3 Test pilot access, onboarding, role changes and offboarding

**Purpose:** Confirm that pilot access and user lifecycle changes work correctly within expected operational timelines.

**Core activities:**

- Test that approved pilot users can access the MVP through the expected identity, group, role and connection route.

- Confirm that each user sees only the data, questions and answer types allowed by their role or access group.

- Include planned lifecycle scenarios in the pilot test plan, such as adding a new user, changing role, changing region or removing access.

- Confirm or baseline the expected timing for access changes to take effect, including approval, provisioning, permission sync and system visibility.

- Test offboarding or access removal for users who leave the pilot, change role or no longer require access.

- Capture access exceptions, workarounds, delays, stale permissions and support steps.

**Output:**

- Pilot access test evidence by user group, role and data boundary.

- User lifecycle test plan covering onboarding, role / access change and offboarding.

- Access-change timing record, including expected and observed propagation times.

- Access exception and workaround log.

- Production-readiness gaps for identity, permissions, user administration and support handling.

**Red flags:**

- Access changes depend on manual fixes that are not visible to support or governance.

- Permission changes take effect later than expected, with no clear communication or monitoring.

- Role or region changes create stale permissions, incorrect data visibility or inconsistent answers.

- Offboarding is slow, unclear or not testable during the pilot.

- Support cannot distinguish access issues from data, model, UI or user misunderstanding issues.

**Practitioner note:**  
**Note 1:** Access lifecycle should be tested deliberately when the pilot is on a path to production. For a small POC or expert pilot, manual provisioning may be acceptable, but it should be documented.

**Note 2:** Where access changes are tested, the team needs enough traceability to confirm the effect: who asked the question, under which role or permission, what data boundary was applied, and what query or tool call was generated. For sensitive data, this may require restricted access to logs or redacted traces rather than broad visibility.

### 5.4 Run controlled pilot usage and monitored sessions

**Purpose:** Observe how real users use the MVP inside the approved pilot boundary.

**Core activities:**

- Run pilot usage through the agreed channel, environment, user cohort and operating rhythm.

- Combine normal user activity with a small number of monitored sessions where users complete realistic workflow tasks.

- Encourage users to ask natural questions, including outside-scope questions, so boundary handling can be observed.

- Capture how users interpret answers, caveats, refusals, clarifications, sources and follow-up prompts.

- Monitor whether users stay within responsible-use guidance, usage limits and escalation expectations.

- Record practical friction, including access, UI, latency, unclear wording, missing context and support needs.

**Output:**

- Pilot usage record covering users, sessions, question types and workflow context.

- Monitored-session notes showing user behaviour, interpretation and friction points.

- Outside-scope question log with system response and backlog implication.

- User behaviour observations linked to feedback, traces or support tickets.

- Pilot issue candidates for triage in Activity 8.

**Red flags:**

- Users only test artificial prompts and do not use the MVP in a real workflow.

- The pilot becomes a demo session where facilitators guide users around known weaknesses.

- Users treat caveated or partial answers as final decision evidence.

- Outside-scope questions are answered informally by the team instead of being handled by the system.

- Important behaviour is discussed in meetings but not linked to traces, feedback or issue records.

**Practitioner note:**  
**Note 1:** Controlled pilot usage should feel realistic, not theatrical. The point is not to make the MVP look good; it is to see what users actually ask, how they react to answers, where they misunderstand the boundary and whether the system remains useful without the build team coaching every interaction.

**Note 2:** A diverse pool of realistic users is often hard to secure. A pilot made only of sponsors, champions or highly motivated users may still be useful, and sometimes it is the only practical option, but the evidence should be caveated. The pilot output should state clearly whether findings reflect normal users, expert users, friendly users or a narrow champion group.

### 5.5 Capture feedback and monitor pilot signals

**Purpose:** Turn pilot usage, feedback, monitoring and support signals into diagnosable evidence linked to real system behaviour.

**Core activities:**

- Capture structured feedback from the UI, support channel, monitored sessions and user interviews.

- Link material feedback to user role, question type, timestamp, system trace, answer, caveat, refusal, escalation and outcome.

- Track usage by user group, question type, workflow, time period and interaction pattern.

- Monitor trust signals, including repeated verification, ignored caveats, over-reliance, low confidence, abandoned sessions and escalation behaviour.

- Review errors, refusals, clarifications, failed queries, empty results, timeout events and unsupported-question handling.

- Monitor support tickets, incidents, access issues, repeated confusion and escalation volume.

- Track latency, model usage, query cost, infrastructure cost and high-cost interaction patterns.

- Classify feedback and monitoring signals by source: useful answer, wrong answer, confusing answer, unsupported question, refusal issue, latency issue, access issue, workflow issue, support issue or cost issue.

- Separate user perception from diagnosis; a complaint may reflect a product issue, data gap, semantic ambiguity, unsupported scope, poor guidance or user misunderstanding.

- Capture positive feedback only where it links to real workflow value, not generic satisfaction.

- Review pilot signals at the agreed cadence and flag items requiring triage, hot fix, user guidance, constraint or pause.

**Output:**

- Feedback-to-trace register linking user feedback to questions, traces, answers, caveats and issue categories.

- Pilot monitoring dashboard or review pack covering usage, quality, errors, refusals, support, cost and latency.

- Usage-pattern summary by cohort, workflow, question type and distinctive user behaviour.

- Trust and responsible-use signal summary.

- Positive-value evidence showing where the MVP helped a real workflow.

- Unsupported-demand log showing questions users wanted to ask beyond the approved scope.

- Cost, latency and performance exception log.

- Escalation, incident and support summary for Activity 7 triage.

**Red flags:**

- Feedback is collected as comments or ratings but cannot be linked to questions or traces.

- Usage is measured only as volume, without understanding value, risk or question type.

- Positive feedback is treated as evidence of value without knowing what workflow it supported.

- Users report wrong or confusing answers, but the team cannot reconstruct the interaction.

- Unsupported demand is treated as product failure instead of being separated from approved-scope performance.

- High usage creates cost, latency or support pressure that is not visible to decision owners.

- Refusals, clarifications and errors are counted but not reviewed for whether they were appropriate.

- Trust signals are inferred from satisfaction scores rather than observed behaviour.

- Monitoring dashboards exist but are not used in review meetings or pilot decisions.

**Practitioner note:**

Monitoring should not become vanity reporting. Usage counts and satisfaction scores are useful, but they do not show whether the pilot is safe or valuable. The important patterns are behavioural: who uses it heavily, who avoids it, who asks unsupported questions, who ignores caveats, who escalates, and which interactions create cost, latency or support burden.

A practical approach is to follow up with users who show distinctive behaviour: unusually high usage, low usage, repeated unsupported questions, repeated refusals, high feedback volume or no feedback despite heavy use.

### 5.6 Review answer quality, caveat understanding and user interpretation

**Purpose:** Assess whether real pilot answers are correct, understood and safely acted on.

**Core activities:**

- Review a sample of real pilot interactions across supported, ambiguous and outside-scope questions.

- Check whether answers use the right data, metric, filters, grain, caveats and access boundary.

- Assess whether users understand answer wording, caveats, limitations, refusals and clarifications.

- Identify technically correct answers that are misunderstood or used in the wrong decision context.

- Identify interactions where traces are not enough to explain user intent, interpretation or decision use, and select them for follow-up interview.

- Flag answer issues requiring user education, wording changes, product fixes, constraints or pause.

**Output:**

- Real-interaction answer-quality review covering correctness, grounding, caveats and interpretation.

- Misunderstood-answer log showing where technically correct answers created user confusion.

- Caveat and refusal understanding summary.

- User-interpretation issues linked to traces, feedback, question types and follow-up interview needs.

- Candidate fixes for answer format, guidance, training, backlog or pilot constraints.

**Red flags:**

- Answers are technically correct but users draw unsupported conclusions from them.

- Caveats are shown but ignored, misunderstood or too weakly placed.

- Users treat descriptive outputs as causal explanation or recommendation.

- Refusals and clarifications are correct technically but unclear to users.

- The team reviews answer correctness without checking how users interpreted or used the answer.

**Practitioner note:**  
A correct answer can still fail if users misunderstand it. In T2D, quality is not only whether the number matches the data; it is whether the user understands what the answer means, what it does not mean, and whether it is safe to use in the workflow. Some interactions cannot be judged from traces alone. Where the user intent, interpretation or decision impact is unclear, the team should follow up through a short interview rather than guessing from logs.

### 5.7 Triage issues, manage backlog and controlled change

**Purpose:** Classify pilot issues, decide the right action and manage improvements without allowing scope drift or untested behaviour changes.

**Core activities:**

- Review issues from feedback, traces, monitoring, support tickets, answer-quality reviews and access tests.

- Classify each issue by source: product, data, semantic, access, model or orchestration, user education, support, process or scope.

- Assess severity, affected users, affected question types, recurrence, business impact, confidence impact and exposure risk.

- Decide whether to continue, monitor, educate, fix, constrain, pause, restart, redesign or stop.

- Classify triaged issues as hot fix, quick win, pilot constraint, Phase 8 item, later enhancement or redesign signal.

- Apply hot fixes only where they are bounded, tested, logged, communicated and inside the approved pilot boundary.

- Retest material fixes before affected usage restarts or expands.

- Update user guidance, support guidance, monitoring views or caveat wording where pilot learning shows avoidable confusion.

- Maintain version history for changes to prompts, model routing, validation rules, metadata, UI wording, access handling or answer format.

- Communicate relevant changes to pilot users, support teams, operators and decision owners.

- Assign owner, decision route, evidence required and review point for each material issue.

**Output:**

- Pilot issue triage log with source, severity, owner, decision and evidence link.

- Continue, constrain, pause, restart, redesign or stop decision records for material issues.

- Root-cause summary by issue type, user cohort and question category.

- Controlled pilot backlog with owner, priority, decision route and target phase.

- Hot-fix and quick-win log with test evidence, version history, release note and communication record.

- Retest evidence for material fixes or restarted pilot scope.

- Updated pilot constraints, user guidance, support guidance or monitoring notes where applicable.

- Phase 8 backlog items separated from later enhancements.

**Red flags:**

- Issues are treated as generic “feedback” rather than classified by cause and decision route.

- The team fixes symptoms without deciding whether the issue is product, data, semantic, access, user or process related.

- Material issues continue in pilot because no one is empowered to pause or constrain usage.

- Every issue is pushed into the backlog, including items that should trigger immediate constraint or remediation.

- Unsupported-scope demand is treated as a defect rather than separated from approved-scope performance.

- Hot fixes are released without regression checks, version history or communication.

- The pilot expands through backlog fixes instead of formal scope approval.

- Material fixes restart affected usage without retest evidence.

- Users are not told when answer behaviour, caveats, supported scope or known limitations change.

- The team keeps patching symptoms instead of recognising a structural redesign need.

**Practitioner note:**

A pilot should be able to improve while it runs, but changes must remain visible, tested and controlled. The discipline is to classify before fixing: decide whether an issue is product, data, semantic, access, user, support or process-related, and whether it should be fixed now, constrained, paused, moved to Phase 8 or treated as later scope.

Hot fixes should trigger the relevant regression checks. The risk is not fixing issues quickly; the risk is releasing untracked fixes that change behaviour, hide evidence or expand scope without approval.

### 5.8 Assess adoption, workflow fit, supportability and Phase 8 implications

**Purpose:** Decide what the pilot proves about value, real-world use, supportability and production-readiness needs.

**Core activities:**

- Assess whether representative users used the MVP for real workflows, not only test prompts or curiosity.

- Review adoption signals, including sustained use, low use, repeated use, requests for more scope and workflow integration demand.

- Evaluate workflow fit: where the MVP improved speed, exploration, consistency, decision support or analyst dependency.

- Assess supportability, including support volume, costs, escalation needs, incident handling, access lifecycle and build-team dependency.

- Consolidate unresolved risks, constraints, hot fixes, production-readiness gaps and later enhancements.

- Recommend whether to proceed to Phase 8, proceed with constraints, extend, narrow, pause, redesign or stop.

**Output:**

- Pilot adoption and workflow-fit assessment.

- Supportability and operating-model findings.

- Value evidence linked to representative users, workflows and real interactions.

- Phase 8 production-readiness backlog with owners and priorities.

- Phase 7 decision recommendation and rationale.

**Red flags:**

- Pilot success is claimed from positive feedback without evidence of real workflow use.

- Usage is driven mainly by sponsors or champions but presented as representative adoption.

- Users want broader scope, but safety, supportability or cost implications are not assessed.

- Support still depends heavily on the build team for diagnosis, fixes or user explanations.

- The Phase 8 backlog mixes production blockers, nice-to-have features and unresolved pilot risks.

**Practitioner note:**  
The strongest pilot signal is not excitement; it is representative users coming back because the MVP helps their real work and asking for more scope, better integration or broader access. That is strong evidence of value pull, but it is not production readiness. Phase 7 should separate value evidence from hardening needs: a tool users want more of may still need stronger access lifecycle, monitoring, documentation, support, cost control and governance before release.

## 6 Consolidated Phase 7 outputs

Phase 7 should produce a small set of decision-useful outputs, not a large archive of pilot notes. The purpose is to show what happened in controlled real use, what the team learned, what must change before production readiness, and whether the MVP should proceed, continue with constraints, pause, narrow, redesign or stop.

The outputs should be traceable enough to support a senior decision. Positive user comments, usage charts and issue lists are useful only if they are connected to real users, workflows, question types, traces, support evidence and risk decisions.

### 6.1 Pilot learning pack

The main output of Phase 7 is the pilot learning pack. It should consolidate the evidence needed to decide whether the MVP is ready for Phase 8 production-readiness assessment.

The pilot learning pack should include:

| Output                                 | Purpose                                                                                                     |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Pilot scope and boundary summary       | Confirms users, questions, data, answer types, caveats, constraints and exclusions tested during the pilot. |
| User cohort and evidence caveats       | Explains whether users were representative, expert, friendly, sponsor-led or narrow.                        |
| Usage and adoption summary             | Shows usage patterns by user group, workflow, question type and distinctive behaviour.                      |
| Workflow-fit assessment                | Explains whether the MVP supported real work, not only demonstrations or curiosity.                         |
| Trust and interpretation findings      | Summarises caveat understanding, over-trust, under-trust, verification and misunderstood answers.           |
| Feedback-to-trace evidence             | Links material feedback to questions, answers, traces, support tickets and issue categories.                |
| Supportability findings                | Shows whether support and operator teams could diagnose, escalate and handle pilot issues.                  |
| Technology behaviour summary           | Covers access lifecycle, logs, latency, cost, errors, refusals, monitoring and hot fixes.                   |
| Governance, triage and decision log    | Shows issue source, severity, owner, decision rights, risk acceptance, action and review point.             |
| Pilot backlog and Phase 8 implications | Separates hot fixes, pilot constraints, production-readiness items and later enhancements.                  |
| Final Phase 7 decision recommendation  | States proceed, proceed with constraints, extend, narrow, remediate, pause, redesign or stop.               |

The pack should make evidence limitations explicit. A pilot run mainly with champions may still be valuable, but it should not be presented as proof of broad adoption. A pilot with low usage may still be useful if it explains why users did not adopt the tool. A pilot with strong value pull may still need substantial production hardening.

### 6.2 Output quality test

Before Phase 7 outputs are used for decision-making, the team should check whether they are clear, evidence-based and decision-ready.

| Test                    | Question                                                                                                         |
|-------------------------|------------------------------------------------------------------------------------------------------------------|
| Boundary clarity        | Is it clear what was actually piloted and what remained out of scope?                                            |
| Evidence traceability   | Are material findings linked to traces, users, question types, feedback or support records?                      |
| User representativeness | Does the pack state whether pilot users were representative, expert, sponsor-led or unusually motivated?         |
| Value evidence          | Is workflow value evidenced through real use, not only positive comments or satisfaction?                        |
| Trust evidence          | Does the pack show whether users understood caveats, refusals, limitations and answer boundaries?                |
| Supportability evidence | Is it clear whether support could diagnose and resolve common issues without relying on the build team?          |
| Technology evidence     | Are access lifecycle, latency, cost, logging, errors and hot fixes covered?                                      |
| Issue classification    | Are issues classified by root cause and decision route, not just listed as feedback?                             |
| Backlog quality         | Are Phase 8 blockers separated from pilot fixes and later enhancements?                                          |
| Decision usefulness     | Could a senior decision owner make a proceed, constrain, extend, pause, redesign or stop decision from the pack? |

If the answer to several of these questions is no, the phase may have generated activity but not decision evidence.

### 6.3 Minimum output set by pilot type

The output set should be proportionate to the pilot’s intent and risk.

| Pilot type                           | Minimum expected outputs                                                                                                                                                                |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Small POC or expert pilot            | Pilot scope summary, user notes, basic feedback log, key traces, issue list, learning summary and caveats.                                                                              |
| Controlled business pilot            | Pilot learning pack, feedback-to-trace register, usage summary, support findings, triage log, pilot backlog and decision recommendation.                                                |
| Production-path MVP                  | Full pilot learning pack, representative-user caveats, access lifecycle evidence, monitoring summary, hot-fix records, supportability findings, Phase 8 backlog and residual-risk view. |
| Sensitive or decision-critical pilot | Production-path outputs plus stronger evidence on access, exposure, auditability, user interpretation, support escalation, pause decisions and risk acceptance.                         |

The output standard should rise when the pilot touches sensitive data, senior decision workflows, broad user groups, regulated reporting, financial metrics or high-cost usage patterns.

### 6.4 Practitioner note

The consolidated outputs should tell a clear story: who used the MVP, for what workflow, what happened, what was useful, what failed, what was misunderstood, what support could handle, what technology needs hardening, and what Phase 8 must decide. Anything else belongs in the annexes or backlog, not the main decision pack.

## 7 Exit criteria and handover

Phase 7 should end with a clear decision and a usable handover to Phase 8. The objective is not to prove production readiness, but to decide whether the MVP has enough real-use evidence to enter production readiness and controlled-release preparation, under which constraints, with which backlog, and with which issues requiring fix, acceptance, monitoring, redesign or deferral.

The handover should explain what the pilot proved, what it did not prove, what remains uncertain and what must be fixed, accepted, constrained or deferred before broader release. It should not hand over a generic feature backlog without value, risk, supportability and governance context.

### 7.1 Required exit outputs

The required exit output is the pilot learning decision pack described in Section 6, completed to the standard required by pilot scale and risk.

The exit decision should confirm whether the MVP can proceed to Phase 8, proceed with constraints, extend pilot, narrow pilot, pause and remediate, redesign or stop. It should also identify the tested boundary, evidence limitations, production-readiness backlog, residual risks, supportability findings and ownership route.

The evidence does not need to be perfect, but it must be honest. If users were mostly champions, if usage was low, if support was handled by the build team or if access lifecycle was only manually tested, the exit pack should say so.

### 7.2 Handover to Phase 8

The Phase 8 handover should focus on production-readiness implications, not general product ideas. It should make clear what needs to be hardened, approved, funded, supported or constrained before any broader release.

The handover should cover:

- **Production scope:** users, domains, question types, data assets and answer types recommended for production-readiness assessment.

- **Production exclusions:** areas that should remain out of scope until data, semantic, access, evaluation or support gaps are closed.

- **Access and security:** user lifecycle, row / column restrictions, sensitive-data controls, auditability and residual exposure risks.

- **Support model:** support ownership, escalation route, operating hours, incident handling, runbooks and support trace access.

- **Monitoring and quality:** monitoring signals, alert thresholds, regression tests, answer-quality review and drift risks.

- **User enablement:** documentation, onboarding, usage guidance, caveat explanations and responsible-use expectations.

- **Technology hardening:** reliability, latency, cost controls, logging, traceability, release process and rollback route.

- **Governance and economics:** decision rights, risk acceptance, change control, run-cost ownership and budget implications.

Any issue accepted during the pilot should be reclassified before Phase 8. “Accepted for pilot” does not mean “acceptable for production”. Phase 8 should decide whether each accepted issue becomes a blocker, a constraint, a monitored residual risk or a later enhancement.

### 7.3 Exit decision wording

Phase 7 should close with explicit decision wording. The wording should be precise enough for a sponsor, product owner, security lead, operating owner and Phase 8 team to understand what is being approved.

Example decision wording: Proceed to Phase 8 for the approved sales performance scope, limited to regional managers and sales operations users. Pilot evidence shows repeated workflow use, manageable support load and acceptable answer interpretation for revenue and pipeline questions. Margin, forecasting and individual performance questions remain out of scope. Phase 8 must address access lifecycle timing, support trace access, monitoring thresholds, documentation, run-cost ownership and production release governance before any broader rollout.

Alternative decisions should be equally explicit:

- **Proceed with constraints:** state which users, questions, data or answer types are excluded.

- **Extend pilot:** state what evidence is missing and how the extension will collect it.

- **Narrow pilot:** state which risk or support burden requires reduced scope.

- **Pause and remediate:** state what must be fixed and retested before restart.

- **Redesign:** state which structural assumption failed.

- **Stop:** state why value, risk or operability does not justify continuation.

## 8 Key risks and failure modes

Phase 7 reduces uncertainty by exposing the MVP to controlled real use. It does not remove risk. The main risks in this phase come from confusing pilot enthusiasm with readiness, allowing the boundary to drift, missing weak trust signals, or failing to turn real-use evidence into production-readiness decisions.

| Risk / failure mode               | Why it matters                                                                                        | Likely response                                                                           |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Pilot becomes informal production | Users rely on the MVP beyond the approved boundary before production controls exist.                  | Reinforce pilot status, constrain usage and escalate unsafe reliance.                     |
| Scope expands silently            | New users, data, questions or answer types are absorbed without validation.                           | Log demand, refuse or redirect unsupported use, and route expansion through approval.     |
| Pilot signals are misread         | Positive feedback, low usage or champion-user enthusiasm can all distort the real adoption picture.   | Link signals to real workflows, representative users, traces and follow-up interviews.    |
| Trust and interpretation are weak | Users may over-trust fluent answers or misunderstand technically correct outputs.                     | Improve caveats, answer wording, onboarding and escalation guidance; constrain if needed. |
| Unsupported demand is mishandled  | Out-of-scope questions may be mistaken for product failure or silently added to scope.                | Separate boundary-handling quality from future-scope demand.                              |
| Support cannot diagnose issues    | The pilot remains dependent on the build team and does not test the operating model.                  | Improve support documentation, trace access, runbooks and escalation route.               |
| Access lifecycle is under-tested  | Onboarding may work, but role changes, revocation or offboarding may fail.                            | Test or document lifecycle shortcuts and carry production-grade gaps into Phase 8.        |
| Monitoring is decorative          | Dashboards exist but do not drive decisions, constraints, fixes or pause actions.                     | Define review cadence, owners and decision thresholds.                                    |
| Controlled change breaks down     | Hot fixes change behaviour, caveats, refusals, access or cost without test evidence or communication. | Require regression checks, version history and user/support communication.                |
| Backlog loses decision structure  | Blockers, pilot fixes, Phase 8 items and later enhancements are mixed together.                       | Classify backlog by decision route and production-readiness implication.                  |
| Pause conditions are not used     | The team sees risk but keeps running because stopping feels politically difficult.                    | Empower pause authority and treat temporary pause as controlled delivery, not failure.    |

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
