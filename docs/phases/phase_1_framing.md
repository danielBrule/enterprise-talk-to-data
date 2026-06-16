# Talk-to-Data Delivery Blueprint — Phase 1: Framing

*Daniel Brule · Talk-to-Data Delivery Blueprint · v1.0 · June 2026*

---

**Table of contents**

- [1 Executive summary](#1-executive-summary)
- [2 Phase Overview](#2-phase-overview)
  - [2.1 Objective](#21-objective)
  - [2.2 Scope of the phase](#22-scope-of-the-phase)
  - [2.3 What this phase does not do](#23-what-this-phase-does-not-do)
  - [2.4 Expected duration and level of effort](#24-expected-duration-and-level-of-effort)
  - [2.5 Main participants and decision owners](#25-main-participants-and-decision-owners)
- [3 Framing decision and delivery implications](#3-framing-decision-and-delivery-implications)
  - [3.1 The five possible framing outcomes](#31-the-five-possible-framing-outcomes)
  - [3.2 Minimum conditions to proceed](#32-minimum-conditions-to-proceed)
  - [3.3 Common reasons to reassess the initiative](#33-common-reasons-to-reassess-the-initiative)
  - [3.4 How framing shapes later phases](#34-how-framing-shapes-later-phases)
- [4 Framing activities overview](#4-framing-activities-overview)
  - [4.1 Activity sequence](#41-activity-sequence)
  - [4.2 Output need levels](#42-output-need-levels)
- [5 Framing activities](#5-framing-activities)
  - [5.1 Business framing](#51-business-framing)
  - [5.2 User and workflow discovery](#52-user-and-workflow-discovery)
  - [5.3 Initial data landscape scan](#53-initial-data-landscape-scan)
  - [5.4 Initial semantic framing](#54-initial-semantic-framing)
  - [5.5 Security and governance framing](#55-security-and-governance-framing)
  - [5.6 Solution architecture framing](#56-solution-architecture-framing)
  - [5.7 Delivery planning and MVP boundary](#57-delivery-planning-and-mvp-boundary)
  - [5.8 Evaluation design framing](#58-evaluation-design-framing)
  - [5.9 Operating model framing](#59-operating-model-framing)
- [6 Framing decision pack](#6-framing-decision-pack)
  - [6.1 Decision-pack quality test](#61-decision-pack-quality-test)
- [7 Exit criteria and handover](#7-exit-criteria-and-handover)
  - [7.1 Readiness check before exit](#71-readiness-check-before-exit)
  - [7.2 Required exit outputs](#72-required-exit-outputs)
  - [7.3 Handover to later phases](#73-handover-to-later-phases)
  - [7.4 Exit decision wording](#74-exit-decision-wording)
  - [7.5 Practitioner note](#75-practitioner-note)
- [8 Key risks and failure modes](#8-key-risks-and-failure-modes)
  - [8.1 Practitioner note](#81-practitioner-note)

---

## 1 Executive summary

The framing phase determines whether Talk-to-Data (T2D) is the right response to a real business need, and whether the initial ambition is realistic within the expected timeline, budget and organisational constraints.

It should start with the business questions users need to answer, the decisions those answers support, and the evidence required for the organisation to trust the system. The aim is to confirm whether there is a valuable decision workflow, a bounded user group, answerable priority questions, plausible data foundations, manageable security and governance constraints, and accountable owners.

The framing phase should produce enough evidence to make one of five explicit delivery decisions: proceed, narrow, pause, redirect or stop.

A successful framing phase does not solve every data, semantic, security, operating model or architecture question. It identifies the major risks, assumptions and constraints early enough to shape the next delivery phases and avoid building a prototype with no credible path to production.

By the end of framing, senior stakeholders should be able to say, in plain language, what is being built, for whom, why it matters, what is out of scope, what is assumed, what is risky, whether the timeline and budget are credible, who owns the decision, and what evidence is required before moving forward.

## 2 Phase Overview

### 2.1 Objective

The objective of Phase 1 is to decide whether Talk-to-Data should move forward, and if so, how the first delivery scope should be shaped.

Framing defines the initial use case, target users, priority questions, MVP boundary, success criteria, risk posture, governance route, budget envelope and ownership model. It also captures early assumptions about data availability, semantic maturity, security constraints, architecture feasibility, evaluation and operating readiness.

The purpose is not to solve every downstream issue. It is to expose the material risks, assumptions and constraints early enough to shape delivery before the team commits to detailed readiness assessment, architecture design or prototype build.

Weak framing usually fails later: the prototype looks promising but cannot be trusted, secured, evaluated, funded or operated.

**Practitioner note**: Communication matters during framing. If the phase is presented only as risk, governance and control, it may slow momentum or make the initiative feel blocked before it has been properly explored. If those topics are avoided, the project may start on weak assumptions and become harder to correct later. The aim is to create a balanced discussion: enough structure to make the decision responsible, and enough openness to let a valuable idea develop.

### 2.2 Scope of the phase

Phase 1 should remain deliberately bounded. It should identify what is known, what is assumed, what is risky and what must be validated later. The minimum framing questions are:

- **Why T2D is being considered** and which business decision or workflow it should improve.

- **Who the first users are**, how they currently get answers, what blockers they face, and why the current approach is not working well enough

- **Which questions are in scope** for the first release.

- **Which questions are explicitly out of scope** and why.

- **Which alternative route,** such as a dashboard, report, semantic-layer fix or analyst workflow, may be more appropriate.

- **Which sources, reports, datasets or semantic assets** may support the use case, and whether they are approved, informally trusted, assumed trusted or require validation.

- **Which metrics, dimensions, joins and filters are likely to create semantic risk.**

- **Which access, privacy, compliance and audit constraints may affect feasibility.**

- **Which architecture assumptions need validation before prototype or MVP delivery.**

- **How correctness, usefulness and safe failure will be evaluated.**

- **Who provisionally owns the business outcome, delivery decisions and operating route**, recognising that ownership may evolve between POC, MVP, pilot and production.

### 2.3 What this phase does not do

Framing is not a full data readiness assessment, semantic modelling exercise, security review, architecture design, vendor selection process or production plan.

It should not finalise every metric definition, access rule, architecture decision, evaluation set or operating model. Those require deeper evidence and are handled in later phases.

However, framing must expose major blockers. If the business problem is vague, the user group is unclear, the data is unlikely to support the questions, metrics are contested, access cannot be controlled, or no owner will operate the capability, the initiative should not move directly into build.

A framing phase that stops or redirects a weak T2D initiative has done its job.

### 2.4 Expected duration and level of effort

For a focused discovery, POC or early MVP, framing can usually be completed in a few days to one week if the right stakeholders are available.

The effort should match the risk. A narrow internal prototype using non-sensitive data may need lightweight framing. A decision-critical, sensitive, regulated, cross-domain or broad-user use case requires deeper framing before progressing.

The phase should not be measured by elapsed time. The real measure is whether the team has enough evidence to make a responsible proceed, narrow, pause, redirect or stop decision.

### 2.5 Main participants and decision owners

The exact participants may vary, but the framing decision should not be made by the AI or technology team alone. The minimum ownership model is:

| Role                    | Main responsibility in framing                                           |
|-------------------------|--------------------------------------------------------------------------|
| Executive sponsor       | Confirms strategic rationale, funding route and risk appetite            |
| Product owner           | Owns MVP scope, user needs, trade-offs and priorities                    |
| Business owner / SME    | Validates workflow, priority questions and decision value                |
| Data owner              | Confirms likely source-of-truth assets and usage constraints             |
| Metric / semantic owner | Identifies definition risks, approved metrics and caveats                |
| Security / gov. lead    | Identifies access, privacy, compliance, audit and exposure constraints   |
| AI / solution architect | Assesses orchestration, tool use, query flow and integration feasibility |
| Evaluation owner        | Shapes how correctness, safety and usefulness will be tested             |
| Operating owner         | Identifies the likely support and ownership route beyond POC             |

The important point is not that every role attends every discussion. It is that the major decisions have named owners. The important point is not that every role attends every meeting.

## 3 Framing decision and delivery implications

Framing should not end with a vague recommendation to “continue discovery”. It should end with one of five explicit outcomes: **proceed, narrow, pause, redirect or stop**[^1].

The decision should be based on the evidence gathered during framing and on the actions taken to address early issues where possible. The goal is not simply to list risks for later; it is to resolve what can be resolved, narrow what is too broad, and make the remaining assumptions explicit.

A proceed decision is not a final commitment to production. It means the initiative is credible enough to enter the next delivery phases with a defined scope, known assumptions and testable risks. Later phases may still expose data, semantic, security, architecture, evaluation or operating issues that require the scope, timeline, budget or delivery approach to be adjusted.

### 3.1 The five possible framing outcomes

Framing should end with one of five explicit delivery decisions that should be used consistently in the framing decision record.

| Outcome  | Meaning                                                             | Typical trigger                                                                         |
|----------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Proceed  | Move to the next delivery phases with the proposed scope.           | The use case is valuable, bounded and plausible.                                        |
| Narrow   | Continue, but reduce the scope, user group, domain or question set. | The opportunity is real, but the initial ambition is too broad.                         |
| Pause    | Delay delivery until material blockers are resolved.                | Data, ownership, security, funding or governance questions are not ready.               |
| Redirect | Address the need through another intervention.                      | A dashboard, report, semantic-layer fix or analyst workflow is more appropriate.        |
| Stop     | Do not proceed with T2D for this use case.                          | The value case is weak, the risk is too high, or the conditions for success are absent. |

### 3.2 Minimum conditions to proceed

A proceed decision does not mean the initiative is fully de-risked. It means the minimum conditions justify moving to the next delivery phases. Proceed only when

- **Value is clear:** the use case supports a real decision or workflow.

- **Scope is bounded:** the first users, question set and exclusions are understood.

- **Foundations are plausible**: candidate data, metrics and access routes appear viable, even if they still require validation.

- **Alternative routes have been considered:** the team can explain why T2D is preferable to a dashboard, report, semantic-layer fix or analyst workflow.

- **Risks are visible:** the main semantic, security, evaluation and operating risks are explicit.

- **Delivery is credible:** ambition is align with the available timeline, budget and capacity.

- **Ownership exists:** named owners cover value, delivery and key controls.

### 3.3 Common reasons to reassess the initiative

The team should avoid moving directly into build if any of the following conditions apply without a credible mitigation or learning objective:

- **Technology-led rationale:** T2D is being pursued mainly because GenAI is attractive, without a clear decision workflow or learning objective. Structured learning can be a legitimate POC objective, but the success criteria should then focus on feasibility, risks, user value, data readiness and delivery implications.

- **Unclear users:** the first user group is vague, too broad or not close enough to the decision being improved.

- **Weak question set:** questions are generic, low-value, too rare or not specific enough to drive data, semantic and evaluation work.

- **Dashboard problem:** the need appears better served by improving existing BI, reporting, semantic-layer assets or analyst workflows.

- **Unresolved metric ambiguity:** key terms such as revenue, margin, churn, customer or stock have material ambiguity, and there is no credible route to define a safe MVP interpretation.

- **Unclear source of truth:** candidate data exists, but ownership, quality, lineage or usage rights are too uncertain to support even a bounded POC or MVP.

- **Unmanaged exposure risk:** the use case involves sensitive data, inference risk or repeated-query risk, and there is no plausible control route.

- **Weak evaluation route:** the team cannot yet identify candidate test questions, expected-answer sources or quality criteria for correctness, usefulness and safe failure.

- **No credible owner:** the initiative has no clear owner for value, scope, key definitions, risk acceptance or delivery decisions.

- **Unrealistic delivery envelope:** the timeline, budget or capacity is materially inconsistent with the ambition.

### 3.4 How framing shapes later phases

Framing creates the inputs for several later phases, not only the next one. It should give each phase enough direction to start, while making clear which assumptions still need validation.

| Later phase                                     | What framing should provide                                                                       |
|-------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Phase 2 — Data and semantic readiness           | Priority questions, candidate sources, known data gaps, metric assumptions and semantic risks.    |
| Phase 3 — Governed data foundations             | Source-of-truth candidates, access boundaries and queryable data needs.                           |
| Phase 4 — Architecture and orchestration design | User channels, tool-use assumptions, query flow, validation, logging and integration constraints. |
| Phase 5 — Prototype build                       | Bounded MVP scope, first user group, expected answer formats and known limitations.               |

<span id="_Framing_activities_overview" class="anchor"></span>The full handover to later phases is consolidated in [Section 7.3](#handover-to-later-phases).

## 4 Framing activities overview

The framing phase is organised around nine activities. They provide a practical structure for the work, not a rigid delivery sequence. In a focused POC, several activities may be covered in the same workshop. In a higher-risk initiative, they may require separate sessions and deeper evidence.

The activities should be used to build a shared view of the opportunity, the constraints and the decisions still required. Their role is to turn a broad T2D idea into a bounded delivery scope, a set of testable assumptions and a clear set of outputs for the next phases.

### 4.1 Activity sequence

| Activity                               | Main question                                                                         | Indicative duration |
|----------------------------------------|---------------------------------------------------------------------------------------|---------------------|
| 1\. Business framing                   | Is there a real business reason for T2D, and where should it start?                   | 0.5–1 day           |
| 2\. User and workflow discovery        | Who will use it, how do they work today, and what is not working?                     | 1–2 days            |
| 3\. Initial data landscape scan        | Do plausible data sources or reporting assets exist?                                  | 0.5–1 day           |
| 4\. Initial semantic framing           | Are the key metrics, dimensions, filters and definitions likely to be usable?         | 0.5–1 day           |
| 5\. Security and governance framing    | Can the use case be exposed safely in principle?                                      | 0.5–1 day           |
| 6\. Solution architecture framing      | Is there a plausible technical route within enterprise constraints?                   | 0.5–1 day           |
| 7\. Delivery planning and MVP boundary | Can the first release be delivered within the expected timeline, budget and capacity? | 0.5–1 day           |
| 8\. Evaluation design framing          | Can correctness, usefulness and safe failure be tested?                               | 0.5–1 day           |
| 9\. Operating model framing            | Is there a credible route to support, monitor and improve the capability beyond POC?  | 0.5–1 day           |

The activities are connected. Business framing defines the initial scope, but user discovery may show that the selected workflow is weaker than expected. The data scan may show that the required sources exist, but semantic framing may reveal that the definitions are contested. Architecture may be feasible, but security may require a narrower access model. Evaluation planning may expose that the questions are too vague to test.

These loops are normal. The aim is not to complete each activity once and move on. The aim is to use the activities to refine the scope, expose trade-offs and strengthen the delivery decision.

The most useful framing discussions often happen at the boundaries between activities: a business question may look simple until the data team explains the grain, or a trusted report may become questionable once the metric owner explains exclusions.

The activities should not be treated as equal-risk checklist items. In most T2D initiatives, the areas most likely to change the framing decision are business value, semantic ambiguity, exposure risk, evaluation route and operating ownership.

### 4.2 Output need levels

Each activity should produce outputs at different levels of importance:

| Need level                       | Meaning                                                                           |
|----------------------------------|-----------------------------------------------------------------------------------|
| **Mandatory**                    | Required to exit framing and make a responsible decision.                         |
| **Recommended**                  | Strongly useful but may be simplified for a narrow POC.                           |
| **Optional / context-dependent** | Needed only for higher-risk, larger-scale, regulated or more complex initiatives. |

This distinction is important. Treating every output as mandatory makes framing too heavy. Treating every output as optional makes the decision unsafe. The need level should reflect the ambition, risk and intended use of the initiative.

Detailed question banks, templates and scorecards sit in the annexes; the main guide focuses on the decisions and outputs required to frame the initiative.

## 5 Framing activities

This chapter describes the nine activities used to frame a T2D initiative. Each activity should produce enough evidence to support the framing decision, while remaining proportionate to the ambition, risk and delivery stage.

Outputs use the need levels defined in [Chapter 4](#_Framing_activities_overview). Detailed question banks, example templates and extended scorecards are maintained in the [Phase 1 Annex Pack](https://d.docs.live.net/61FBE9373288B976/Desktop/decks/T2D/T2D%20-%20phase%201%20-%20Framing%20-%20Annexes.pdf).

### 5.1 Business framing

Business framing defines why T2D is being considered, where it should start and what value it should create. The goal is to confirm that T2D is being used to improve a real decision or workflow, not to justify a GenAI use case.

The output should be a bounded starting point: first domain, first users, priority questions, success criteria, risk appetite, budget envelope and decision ownership.

**Anchor questions**

- Why is T2D being considered now?

- Which decision or workflow should it improve?

- What is the smallest valuable scope that is worth testing?

**Outputs and need level**

| Output                       | Description                                                      | Need level                   |
|------------------------------|------------------------------------------------------------------|------------------------------|
| Problem statement            | Clear reason why T2D is being considered.                        | Mandatory                    |
| Priority domain              | First business area in scope.                                    | Mandatory                    |
| MVP scope                    | First users, questions, datasets and explicit exclusions.        | Mandatory                    |
| Success criteria             | Expected decision, time, quality, cost or risk benefit.          | Mandatory                    |
| Risk appetite                | Initial view of acceptable accuracy, exposure and autonomy risk. | Mandatory                    |
| Sponsor and decision owner   | Named owner for funding, priority and business decision.         | Mandatory                    |
| Budget envelope              | Initial view of discovery, POC / MVP and run-cost assumptions.   | Recommended                  |
| Longer-term ambition         | Direction beyond the first release.                              | Recommended                  |
| Full quantified benefit case | Detailed value model.                                            | Optional / context-dependent |

**  
**

**Watchpoints**

| Watchpoint                                        | Delivery risk                                                       | Framing response                                                                                                 |
|---------------------------------------------------|---------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Rationale is mainly “we need a GenAI use case”.   | The initiative may become technology-led rather than value-led.     | Clarify whether the objective is business value or structured learning, and adjust success criteria accordingly. |
| First domain is not agreed.                       | Scope, ownership and source-of-truth decisions may remain unstable. | Agree a first domain before moving into detailed readiness or build activity.                                    |
| Scope, budget or timeline are inconsistent        | The MVP may become too broad to deliver, govern or evaluate.        | Narrow the first release or position the work as a learning POC.                                                 |
| Success criteria are vague or purely qualitative. | The team may be unable to prove value or make informed trade-offs.  | Define measurable or observable success criteria linked to decision quality, speed, cost, risk or user value.    |
| No sponsor owns the value case.                   | Funding, prioritisation and decision ownership may be weak.         | Identify the sponsor or decision owner before proceeding.                                                        |

### 5.2 User and workflow discovery

User and workflow discovery develops an initial view of who may use the T2D capability, which workflows it may support, how users appear to get answers today, and where the current approach may be breaking down.

At framing stage, this view is often incomplete. Sponsor input should be treated as a hypothesis until tested with real users, analysts and workflow evidence.

The activity should identify the recurring questions and follow-up patterns that appear to create most of the value, while capturing edge cases carefully. Edge cases often explain why T2D may be more useful than a fixed dashboard, but they should still be classified as MVP, clarification/refusal/escalation, or later roadmap scope.

**Anchor questions**

- Who are the first users, and what decisions do they need to make?

- How do they get answers today, and where does the current approach break down?

- Which recurring questions or follow-up patterns create most of the value?

**Outputs and need level**

| Output                  | Description                                                            | Need level                   |
|-------------------------|------------------------------------------------------------------------|------------------------------|
| First user group        | Defined initial audience for POC / MVP.                                | Mandatory                    |
| Workflow description    | Current process and decision context.                                  | Mandatory                    |
| Priority question set   | Initial list of business questions to drive later phases.              | Mandatory                    |
| Current blockers        | Why current dashboards, reports or analyst workflows are insufficient. | Mandatory                    |
| Expected answer formats | Preferred output types for the first release.                          | Recommended                  |
| Trust requirements      | Source, caveat, freshness, definition or SQL visibility needs.         | Recommended                  |
| Human review cases      | Situations requiring analyst review, refusal or escalation.            | Recommended                  |
| User segmentation       | Differences by role, skill level, geography or channel.                | Optional / context-dependent |

**Watchpoints**

| Watchpoint                                                                 | Delivery risk                                                                         | Framing response                                                                                      |
|----------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| User understanding is based mainly on sponsor or senior stakeholder input. | Operational workarounds, analyst handoffs and exception cases may be missed.          | Treat the user view as a hypothesis and validate it with real users and analysts later.               |
| The first user group is broad or mixed.                                    | Question patterns, access needs and trust requirements may vary too much for one MVP. | Narrow the MVP audience or segment users by role, workflow or decision need.                          |
| Current workflow is only partly understood.                                | T2D may solve a perceived problem rather than a real workflow constraint.             | Capture workflow assumptions and validate them during discovery, prototype or pilot.                  |
| Questions are broad or uneven in quality.                                  | Data, semantic and evaluation work may lose focus.                                    | Prioritise the questions that best represent the value case and move weaker questions to the backlog. |
| Follow-ups and edge cases are unclear                                      | The team may overestimate conversational value or include unsafe scope.               | Capture likely follow-ups and classify edge cases as MVP, clarify/refuse/escalate, or roadmap.        |
| Trust requirements are unclear.                                            | Users may not rely on answers even when they are technically correct.                 | Capture likely trust needs such as source, caveat, freshness, definition or SQL visibility.           |

### 5.3 Initial data landscape scan

The data landscape scan identifies whether plausible sources, reports, marts, APIs or semantic assets exist to support the priority questions. It is not a full data readiness assessment. The aim is to identify candidate sources, known gaps, ownership, freshness, coverage and obvious blockers.

In many organisations, a report, dataset or dashboard may be described as “trusted” because it is widely used in decision-making, not because its definitions, lineage, controls or quality are fully understood. This distinction matters for T2D. A conversational system can make an informally trusted asset appear more authoritative than it really is, especially when answers are repeated, summarised or used outside the original reporting context.

Framing should therefore classify candidate sources by confidence level: approved, informally trusted, assumed trusted or needing validation. The aim is not to challenge every existing report, but to make delivery risk explicit. Where a source supports executive reporting, finance, performance management or commercial decisions, questioning its trust status may also have political implications. These risks should be captured early and carried into data and semantic readiness.

Where owners, lineage, refresh rules or known issues are undocumented, this should be captured explicitly. The aim is to identify what is known, what is assumed, who holds the knowledge and what must be validated in Phase 2.

**Anchor questions**

- Which sources, reports or datasets are likely to answer the priority questions?

- Who owns or understands those assets?

- What is known, assumed or risky about coverage, freshness, lineage, access or future evolution?

**Outputs and need level**

| Output                           | Description                                                                                                                     | Need level                   |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| Candidate source list            | Likely data sources, reports or semantic assets.                                                                                | Mandatory                    |
| Source ownership view            | Initial business and technical owners.                                                                                          | Mandatory                    |
| Source confidence classification | Whether each candidate source is approved, informally trusted, assumed trusted or requires validation before T2D can rely on it | Mandatory                    |
| Known data risks                 | Obvious quality, coverage, freshness or lineage concerns.                                                                       | Mandatory                    |
| Freshness and coverage view      | Whether data appears usable for the priority questions.                                                                         | Recommended                  |
| Reusable semantic assets         | Existing BI, metric, cube, dbt or semantic-layer assets.                                                                        | Recommended                  |
| Data change risks                | Planned migrations, ownership changes or model changes.                                                                         | Optional / context-dependent |

**Watchpoints**

| Watchpoint                                                          | Delivery risk                                                                                                      | Framing response                                                                                       |
|---------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Candidate sources are identified mainly through stakeholder memory. | The source view may be informal, incomplete or outdated.                                                           | Capture the assumption and validate source ownership, lineage and fitness in Phase 2.                  |
| A report is treated as trusted because it is widely used.           | Organisational trust may hide undocumented definitions, lineage gaps, manual adjustments or political sensitivity. | Classify the source as informally trusted and identify what must be validated before T2D relies on it. |
| Several reports appear to answer the same question.                 | Metrics, filters, refresh rules or grains may differ, creating inconsistent answers.                               | Record competing sources and identify a likely source-of-truth candidate for validation.               |
| Source ownership is unclear.                                        | Validation, access approval and issue resolution may stall.                                                        | Identify who likely holds the knowledge and assign follow-up ownership.                                |
| Lineage is not documented.                                          | Reported figures may not be traceable enough for trusted conversational answers.                                   | Treat lineage as a Phase 2 validation item.                                                            |
| Refresh rules are unclear.                                          | Data may not be timely enough for the target workflow.                                                             | Capture assumed freshness and validate it against user needs.                                          |
| Known quality issues are anecdotal.                                 | Delivery risk may be over- or under-estimated.                                                                     | Record known concerns and distinguish evidence from opinion.                                           |
| Required data sits across multiple domains.                         | Joins, grains, ownership and access controls may make the MVP too complex.                                         | Flag cross-domain scope and consider narrowing the first release.                                      |
| Existing semantic assets may be reusable.                           | Reuse may save effort, but hidden assumptions may be wrong.                                                        | List candidate assets and validate fitness in Phase 2.                                                 |
| Data access route is uncertain.                                     | A plausible source may still be difficult to query safely.                                                         | Capture access assumptions and align with security and architecture framing.                           |

### 5.4 Initial semantic framing

Initial semantic framing identifies the metrics, dimensions, filters, joins, grains and business definitions that may be required for the first T2D release.

At framing stage, the aim is not to finalise the semantic model. It is to expose ambiguity that may affect answer quality, access, evaluation or trust. Many semantic issues will be resolved later, but should be visible early enough to shape MVP scope and delivery assumptions.

Semantic ambiguity is a major T2D risk. If key business terms are not yet formally defined, the issue is not automatically fatal, but it must be made explicit. Later phases may need time to formalise definitions, agree owners, educate users and manage expectations as the capability moves toward production.

In practice, the hardest semantic issue is rarely whether a metric has a definition somewhere. It is whether the organisation agrees which definition is safe for this user group, this workflow and this answer context. Terms such as revenue, margin, customer, churn, stock or active user may each have several valid interpretations. T2D makes this risk more visible because conversational answers can sound definitive even when the underlying definition is contested.

**Anchor questions**

- Which metrics, dimensions and filters are needed for the priority questions?

- Which business terms are ambiguous or contested?

- Who can approve or challenge the working interpretation for the MVP?

**Outputs and need level**

| Output                           | Description                                               | Need level                   |
|----------------------------------|-----------------------------------------------------------|------------------------------|
| Priority metric list             | Metrics needed for first-release questions.               | Mandatory                    |
| Semantic risk log                | Ambiguous terms, contested definitions and unsafe joins.  | Mandatory                    |
| Initial definition assumptions   | Working assumptions for MVP interpretation.               | Mandatory                    |
| Metric / semantic owners         | People or forums needed to approve definitions.           | Mandatory                    |
| Candidate source-of-truth assets | Reports, models or datasets likely to anchor definitions. | Recommended                  |
| Known filters and exclusions     | Standard exclusions and business rules.                   | Recommended                  |
| Example approved questions       | Questions that can later support evaluation.              | Recommended                  |
| Draft metric cards               | Early metric-level artefacts.                             | Optional / context-dependent |

**Watchpoints**

| Watchpoint                                                 | Delivery risk                                                                          | Framing response                                                                                   |
|------------------------------------------------------------|----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| Key terms have different meanings across teams.            | The system may give definitive-sounding answers using the wrong interpretation.        | Capture the ambiguity and define whether the MVP should answer, clarify, caveat, exclude or defer. |
| Definitions are held in reports, SQL or analyst knowledge. | The system may depend on undocumented logic that is difficult to validate or maintain. | Identify likely owners and carry validation into Phase 2.                                          |
| Metric ownership is unclear.                               | Semantic decisions may stall or remain implicit in prompts, SQL or analyst judgement.  | Identify a provisional owner or decision forum.                                                    |
| Joins, grains or filters are unclear.                      | Query correctness may be unreliable even when the right source is used.                | Flag as a semantic readiness risk and narrow scope if needed.                                      |
| Multiple “official” sources exist.                         | Source-of-truth decisions may become political or delay delivery.                      | Record competing sources and identify what must be validated.                                      |
| The MVP depends on highly contested metrics.               | The first release may become too risky, slow or politically difficult to approve.      | Consider simpler metrics, a narrower domain or deferring the contested area.                       |
| Stakeholders treat semantic disagreement as a model issue. | The team may overestimate what the LLM can safely resolve.                             | Make semantic ownership and approval needs explicit.                                               |

### 5.5 Security and governance framing

Security and governance framing identifies early access, privacy, compliance, audit and exposure constraints that may affect the T2D initiative.

At framing stage, the aim is not to complete a full security or compliance review. It is to understand whether the use case can be exposed safely, which controls matter, who must approve the risk posture, and what needs deeper validation before prototype, MVP or pilot.

T2D changes the interaction model with data. Users may ask follow-up questions, combine filters, request breakdowns or infer information through repeated queries. Framing should therefore consider not only what users can see directly, but also what they may be able to infer.

For T2D, security risk is not limited to whether a user can access a table or dashboard. Users may infer restricted information through repeated filters, narrow cohorts, comparisons over time or follow-up questions. Framing should therefore consider both direct access and conversational exposure: what users can see, what they can combine, and what they may be able to infer.

**Anchor questions**

- Can the use case be exposed safely in principle?

- Which access, privacy, compliance, audit or inference risks could affect the MVP?

- Who needs to approve the risk posture before prototype, MVP or pilot?

**Outputs and need level**

| Output                              | Description                                                  | Need level                   |
|-------------------------------------|--------------------------------------------------------------|------------------------------|
| Initial access model                | Authentication, authorisation and permission assumptions.    | Mandatory                    |
| Sensitive-data view                 | Initial classification of data exposure risks.               | Mandatory                    |
| Governance approval route           | Owners or forums required for risk approval.                 | Mandatory                    |
| Exposure-risk assumptions           | Inference, aggregation and repeated-query risks.             | Mandatory                    |
| Logging and audit assumptions       | What should be captured and reviewed.                        | Recommended                  |
| Retention and redaction assumptions | Prompt, SQL, result and feedback retention needs.            | Recommended                  |
| Model / vendor policy view          | Whether provider, endpoint or data policy constraints apply. | Recommended                  |
| Formal compliance mapping           | Detailed regulatory mapping.                                 | Optional / context-dependent |

**Watchpoints**

| Watchpoint                                           | Delivery risk                                                                           | Framing response                                                                  |
|------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Security or governance stakeholders are not engaged. | Approval may fail late or require major redesign.                                       | Identify likely reviewers and when they need to be involved.                      |
| Access rules are assumed rather than validated.      | The system may expose data outside existing permission boundaries.                      | Capture assumptions and validate access inheritance in later phases.              |
| Sensitive data may be in scope.                      | Privacy, compliance, contractual or commercial constraints may affect feasibility.      | Classify the data and consider narrowing, masking, aggregation or exclusion.      |
| The use case relies on broad service-account access. | Existing user-level controls may be bypassed.                                           | Assess inherited permissions or policy-layer controls and flag likely exceptions. |
| Inference risk is not yet understood.                | Users may infer restricted information through filters, cohorts or follow-up questions. | Treat inference through aggregation and multi-turn use as a validation item.      |
| Logging requirements are unclear.                    | Audit, debugging, evaluation and support may be weak.                                   | Capture minimum logging assumptions and carry details into architecture design.   |
| Model or vendor policy is uncertain.                 | Data or metadata sharing may breach enterprise policy.                                  | Identify approved routes and open policy questions.                               |
| No clear risk acceptance route exists.               | Decisions may stall or become implicit.                                                 | Identify the likely risk owner or approval forum.                                 |

### 5.6 Solution architecture framing

Solution architecture framing tests whether there is a plausible technical route for the T2D initiative within enterprise constraints. The purpose is not to design the target architecture. It is to confirm that a plausible controlled route exists for model access, metadata retrieval, query validation, execution, logging and deployment.

At framing stage, the aim is to identify the main assumptions around user interface, model access, data connectivity, tool use, query validation, logging, deployment and operational constraints. These assumptions should be detailed enough to shape the MVP and avoid proposing a route that later conflicts with security, platform or architecture standards.

Architecture approval is not only a formal process. In many organisations, feasibility also depends on established platform patterns, preferred technologies and the views of senior architects. Early engagement reduces the risk of late challenge.

**Anchor questions**

- Is there a plausible technical route for the MVP within enterprise constraints?

- Which user channel, model route, data access path and deployment pattern are realistic?

- What architecture assumptions could materially affect scope, timeline, cost or approval?

**Outputs and need level**

| Output                           | Description                                                       | Need level                   |
|----------------------------------|-------------------------------------------------------------------|------------------------------|
| Initial architecture assumptions | High-level view of user channel, model, data and orchestration.   | Mandatory                    |
| Model / provider assumption      | Approved or candidate LLM route.                                  | Mandatory                    |
| Data access route                | Candidate query path through governed data or semantic layer.     | Mandatory                    |
| Query validation approach        | Initial control assumptions for generated queries.                | Mandatory                    |
| Deployment route                 | Likely environment and release path.                              | Recommended                  |
| Observability assumptions        | Logging, cost, latency, errors and feedback needs.                | Recommended                  |
| Integration constraints          | Dependencies on identity, BI, warehouse, API or platform tooling. | Recommended                  |
| Non-functional view              | Initial latency, scalability, resilience and cost expectations.   | Optional / context-dependent |

**Watchpoints**

| Watchpoint                                                | Delivery risk                                                        | Framing response                                                                        |
|-----------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| No approved model or provider route is clear.             | The team may be unable to build or deploy within policy.             | Identify candidate routes and carry approval into architecture and security validation. |
| The proposed flow requires unrestricted data access.      | Governance and exposure risks may become unacceptable.               | Assess whether data scope, tools or query boundaries need to be narrowed.               |
| Query validation is not considered.                       | Incorrect, unsafe or high-cost queries may reach production systems. | Capture query validation as a core architecture assumption.                             |
| Tool boundaries are unclear.                              | The system may gain broader capability than intended.                | Identify which tools are likely in or out of scope for POC or MVP.                      |
| Architecture depends on unapproved tools or platforms.    | Delivery may be delayed or blocked by standards review.              | Identify approved patterns or engage architecture owners early.                         |
| Logging and observability are treated as later additions. | Quality, cost, audit and support issues may be invisible.            | Capture minimum logging and monitoring assumptions early.                               |
| Deployment route is unclear.                              | The prototype may have no credible route to pilot or production.     | Clarify likely environment, release and approval assumptions.                           |
| Non-functional expectations are not discussed.            | Latency, cost, reliability or support needs may be underestimated.   | Capture early NFR assumptions and validate them in later phases.                        |

### 5.7 Delivery planning and MVP boundary

MVP delivery planning converts the framed scope into an initial delivery view: what will be built first, what will be excluded, which workstreams are needed, which assumptions must be tested, and whether the ambition is credible within the available timeline, budget and capacity.

At framing stage, the plan should be directional rather than fixed. Data, semantic, security, architecture and user constraints may still change the delivery path. The purpose is to test whether ambition and delivery reality are broadly aligned.

The plan should avoid false confidence about production. A POC or early MVP may prove feasibility and value, but production readiness usually requires further work on governance, evaluation, monitoring, support, cost control, access management and ownership.

**Anchor questions**

- What is the smallest valuable first-release scope that can test the use case?

- Is the proposed MVP or first release credible within the expected timeline, budget and capacity?

- Which assumptions could materially change the plan?

**Outputs and need level**

| Output                 | Description                                                  | Need level                   |
|------------------------|--------------------------------------------------------------|------------------------------|
| MVP boundary           | Users, domains, questions, data and answer types in scope.   | Mandatory                    |
| Initial delivery plan  | Directional timeline and workstream view.                    | Mandatory                    |
| Key dependencies       | Data, security, architecture, SME and platform dependencies. | Mandatory                    |
| Delivery capacity view | Initial team and role assumptions.                           | Mandatory                    |
| Budget envelope        | Initial cost assumptions for POC / MVP and later scale.      | Recommended                  |
| Governance gates       | Expected approvals for prototype, pilot and production.      | Recommended                  |
| Initial backlog        | Epics or high-level delivery items.                          | Recommended                  |
| Production path sizing | Indicative view of what moving beyond MVP may require.       | Optional / context-dependent |

**Watchpoints**

| Watchpoint                                         | Delivery risk                                                        | Framing response                                                                          |
|----------------------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| MVP scope is still open-ended.                     | Delivery cannot be planned, controlled or evaluated.                 | Narrow users, domains, questions or answer types before build.                            |
| Timeline is fixed before key risks are understood. | The plan may ignore data, semantic, security or architecture effort. | Treat the timeline as provisional and identify assumptions that could change it.          |
| Budget excludes non-model work.                    | True delivery cost may be understated.                               | Include data, semantics, evaluation, governance, monitoring, support and platform effort. |
| Business or data capacity is unavailable.          | Delivery may stall even if the technical route is viable.            | Identify minimum SME, data owner and analyst involvement.                                 |
| Production is assumed after POC.                   | Stakeholders may confuse feasibility with readiness.                 | Make POC, MVP, pilot and production-readiness criteria distinct.                          |
| Governance gates are unclear.                      | Approval delays may block delivery later.                            | Identify likely approval forums and decision points.                                      |
| Dependencies sit outside the project team.         | Delivery may depend on teams with different priorities.              | Record dependencies and likely escalation or sequencing assumptions.                      |

### 5.8 Evaluation design framing

Evaluation design framing defines the initial approach for testing whether T2D answers are correct, useful and safe enough for the intended use case.

At framing stage, the team does not need a complete evaluation set. It should identify candidate question types, likely expected-answer sources, initial quality criteria and provisional evaluation ownership. The aim is to make evaluation a design input, not a post-build activity.

Evaluation should eventually cover more than final answer accuracy, including query correctness, metric interpretation, access behaviour, clarification, refusal, explanation quality and user understanding of assumptions.

**Anchor questions**

- What evidence will show that answers are correct, useful and safe enough?

- Which candidate questions and expected-answer sources can be used for testing?

- Who owns evaluation design and quality sign-off?

**Outputs and need level**

| Output                     | Description                                                                    | Need level                   |
|----------------------------|--------------------------------------------------------------------------------|------------------------------|
| Evaluation approach        | Initial view of how quality and safety will be tested.                         | Mandatory                    |
| Candidate test questions   | Early questions that can become golden questions.                              | Mandatory                    |
| Expected-answer sources    | Reports, SQL, SMEs or systems used to validate answers.                        | Mandatory                    |
| Evaluation owner           | Named person or group responsible for quality evidence.                        | Mandatory                    |
| Failure categories         | Wrong metric, wrong filter, unsafe answer, hallucination, refusal failure etc. | Recommended                  |
| Acceptance criteria        | Initial thresholds or qualitative standards for POC / MVP.                     | Recommended                  |
| Regression-test assumption | View of how changes will be retested over time.                                | Optional / context-dependent |

**  
**

**Watchpoints**

| Watchpoint                                                | Delivery risk                                                       | Framing response                                                                            |
|-----------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Evaluation is treated as something to define after build. | Quality may not shape the design early enough.                      | Position evaluation as a design input for later phases.                                     |
| Expected-answer sources are unclear.                      | Correctness may be hard to assess consistently.                     | Identify likely reports, SQL, SMEs or reconciliation sources to validate later.             |
| Candidate questions are broad or uneven.                  | Testing may become subjective or hard to repeat.                    | Convert the most important questions into testable examples.                                |
| Early evaluation examples are mostly happy-path.          | Failure modes may be underrepresented.                              | Plan to include ambiguity, access, refusal and edge-case scenarios later.                   |
| Evaluation focuses mainly on final answers.               | Query, access, clarification and safe-failure issues may be missed. | Capture the need to evaluate query logic, permissions, clarification and refusal behaviour. |
| Evaluation ownership is unclear.                          | Quality evidence may remain informal.                               | Identify a provisional owner or decision forum.                                             |
| Regression testing is not considered.                     | Future changes may break previously correct behaviour.              | Capture repeatable testing as a later-phase requirement.                                    |

### 5.9 Operating model framing

Operating model framing identifies whether there is a credible route to support, monitor and improve the T2D capability if it moves beyond POC.

At framing stage, the operating model does not need to be designed in detail. The aim is to form an early view of likely ownership, monitoring, support, semantic maintenance, change control and run-cost implications. These points should be visible early because they affect whether the initiative should proceed, remain a learning POC, or require further work before pilot or production.

If no operating route is visible, the initiative may still proceed as a POC, but it should not be presented as having a credible path to production until ownership and support questions are better understood.

**Anchor questions**

- Who is likely to own the capability if it moves beyond POC?

- What would that owner need to be accountable for?

- Who would maintain metric definitions, caveats and source mappings?

- What answer-quality, usage, failure, access, cost or latency signals may need to be monitored later?

- How might users report wrong, unclear, incomplete or unsafe answers?

- What types of prompt, model, data, tool or semantic changes may require testing and approval?

- What run-cost drivers could affect the decision to continue, pilot or productionise?

**Outputs and need level**

| Output                             | Description                                                                                                                                   | Need level                   |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| Provisional operating owner        | Likely team, role or ownership option for the capability beyond POC.                                                                          | Mandatory                    |
| Operating accountability view      | Initial view of who may own answer quality, support, semantic maintenance, security review, cost and improvement.                             | Mandatory                    |
| Semantic maintenance route         | Early view of who would maintain metric definitions, caveats, source mappings and semantic assumptions.                                       | Mandatory                    |
| Support and escalation assumptions | Initial view of how users may report wrong answers, unclear answers, access issues or unsafe responses.                                       | Recommended                  |
| Monitoring assumptions             | Early view of what may need to be monitored: usage, failed questions, answer quality, cost, latency, access events, errors and user feedback. | Recommended                  |
| Change-control assumptions         | Initial view of which changes to prompts, models, tools, data, semantic definitions or evaluation sets may need testing and approval.         | Recommended                  |
| Run-cost assumptions               | Early view of model, warehouse, platform, monitoring, support, evaluation and SME effort costs.                                               | Recommended                  |
| Regression-test assumption         | Initial view of whether golden questions and safe-failure tests may need to become a repeatable test set after launch.                        | Recommended                  |
| Adoption assumptions               | Initial view of training, communications, caveats, analyst involvement and trust-building needs.                                              | Optional / context-dependent |

**Watchpoints**

| Watchpoint                                               | Delivery risk                                                                                      | Framing response                                                                                          |
|----------------------------------------------------------|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Ownership beyond POC is unclear.                         | The prototype may have no credible route to service.                                               | Identify likely ownership options and keep the initiative positioned as a POC until ownership is clearer. |
| Operating accountability is assumed rather than named.   | Answer quality, user support, cost, semantic maintenance and access review may fall between teams. | Capture provisional accountability assumptions and validate them in later phases.                         |
| Semantic maintenance is treated as a one-off build task. | Metrics, definitions, caveats and source mappings may drift after launch.                          | Identify likely semantic owners and carry maintenance design into productionisation.                      |
| Monitoring is limited to technical uptime.               | Usage, failed questions, wrong answers, unsafe requests, cost and trust issues may be invisible.   | Capture monitoring needs across quality, usage, cost, latency, access and feedback.                       |
| Support route is unclear.                                | Users may lose trust if wrong or unclear answers cannot be reported and resolved.                  | Identify likely issue intake, triage, escalation and communication assumptions.                           |
| Change control is not considered.                        | Prompt, model, data, tool or semantic changes may break previously correct behaviour.              | Capture the need for regression testing and release control in later phases.                              |
| Run cost is treated as model cost only.                  | Warehouse queries, logging, monitoring, evaluation, platform and support effort may be missed.     | Capture full operating cost drivers, not only LLM or API usage.                                           |
| Adoption is assumed.                                     | Users may over-trust, under-trust or misuse the capability.                                        | Treat training, caveats, analyst involvement and feedback as later adoption requirements.                 |
| Production is assumed after a successful prototype.      | A working demo may not be supportable, governable or economically viable.                          | Keep POC, pilot and production-readiness expectations distinct.                                           |

**Practitioner note**

At framing stage, the operating model is a direction-of-travel test. The team does not need the final support model, monitoring process or release governance. It does need an early view of who could inherit the service, what they would need to run it safely, and whether those needs are realistic.

## 6 Framing decision pack

The output of Phase 1 should be a decision pack, not a large discovery report. It should contain enough evidence for stakeholders to decide whether to proceed, narrow, pause, redirect or stop, and enough context for later phases to validate the remaining assumptions.

The value of framing is not the number of artefacts produced. A long pack of weak outputs is less useful than a short set of clear assumptions, decisions and risks. The strongest framing outputs help the team make trade-offs: what to build first, what to exclude, what must be validated, and what would cause the initiative to change direction.

Detailed templates and examples are maintained in the Phase 1 Annex Pack.

| Output                            | Purpose                                                                                              | Need level  | Main downstream use                              |
|-----------------------------------|------------------------------------------------------------------------------------------------------|-------------|--------------------------------------------------|
| Problem statement                 | Explains why T2D is being considered and which decision or workflow it should improve.               | Mandatory   | Business framing, MVP scope, success criteria    |
| MVP scope                         | Defines first users, domains, questions, data areas, answer types and explicit exclusions.           | Mandatory   | Delivery planning, architecture, prototype build |
| Priority question set             | Captures the initial business questions and follow-up patterns that drive value.                     | Mandatory   | Data readiness, semantics, evaluation, prototype |
| User and workflow hypothesis      | Describes the first users, current process, blockers and expected value.                             | Mandatory   | User validation, adoption, answer design         |
| Candidate source view             | Lists likely reports, datasets, marts, APIs or semantic assets and their validation status.          | Mandatory   | Data and semantic readiness                      |
| Semantic risk view                | Captures ambiguous terms, contested definitions, filters, joins, grains and ownership gaps.          | Mandatory   | Semantic readiness, evaluation, MVP scoping      |
| Access and exposure assumptions   | Defines initial access, privacy, audit, sensitive-data and inference-risk assumptions.               | Mandatory   | Security validation, architecture design         |
| Architecture assumptions          | Captures initial model, tool-use, data access, query validation, logging and deployment assumptions. | Mandatory   | Architecture and orchestration design            |
| Evaluation approach               | Defines how correctness, usefulness and safe failure may be tested.                                  | Mandatory   | Evaluation design, pilot readiness               |
| Delivery stance and dependencies  | Provides directional timeline, workstreams, capacity needs, blockers and dependencies.               | Mandatory   | MVP planning, budget, governance                 |
| Ownership view                    | Identifies provisional owners for value, scope, data, semantics, risk, evaluation and operation.     | Mandatory   | Decision gates, delivery governance              |
| Budget envelope                   | Captures early cost assumptions for POC / MVP and likely productionisation drivers.                  | Recommended | Funding, delivery planning                       |
| Operating assumptions             | Captures likely support, monitoring, semantic maintenance, feedback and run-cost needs.              | Recommended | Pilot and production readiness                   |
| Risk, decision and assumption log | Records material risks, decisions made, open assumptions and validation actions.                     | Mandatory   | All later phases                                 |
| Longer-term ambition              | Describes the likely direction beyond the first release without over-expanding the MVP.              | Recommended | Roadmap, stakeholder alignment                   |

### 6.1 Decision-pack quality test

Each output should be tested against three questions:

| Test                | Question                                                                                                       |
|---------------------|----------------------------------------------------------------------------------------------------------------|
| Decision usefulness | Does this output help decide whether to proceed, narrow, pause, redirect or stop?                              |
| Delivery usefulness | Does this output guide at least one later phase?                                                               |
| Assumption clarity  | Does this output make clear what is known, assumed, risky or still to be validated?                            |
| Handover clarity    | Can the next phase tell what to validate, refine or challenge without rediscovering the use case from scratch? |

An output that does not support a decision or later delivery activity should either be simplified or moved to the annex pack.

## 7 Exit criteria and handover

The framing phase should end with a clear decision, a bounded scope and a practical handover into later phases. It should not end with a general recommendation to continue discovery.

Exit does not mean that all questions have been resolved. It means the team has enough evidence to decide whether to proceed, narrow, pause, redirect or stop, and enough clarity to know what must be validated next.

### 7.1 Readiness check before exit

Before exiting framing, the team should test the framing outputs against the minimum conditions in [Section 3.2](#minimum-conditions-to-proceed).

This check should support judgement, not replace it. The team should not average the answers or treat the review as a scoring exercise. One material weakness can outweigh several positive signals. For example, strong business value does not compensate for unmanaged exposure risk, and a promising prototype path does not compensate for unclear ownership.

| Area                    | Exit question                                                                                        |
|-------------------------|------------------------------------------------------------------------------------------------------|
| Business value          | Is there enough evidence that T2D may improve a real decision or workflow?                           |
| User and workflow       | Are the first users, current blockers and priority questions understood well enough to proceed?      |
| MVP scope               | Are the first release and explicit exclusions clear?                                                 |
| Data and semantics      | Are candidate sources, metric assumptions and semantic risks visible?                                |
| Security and governance | Are access, privacy, audit and exposure assumptions clear enough for deeper validation?              |
| Architecture            | Is there a plausible technical route within enterprise constraints?                                  |
| Evaluation              | Is there a credible route to test correctness, usefulness and safe failure?                          |
| Delivery                | Are timeline, budget, capacity and dependencies broadly understood?                                  |
| Ownership               | Are provisional owners identified for value, scope, data, semantics, risk, evaluation and operation? |

The exit decision should identify any unresolved weakness clearly and state whether it leads to a decision to proceed, narrow, pause, redirect or stop.

### 7.2 Required exit outputs

The required exit outputs are the minimum version of the framing decision pack described in [Section 6](#framing-activities):

| Output                            | Minimum expectation                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------|
| Framing decision                  | Proceed, narrow, pause, redirect or stop.                                                     |
| MVP scope                         | First users, priority questions, data areas, answer types and exclusions.                     |
| Priority question set             | Initial questions and follow-up patterns to drive later phases.                               |
| User and workflow hypothesis      | First view of users, current process, blockers and value.                                     |
| Candidate source view             | Likely sources, reports, datasets or semantic assets and validation needs.                    |
| Semantic risk view                | Ambiguous terms, contested metrics, filters, joins, grains and owners.                        |
| Security and exposure assumptions | Initial access, privacy, audit, sensitive-data and inference-risk assumptions.                |
| Architecture assumptions          | Initial view of model route, tool use, data access, query validation, logging and deployment. |
| Evaluation approach               | Candidate test questions, expected-answer sources and quality dimensions.                     |
| Delivery plan                     | Directional timeline, workstreams, dependencies, capacity and budget envelope.                |
| Ownership view                    | Provisional owners for key decisions and later validation.                                    |
| Risk, decision and assumption log | Material risks, decisions made, open assumptions and follow-up actions.                       |

### 7.3 Handover to later phases

The handover from framing should make clear what later phases are expected to validate, refine or challenge. Although Phase 1 primarily informs the immediate readiness, architecture and prototype work, its outputs should also create a traceable line of sight to pilot, productionisation and adoption.

| Later phase                                     | Handover focus                                                                                                                                                      |
|-------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Phase 2 — Assess data and semantics             | Validate candidate sources, ownership, metric definitions, grains, joins, filters, known data gaps and semantic risks.                                              |
| Phase 3 — Build governed foundations            | Confirm source-of-truth assets, queryable data structures, access boundaries, approved metrics and data controls.                                                   |
| Phase 4 — Design architecture                   | Refine model route, tool boundaries, metadata retrieval, query validation, logging, deployment and integration design.                                              |
| Phase 5 — Prototype build                       | Build against the MVP scope, first user group, expected answer formats, known limitations, operating assumptions and governance expectations.                       |
| Phase 6 — Validation, assurance and remediation | Test and remediate access, exposure, answer quality, query correctness, refusal, clarification, logging and failure modes.                                          |
| Phase 7 — Pilot                                 | Use the framed user group, workflow hypothesis, success criteria and known limitations to test the capability in controlled real-world use.                         |
| Phase 8 — Production readiness                  | Use the ownership view, operating assumptions, governance route, run-cost assumptions and validation evidence to prepare for live operation.                        |
| Phase 9 — Run, adopt and improve                | Use the priority question set, feedback routes, semantic ownership and evaluation approach to support adoption, monitor trust and improve the capability over time. |

### 7.4 Exit decision wording

The exit decision should apply the outcome model defined in Section 3.1. It should be written plainly and should avoid vague wording such as “continue discovery” or “progress subject to alignment.”

| Decision | Example wording                                                                                                |
|----------|----------------------------------------------------------------------------------------------------------------|
| Proceed  | Proceed to the next delivery phases with the agreed MVP scope, assumptions and validation actions.             |
| Narrow   | Proceed only after narrowing the MVP scope to the agreed users, questions, domains or data areas.              |
| Pause    | Pause delivery until the named blocker is resolved.                                                            |
| Redirect | Redirect the need to a dashboard, reporting, semantic-layer, data-governance or analyst-workflow intervention. |
| Stop     | Stop this T2D use case because the value, feasibility or risk position is not strong enough.                   |

### 7.5 Practitioner note

A good framing exit is not a long pack. It is a clear decision with traceable assumptions. The strongest handover is one where the next team can see exactly what is known, what has been assumed, what remains risky and what would cause the scope, timeline or delivery approach to change.

## 8 Key risks and failure modes

Framing should make the main delivery risks visible early enough to shape scope, ownership and the next validation steps. It does not remove these risks, but it should prevent the team from moving into build with major uncertainty hidden or ignored.

| Risk / failure mode               | Why it matters                                                                                                     | Framing response                                                                                             |
|-----------------------------------|--------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| **Technology-led initiative**     | T2D is pursued because GenAI is attractive, not because there is a clear decision workflow.                        | Clarify whether the objective is business value or structured learning; adjust success criteria accordingly. |
| **Unclear user group**            | A generic “business user” audience leads to unfocused scope, weak adoption and poor evaluation.                    | Define the first user group or narrow the POC.                                                               |
| **Weak workflow fit**             | The current problem may be better solved through dashboards, reporting, semantic-layer fixes or analyst workflows. | Test whether conversation adds value beyond existing channels.                                               |
| **Scope expansion**               | Too many users, domains, metrics or answer types make the MVP difficult to deliver and evaluate.                   | Reduce the first release to the smallest valuable scope.                                                     |
| **Assumed trusted data**          | Reports or datasets may be widely used but not formally controlled, documented or fit for T2D.                     | Capture trusted-status assumptions and validate them in later phases.                                        |
| **Semantic ambiguity**            | Metrics, filters, joins, grains or business terms may be interpreted inconsistently.                               | Make ambiguity explicit and identify owners or working MVP assumptions.                                      |
| **Unsafe exposure**               | Users may see or infer sensitive information through filters, aggregates or follow-up questions.                   | Identify access and inference risks before prototype or MVP design.                                          |
| **Weak evaluation route**         | The team may not know how to test correctness, usefulness, refusal or safe failure.                                | Identify candidate test questions, expected-answer sources and evaluation ownership.                         |
| **Unrealistic delivery envelope** | Timeline, budget or capacity may not match the ambition.                                                           | Re-scope, adjust the plan or position the work as a learning POC.                                            |
| **No operating route**            | A promising prototype may have no team to support, monitor or improve it.                                          | Identify likely ownership options and run-cost drivers before progressing too far.                           |

### 8.1 Practitioner note

Most weak T2D initiatives do not fail because the first prototype cannot answer anything. They fail because the prototype answers enough to look promising, but not enough to be trusted, governed, evaluated or operated. Framing should therefore focus less on whether a demo can be built and more on whether the organisation has a credible route from demo to controlled capability.

[^1]: The most useful framing decision is often not a simple “go” or “no go”. Many T2D ideas are directionally valuable but initially too broad: too many users, too many domains, too many metrics, too many data sources and too many answer types. In those cases, narrowing the first release is not a lack of ambition. It is the delivery discipline that gives the initiative a realistic chance of becoming trusted, evaluated and operated.

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
