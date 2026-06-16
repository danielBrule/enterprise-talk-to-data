# Talk-to-Data Delivery Blueprint — Phase 2: Data & Semantic Readiness Assessment

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
- [3 Readiness decision and delivery implications](#3-readiness-decision-and-delivery-implications)
  - [3.1 Possible Phase 2 outcomes](#31-possible-phase-2-outcomes)
  - [3.2 Minimum conditions to proceed](#32-minimum-conditions-to-proceed)
  - [3.3 Common reasons to narrow, remediate, defer or stop](#33-common-reasons-to-narrow-remediate-defer-or-stop)
  - [3.4 How Phase 2 shapes later phases](#34-how-phase-2-shapes-later-phases)
- [4 Data and semantic readiness activities overview](#4-data-and-semantic-readiness-activities-overview)
  - [4.1 Activity sequence](#41-activity-sequence)
  - [4.2 Activity logic](#42-activity-logic)
  - [4.3 Practitioner note](#43-practitioner-note)
- [5 Core readiness activities](#5-core-readiness-activities)
  - [5.1 Validate source inventory](#51-validate-source-inventory)
  - [5.2 Map questions to data](#52-map-questions-to-data)
  - [5.3 Review data model readiness](#53-review-data-model-readiness)
  - [5.4 Confirm semantic definitions](#54-confirm-semantic-definitions)
  - [5.5 Assess data gaps and quality](#55-assess-data-gaps-and-quality)
  - [5.6 Assess metadata and lineage](#56-assess-metadata-and-lineage)
  - [5.7 Review access and exposure](#57-review-access-and-exposure)
  - [5.8 Consolidate readiness gaps](#58-consolidate-readiness-gaps)
- [6 Answerability decision pack](#6-answerability-decision-pack)
  - [6.1 Answerability matrix](#61-answerability-matrix)
  - [6.2 Answerability pack quality test](#62-answerability-pack-quality-test)
- [7 Exit criteria and handover](#7-exit-criteria-and-handover)
  - [7.1 Required exit outputs](#71-required-exit-outputs)
  - [7.2 Handover to later phases](#72-handover-to-later-phases)
- [8 Key risks and failure modes](#8-key-risks-and-failure-modes)
  - [8.1 Practitioner note](#81-practitioner-note)

---

## 1 Executive summary

Phase 2 tests whether the framed Talk-to-Data questions are answerable from trusted data, approved definitions, safe joins, usable metadata and enforceable access rules.

The phase starts from the priority users, questions and MVP boundary agreed during framing. Its purpose is to determine whether the required data, definitions, joins, filters and access rules can support those questions reliably enough for the next delivery stage. The expected output is a clear answerability evidence base: known sources, semantic definitions, data gaps, ownership, access constraints, metadata gaps, semantic risks and candidate golden questions.

This is not a generic data discovery exercise. For Talk-to-Data, the question is not simply whether data exists. The question is whether the system can use that data safely and consistently to answer business questions. A dataset may be available, but still unsuitable if the metric definition is contested, the grain is unclear, the join path is unsafe, the filters are informal, ownership is weak or access rules cannot be enforced.

Phase 2 is therefore both a readiness gate and a scope-shaping exercise. It should classify each priority question as ready for MVP, ready with caveats, dependent on remediation, deferred or out of scope. Where questions are not ready, the phase should capture the reason, required changes, owner and likely route back into a future backlog. The aim is to separate what is safe to build now from what could become viable later with stronger data, clearer definitions, approved joins, better metadata, improved quality controls or revised access rules.

This matters because a fluent prototype can hide weak foundations. It is better to challenge assumed “trusted” sources, expose semantic ambiguity and remove unsafe questions early than to build an interface that returns plausible but wrong answers later. In T2D, production risk is rarely caused by the model alone. It usually comes from weak data foundations, unclear definitions, unsafe query paths and unresolved ownership.

By the end of Phase 2, senior stakeholders should be able to say which priority questions can be supported now, which require caveats or remediation, which should move to the backlog, which data sources should be used, which gaps must be closed, and whether the use case is ready to proceed, narrow, pause or defer.

The core output is an answerability matrix that forces a clear MVP-readiness decision for each priority question: ready or not ready. Caveats, remediation actions, backlog routes and exclusions should explain the decision, not replace it.

## 2 Phase overview

Phase 2 turns the assumptions from framing into evidence. It tests whether the scoped T2D use case has a credible path through the organisation’s data, definitions, joins, filters and access rules.

The phase should expose the gap between a narrow POC that can demonstrate value and a capability that can scale safely. The key discipline is to avoid treating “data exists” as readiness. For T2D, readiness means the system can use the right source, definition, grain, join path, filter and access rule consistently enough to produce trusted answers.

### 2.1 Objective

The objective of Phase 2 is to produce an answerability matrix for the priority T2D questions. Each question should be classified as ready for MVP, ready with caveats, dependent on remediation, deferred or out of scope, with the evidence, caveats, owners and required actions captured. To produce this view, Phase 2 should confirm:

- **Known sources:** which systems, tables, marts, reports, APIs and semantic assets are relevant to the use case, and which are trusted enough to support MVP answers.

- **Semantic definitions:** which KPIs, measures, business terms, calculations, filters, dimensions, synonyms and caveats are approved, contested or missing.

- **Data model readiness:** whether grains, keys, relationships, joins, date logic and aggregation rules are understood well enough for safe querying.

- **Data gaps:** which missing, incomplete, stale or unreliable data issues affect answer quality.

- **Ownership:** who owns the sources, definitions, quality issues and access rules.

- **Access constraints:** what target users are allowed to see, including row, column, aggregation and inference risks.

- **Evaluation eligibility:** which priority questions have enough source, definition, grain, filter, caveat and access clarity to become candidate golden questions.

The depth of Phase 2 should reflect the delivery intent. A discovery or POC may require enough validation to support safe learning with clear caveats. An MVP / pilot / production path requires stronger evidence on trust, definitions, data model safety, quality, access and ownership.

### 2.2 Scope of the phase

Phase 2 should remain bounded to the framed use case, priority users and priority question set. It should not become a broad enterprise data assessment or a general data governance review.

The phase covers only the evidence needed to decide MVP inclusion, caveats, remediation, backlog or exclusion. This includes material risks around source trust, semantic ambiguity, grain, joins, lineage, quality, access and ownership.

The test for inclusion is simple: if an issue materially affects whether the T2D system can answer the scoped questions safely, consistently or explainably, it belongs in Phase 2.

### 2.3 What this phase does not do

Phase 2 does not build the governed data foundation. That is the role of Phase 3. It does not implement metric logic, create production-ready semantic assets, design the orchestration layer or validate the working MVP.

It also does not fix every data-quality, lineage, ownership or access issue it discovers. Full catalogue clean-up, enterprise data model redesign, broad historical data-quality remediation, final production engineering, final semantic-layer implementation, full security approval, penetration testing and expansion into new domains are outside the scope of this phase.

Its role is to classify the impact of readiness gaps on the scoped T2D questions and decide whether each question can proceed, proceed with caveats, require remediation, be deferred or be excluded.

### 2.4 Expected duration and level of effort

For a bounded single-domain use case with available stakeholders and accessible documentation, Phase 2 may take a few days to one or two weeks. Effort increases sharply when definitions are contested, lineage is unclear, data spans multiple domains, access rules are complex or expected-answer sources are not available.

The phase should not be measured by how many assets are reviewed. It should be measured by whether each priority question has a clear readiness decision and evidence trail.

### 2.5 Main participants and decision owners

| Role                                | Main responsibility in Phase 2                                                                    |
|-------------------------------------|---------------------------------------------------------------------------------------------------|
| Product owner                       | Owns MVP scope, question prioritisation and trade-offs.                                           |
| Business SME / domain owner         | Confirms business meaning, usage context and decision relevance.                                  |
| Data owner                          | Confirms source-of-truth status, data usage constraints and ownership.                            |
| Metric / semantic owner             | Approves KPI definitions, dimensions, filters, caveats and business terms.                        |
| Data architect / analytics engineer | Reviews data model, grain, joins, keys and semantic-layer implications.                           |
| Data engineer                       | Assesses source availability, quality issues, freshness and remediation needs.                    |
| Security / governance lead          | Reviews access, sensitivity, masking, audit and exposure constraints.                             |
| AI / solution architect             | Confirms implications for T2D query flow, tool use, retrieval and safe answer generation.         |
| Evaluation owner                    | Identifies how readiness findings will feed golden questions, expected answers and failure cases. |

The key point is accountability. Phase 2 should not end with a list of open issues owned by “the data team”. Every material gap should have an owner, a decision, and a route to either MVP inclusion, remediation, backlog or exclusion.

## 3 Readiness decision and delivery implications

Phase 2 must end with a delivery decision, not a generic statement that data readiness has been assessed. The decision should be based on the answerability matrix: what can be answered safely now, what requires caveats, what needs remediation, and what should remain outside the MVP. The test is not whether a prototype can be made to work; it is whether the data and semantic evidence is strong enough to justify the next delivery step.

### 3.1 Possible Phase 2 outcomes

| Outcome   | Meaning                                                                                    | Typical trigger                                                                            |
|-----------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Proceed   | Move to governed foundations, architecture and build with the proposed MVP question set.   | Priority questions have credible sources, definitions, joins, quality and access controls. |
| Narrow    | Continue, but reduce the question set, user group, data scope or answer types.             | Some value is viable, but parts of the scope are not ready or are too risky.               |
| Remediate | Address specific data, semantic, quality, metadata or access gaps before broader delivery. | The use case is valuable, but key foundations are not yet strong enough.                   |
| Defer     | Move some questions, domains or users to a future backlog.                                 | The questions may be viable later, but not within the current MVP path.                    |
| Stop      | Do not continue this use case as a T2D delivery candidate.                                 | The data, semantics, access model or ownership is too weak to support trusted answers.     |

A proceed decision should not mean that all risks are closed. It means the remaining risks are understood, owned and acceptable for the next delivery stage.

### 3.2 Minimum conditions to proceed

The use case should normally proceed only when the team can demonstrate that:

- **Priority questions are mapped** to known sources, metrics, dimensions and filters.

- **Source trust is understood**, including which assets are authoritative, reference-only, experimental or excluded.

- **Semantic definitions are explicit enough** for the system to interpret questions consistently.

- **Grain and joins are safe enough** to avoid structurally wrong answers.

- **Material data quality issues are known**, with caveats or remediation actions where needed.

- **Access constraints are understood**, including row, column, aggregation and inference risks.

- **Owners are named** for sources, definitions, quality issues, access decisions and remediation.

- **Backlog items are clear** for questions not ready for the first release.

The standard should be higher for pilot or production than for a constrained POC.

### 3.3 Common reasons to narrow, remediate, defer or stop

The team should avoid moving forward unchanged where any of the following apply:

- **The data exists but is not trusted.** Candidate sources are available, but ownership, lineage, certification or usage rights are unclear.

- **The metric is contested.** Different teams use different definitions for the same business term, with no approved MVP interpretation.

- **The join path is unsafe.** The model can generate valid SQL, but the grain, keys or relationships create risk of duplication, omission or misleading aggregation.

- **The filters are informal.** Standard exclusions, time windows, segments or caveats live in analyst judgement rather than reusable logic.

- **The access model is incomplete.** Users can be authenticated, but row-level, column-level, aggregation or inference controls are not ready.

- **The quality issues affect trust.** Completeness, freshness, duplicates, reconciliation gaps or late-arriving data could materially change the answer.

- **The question set is too broad.** Too many metrics, domains, users or answer types are being pushed into the first release.

- **Ownership is unresolved.** No one can approve definitions, accept caveats, prioritise remediation or own the answerability decision.

A T2D system should not be allowed to hide unresolved data and semantic issues behind a fluent answer. If the team cannot explain why a question is answerable, it is not ready for production-style use.

### 3.4 How Phase 2 shapes later phases

Phase 2 creates the evidence base for the next delivery stages. Its outputs should not remain as assessment documents; they should become design inputs.

| Later phase                                     | What Phase 2 should provide                                                                                        |
|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Phase 3 — Governed data foundations             | Confirmed sources, trusted assets, data gaps, quality issues and remediation priorities.                           |
| Phase 4 — Architecture and orchestration design | Data access patterns, semantic context needs, query boundaries, clarification needs and safe failure requirements. |
| Phase 5 — Prototype / MVP build                 | Approved question set, caveats, source mappings, metric definitions and known limitations.                         |
| Phase 6 — Validation, assurance and remediation | Golden-question candidates, expected-answer sources, ambiguity cases, caveat cases and failure categories.         |
| Phase 6 — Validation, assurance and remediation | Access constraints, sensitivity classifications, masking needs, aggregation limits and exposure risks.             |
| Phase 7–9 — Pilot, release and run              | Clear user-facing scope, known caveats, excluded questions and escalation routes.                                  |

This is the practical value of Phase 2: it turns data and semantic uncertainty into delivery decisions. The team should know not only what can be built, but what must be controlled, remediated, deferred or excluded before the system is exposed to users.

## 4 Data and semantic readiness activities overview

Phase 2 is organised around a small set of activities that turn the framed question set into an answerability matrix. The activities are not a rigid sequence. In practice, source validation, semantic discovery, data model review, quality assessment and access review often run in parallel and inform each other.

This phase is not a hard science. In many organisations, the required documentation will be incomplete, outdated or distributed across dashboards, SQL, spreadsheets, data catalogues and people’s memory. The role of the delivery team is not to pretend certainty exists where it does not. It is to find the balance between good enough for the next delivery step and not good enough to trust, scale or expose to users.

The work should remain anchored to the priority questions. A source, metric, join, quality issue or access rule only matters in this phase if it affects whether the T2D system can answer the scoped questions safely, consistently and explainably.

### 4.1 Activity sequence

| Activity                         | Main question                                                             | Main output                                                                                 |
|----------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| 1\. Validate source inventory    | Are the relevant sources trusted enough for MVP use?                      | Source relevance, ownership, trust status, usage constraints, future viability and caveats. |
| 2\. Map questions to data        | Are priority questions answerable from known sources?                     | Source, metric, dimension, filter and coverage mapping by question.                         |
| 3\. Review data model readiness  | Are grain, joins and aggregation rules safe enough for querying?          | Grain, keys, join paths, date logic, aggregation limits and known risks.                    |
| 4\. Confirm semantic definitions | Are the required definitions explicit enough for consistent answers?      | Approved, contested or missing KPIs, terms, filters, dimensions and caveats.                |
| 5\. Assess data gaps and quality | Are data gaps and quality issues acceptable for the scoped answers?       | Completeness, freshness, duplicates, reconciliation issues and affected questions.          |
| 6\. Assess metadata and lineage  | Is metadata usable enough to support T2D interpretation and traceability? | Catalogue coverage, lineage, glossary, documentation quality and ownership.                 |
| 7\. Review access and exposure   | Can the scoped answers be exposed safely to target users?                 | Permissions, sensitivity, masking, aggregation limits, inference risk and audit needs.      |
| 8\. Consolidate readiness gaps   | Is the MVP question set ready, narrowed or dependent on remediation?      | Final answerability matrix, caveats, remediation actions, backlog and exclusions.           |

**Note:** Activities 5.2, 5.3 and 5.4 may identify questions, data structures or semantic items with access, masking, aggregation or inference implications. These should be flagged during the relevant activity but assessed and controlled in Activity 5.7.

### 4.2 Activity logic

The activities should be treated as connected checks, not separate workstreams. A question may appear answerable after source mapping, but become unsafe once grain, joins, access or metric ambiguity are reviewed. Equally, a question may be deferred not because the data is missing, but because the semantic definition is contested or the access route is not acceptable.

The main control mechanism is the answerability matrix. It should be updated as each activity produces evidence, rather than completed once at the end of the phase.

Access, masking, aggregation and inference implications may appear during source mapping, data model review or semantic definition work. These should be flagged when discovered and assessed through the access and exposure review.

### 4.3 Practitioner note

Phase 2 should not become a data inventory exercise. The inventory is useful only if it changes a delivery decision: which questions can be answered, under which definitions, from which sources, for which users, and with which caveats or controls.

The main constraint is often not analysis effort, but access to the right owners. Source trust, metric definitions, lineage, caveats and access rules are frequently held by different people and may not be fully documented. The team should use existing artefacts first, prepare targeted questions, and reserve workshops for decisions that cannot be resolved asynchronously.

Not every limitation is a blocker. Some issues, such as refresh timing, late-arriving data, partial loads, metric caveats or restricted drill-down, may be acceptable if they are documented, monitored and surfaced clearly in the answer. The risk is not imperfection; it is hidden imperfection.

## 5 Core readiness activities

### 5.1 Validate source inventory

Validate which data assets are relevant, trusted and usable for the scoped T2D use case. The aim is not to document the full data estate, but to identify the sources that may support the priority questions and determine whether they are credible enough for MVP use.

A source should not be treated as “trusted” simply because it exists, is widely used or appears in a dashboard. For T2D, source trust means the asset has a clear role, owner, usage context, access route and known caveats.

**Key checks**

- **Relevance:** which systems, tables, marts, reports, APIs or semantic assets support the priority questions.

- **Trust status:** which assets are authoritative, certified, reference-only, experimental, deprecated or excluded.

- **Ownership:** who owns the source, maintains it and can approve its use.

- **Usage:** how the source is currently used in reporting, analysis or decision-making.

- **Access route:** whether the source can be accessed for discovery, POC, MVP and later production.

- **Freshness:** whether refresh cadence and latency are suitable for the user workflow.

- **Caveats:** which known limitations must be carried into later phases.

- **Future viability:** whether the source is stable, being migrated, deprecated, replaced, re-platformed or likely to change during the POC, MVP or pilot window.

- **Required governed assets**: whether existing sources are usable as-is, or whether curated views, marts, semantic-layer objects or controlled APIs need to be created.

**Main output**

A source readiness view showing which assets are relevant, trusted enough for MVP, reference-only, dependent on remediation or excluded.

**Red flags**

- The “trusted” source is trusted socially, but not documented technically.

- Several dashboards answer the same question differently.

- No owner can approve source use or explain caveats.

- The source is accessible for a POC but not for production.

- The team is relying on raw tables where curated assets should exist.

- The source is available today but scheduled for migration, decommissioning or major schema change.

**Practitioner note**: Challenging the trust status of a source can quickly become political, especially when it supports executive reporting or a widely used dashboard. The aim is not to discredit existing assets, but to be precise about whether they are suitable for T2D use, what caveats apply, and what must be validated before they generate conversational answers.

### 5.2 Map questions to data

Map each priority question to the sources, metrics, dimensions, filters and caveats required to answer it. This is the first version of the answerability matrix.

The objective is to move from “we think the data exists” to “we understand the data path required to answer this question”.

**Key checks**

- **Coverage:** which questions can be mapped to candidate sources.

- **Metric needs:** which KPIs or measures are required.

- **Dimension needs:** which slices, filters, time periods or comparisons are needed.

- **Source route:** which asset should be used as the source of truth.

- **Caveats:** which assumptions affect interpretation.

- **Initial status:** whether the question is ready, caveated, dependent on remediation, deferred or out of scope.

- **Evaluation eligibility:** whether the question has enough clarity to become a candidate golden question.

**Main output**

An initial answerability matrix linking each priority question to its required data, semantic definitions, validation needs and MVP decision.

**Red flags**

- Questions are too broad to map to specific data.

- The same question maps to multiple conflicting sources.

- Required dimensions or filters are missing.

- The expected answer depends on analyst judgement rather than reusable logic.

- A question is valuable but cannot yet support a reliable expected answer.

### 5.3 Review data model readiness

Assess whether the underlying data model is safe enough for T2D querying. This is where many plausible but wrong answers originate: incorrect grain, unsafe joins, duplicate keys, unclear date logic or misleading aggregation.

A model can be technically queryable and still be unsafe for T2D.

**Key checks**

- **Grain:** what each table or mart represents.

- **Keys:** which primary, foreign and business keys are reliable.

- **Join paths:** which joins are approved, risky or prohibited.

- **Aggregation:** what can be safely summed, counted, averaged or compared.

- **Date logic:** which dates should be used for each question type.

- **Relationship risk:** whether many-to-many joins, duplicate records or changing dimensions create answer risk.

- **Reusable patterns:** whether the model supports multiple questions or only narrow cases.

**Main output**

A model and join-risk view identifying safe query paths, unsafe joins, aggregation rules, date logic and caveats.

**Red flags**

- Grain is not understood by the delivery team.

- Joins are copied from analyst SQL without validation.

- Valid SQL can produce duplicated or misleading numbers.

- Different date fields produce materially different answers.

- The system would need to infer joins dynamically without approved rules.

### 5.4 Confirm semantic definitions

Confirm whether the required business terms, KPIs, measures, filters, dimensions, synonyms and caveats are explicit enough for consistent T2D answers.

This is not documentation for its own sake. In T2D, semantic definitions become part of the control surface: they guide question interpretation, query generation, caveat handling and safe failure.

**Key checks**

- **Approved definitions:** which metrics and terms have agreed meanings.

- **Calculation logic:** where formulas are implemented or documented.

- **Default filters:** which exclusions, time windows or population rules apply.

- **Dimensions:** which dimensions are approved for slicing and comparison.

- **Synonyms:** which user terms should map to approved business concepts.

- **Caveats:** which limitations must be shown to users.

- **Ownership:** who can approve or change the definition.

- **Change control:** which definitions, filters, dimensions, caveats or mappings require owner approval and versioning before reuse by T2D.

**Main output**

A semantic readiness view showing approved, contested and missing definitions, with required decisions and caveats.

**Red flags**

- Key terms such as revenue, churn, customer, margin or stock mean different things across teams.

- Metric logic exists only in dashboards, spreadsheets or analyst memory.

- Default filters are informal or inconsistently applied.

- The system would need to guess which definition the user intends.

- No owner can approve the MVP interpretation.

**Practitioner note:** Semantic readiness should not be interpreted as exhaustive semantic coverage. For T2D, the objective is to define enough approved meaning for the scoped users, questions and delivery stage. Some terms, synonyms, filters, dimensions and caveats will remain incomplete or evolve through use. The control is not to pretend that every possible interpretation has been captured, but to define which meanings are approved, which require clarification, which must be caveated, which should be refused and which belong in the semantic backlog.

### 5.5 Assess data gaps and quality

Identify whether missing data, poor quality, freshness issues, load failures, late-arriving data or reconciliation gaps could affect trusted answers. The focus should be on material issues that affect the scoped questions, not a full data quality audit.

**Key checks**

- **Completeness:** whether required fields are populated.

- **Freshness:** whether data is updated frequently enough for the use case.

- **Duplicates:** whether duplicate records affect counts, joins or aggregation.

- **Reconciliation:** whether results align with trusted reports or finance packs.

- **Nulls and exceptions:** whether missing values affect metrics or dimensions.

- **Late-arriving data:** whether backfills or timing delays need caveats.

- **Impact:** which priority questions are affected.

- **Refresh and load reliability:** whether update frequency, batch completion, late-arriving data, re-runs, failed loads and partial reloads are understood and visible.

**Main output**

A data quality impact view showing issue, affected questions, severity, business impact, caveat or remediation route.

**Red flags**

- Data quality is described anecdotally but not tested.

- Known issues are not linked to affected questions.

- Reconciliation differences are unexplained.

- Freshness does not match the user workflow.

- The system would present unstable or incomplete data without caveats.

- Missing, delayed or reloaded batches could materially change answers after the system has already responded.

<!-- -->

- The system has no way to caveat freshness, failed loads or incomplete periods.

**Practitioner note:** Data quality assessment is usually easier for governed SQL tables, marts or semantic-layer assets than for spreadsheets, extracts or less structured files. File-based sources may contain manual edits, hidden formulas, inconsistent layouts, local definitions or undocumented refresh processes. These limitations should be made explicit before they are used to support T2D answers.

### 5.6 Assess metadata and lineage

Assess whether metadata, lineage, glossary and documentation are usable enough to support T2D interpretation, traceability and explanation.

Metadata does not need to be perfect, but it must be good enough for the system and delivery team to understand what a source or metric means, where it comes from, who owns it and how it should be used.

**Key checks**

- **Catalogue coverage:** whether relevant assets are registered.

- **Lineage:** whether key metrics and data assets can be traced to source tables and whether the upstream logic that produced those assets is understood[^1].

- **Glossary:** whether business terms and synonyms are documented.

- **Documentation quality:** whether table, column and metric descriptions are usable.

- **Certification:** whether users and systems can distinguish trusted from untrusted assets.

- **Ownership:** whether business and technical owners are visible.

- **System usability:** whether metadata can support retrieval, grounding or explainability.

**Main output**

A metadata and lineage readiness view identifying documentation gaps, traceability lineage, production lineage, ownership issues and metadata risks that affect T2D delivery.

**Red flags**

- Documentation exists but is outdated or not trusted.

- Business terms are not linked to technical assets.

- Lineage cannot explain how reported numbers are produced.

- Ownership is unclear for critical metrics or tables.

- Metadata is too unstructured to support retrieval or governance.

**Practitioner note:** For T2D, metadata is not only documentation. It is part of the system’s operating context. Metadata may be used to route questions to the right domain, retrieve approved definitions, constrain query generation, explain answers and decide when the system should clarify or refuse. Metadata that is incomplete, stale or too unstructured can therefore become an answer-quality risk, not just a governance gap.

### 5.7 Review access and exposure

Confirm whether scoped answers can be exposed safely to target users. Access review for T2D must go beyond basic authentication. It should consider row-level access, column restrictions, aggregation thresholds, masking, follow-up questions and inference risk.

Aggregation risk is especially difficult in T2D. Even where row-level and column-level permissions are enforced, users may infer restricted information through small-group aggregations, repeated follow-up questions, drill-down patterns or comparisons over time. There is no perfect control, especially with probabilistic language interfaces and multi-turn interaction. The practical objective is to reduce exposure through clear limits, monitoring, refusal rules, aggregation thresholds and user-facing caveats — not to pretend the risk can be eliminated completely.

**Key checks**

- **User groups:** who will use the system and what they are allowed to see.

- **Sensitivity:** which data is personal, confidential, regulated or commercially restricted.

- **Permission model:** row-level, column-level, role-based and domain-based controls.

- **Aggregation risk:** whether small groups or drill-downs expose sensitive information.

- **Inference risk:** whether users can infer restricted data through repeated questions.

- **Masking:** where redaction, suppression or aggregation is required.

- **Auditability:** what needs to be logged for review and investigation.

**Main output**

An access and exposure view showing what can be exposed, restricted, masked, aggregated, refused or escalated.

**Red flags**

- Users can authenticate, but data-level permissions are unclear.

- Sensitive fields are available to the model or query layer without control.

- Aggregated answers could reveal small-group or restricted information.

- Follow-up questions allow users to work around access boundaries.

- Security review is deferred until after prototype build.

**Practitioner note:**

**Note 1:** Access rights should come from existing enterprise systems wherever possible, such as identity groups, warehouse roles, BI permissions or approved policy layers. T2D should avoid creating a parallel access model unless there is a clear reason and ownership route.

**Note 2:** Exposure risk increases as conversations iterate. Users may combine filters, ask follow-up questions, narrow cohorts or compare results over time in ways that reveal information not visible in a single answer. It is not realistic to anticipate every possible inference path. Access review should therefore define common risk patterns, aggregation limits, refusal rules, monitoring needs and escalation routes, while recognising that residual multi-turn exposure risk may remain.

### 5.8 Consolidate readiness gaps

Consolidate the findings into a final answerability matrix and remediation backlog. This activity turns assessment into a delivery decision.

The team should take a clear stance for each priority question: **ready for MVP — yes or no**. The explanation can include caveats, remediation needs, backlog route or exclusion rationale, but the decision itself should not be ambiguous. “Probably”, “depends” or “needs more analysis” are not useful delivery outcomes unless they are converted into a specific decision and owner.

**Key checks**

- **MVP readiness:** is this question ready for MVP — yes or no?

- **Decision rationale:** what evidence supports the decision?

- **Caveats:** what limitations must be shown to users or enforced by the system?

- **Remediation:** what must change before inclusion, who owns it and when it is needed?

- **Backlog route:** should the question be revisited later, and under what conditions?

- **Exclusion rationale:** why should the question remain out of scope?

- **Handover:** which findings must feed governed foundations, architecture, evaluation and security validation?

- **Versioning needs:** which semantic definitions, source mappings, caveats or candidate golden questions must be versioned in later phases.

**Main output**

A final answerability matrix with a binary MVP-readiness decision for each priority question, supported by rationale, caveats, remediation actions, backlog route or exclusion rationale.

**Red flags**

- Findings are listed without decisions.

- Issues are owned vaguely by “data” or “business”.

- Deferred questions have no route back into the backlog.

- Caveats are not translated into user-facing or system-facing controls.

- The team proceeds because the prototype is possible, not because the evidence supports it.

## 6 Answerability decision pack

Phase 2 should end with one consolidated artefact: the **answerability matrix**. Supporting notes on sources, semantics, data quality, metadata and access may sit behind it, but the main output should be a decision-ready view of each priority question.

The matrix should force a clear position: **ready for MVP — yes or no**. Caveats, remediation needs, backlog routes and exclusions should explain the decision, not replace it.

### 6.1 Answerability matrix

| Field                              | Purpose                                                                                                        |
|------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Priority question                  | Business question being assessed.                                                                              |
| Ready for current delivery intent? | Binary decision: Yes / No.                                                                                     |
| Status                             | Ready, ready with caveats, dependent on remediation, deferred or out of scope.                                 |
| Source                             | Confirmed source, mart, report, API or semantic asset.                                                         |
| Semantic definition                | Metric, term, calculation, filters, dimensions and caveats.                                                    |
| Data model basis                   | Grain, join path, date logic and aggregation rule.                                                             |
| Quality / freshness caveat         | Known issue affecting confidence or interpretation.                                                            |
| Access constraint                  | User group, masking, row/column restriction or aggregation limit.                                              |
| Evaluation eligibility             | Whether the question is suitable to become a candidate golden question.                                        |
| Decision rationale                 | Why the question is or is not ready.                                                                           |
| Owner                              | Person or function accountable for the decision or gap.                                                        |
| Next action                        | Include, caveat, remediate, backlog or exclude.                                                                |
| Follow-up safety                   | Whether likely follow-up questions remain within approved scope, access rules and safe aggregation boundaries. |

### 6.2 Answerability pack quality test

Before exiting Phase 2, the answerability matrix should allow stakeholders to answer:

- Which questions are ready for MVP, yes or no?

- Which questions need caveats, restrictions or remediation?

- Which questions should move to the backlog or be excluded?

- Which sources, definitions, joins, filters and access rules will be used?

- Which material gaps remain, and who owns them?

- Which questions are eligible to become golden questions?

- What must be handed over to governed foundations, architecture, evaluation and security validation?

If the matrix cannot support these decisions, Phase 2 is not complete enough to justify build.

## 7 Exit criteria and handover

Phase 2 should end with a clear readiness decision and a controlled handover to the next delivery phases. The handover should not be a general data assessment pack. It should provide the specific evidence needed to build, test, secure and govern the scoped T2D capability.

### 7.1 Required exit outputs

The minimum exit output is the final **answerability matrix**. It should include:

- MVP-readiness decision for each priority question.

- Source and semantic definition used.

- Grain, join, filter and aggregation assumptions.

- Quality, freshness or load caveats.

- Access and exposure constraints.

- Evaluation eligibility.

- Remediation actions, backlog items and exclusions.

- Named owners for material gaps and decisions.

Supporting artefacts may include source notes, metric cards, ambiguity logs, data quality findings, access notes or lineage evidence, but these should remain supporting material rather than replacing the matrix.

### 7.2 Handover to later phases

The handover should convert the answerability matrix into phase-specific inputs. It should not repeat the full assessment narrative. Each later phase should receive the decisions, caveats, constraints and unresolved gaps it needs to continue delivery safely.

| Later phase                           | What Phase 2 should hand over                                                                                                                                                       |
|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Governed data foundations             | Confirmed sources, required curated assets, data quality issues, freshness expectations, load-completion checks, known latency, caveats, remediation priorities and data ownership. |
| Architecture and orchestration design | Query boundaries, semantic context needs, clarification needs, refusal cases, tool-use constraints, logging needs and safe-failure requirements.                                    |
| Prototype / MVP build                 | MVP-ready question set, source mappings, semantic definitions, caveats, access constraints and known limitations.                                                                   |
| Evaluation design                     | Candidate golden questions, expected-answer sources, ambiguity cases, caveat cases, unsafe requests and failure categories.                                                         |
| Security and governance validation    | Access constraints, sensitivity classifications, masking needs, aggregation limits, inference risks, audit requirements and exposure controls.                                      |
| Versioning and change control         | Semantic definitions, source mappings, filters, joins, caveats and candidate golden questions that require versioning, approval or controlled change.                               |
| Backlog / roadmap                     | Deferred questions, blocked use cases, required changes, owners, dependencies and triggers for reconsideration.                                                                     |

## 8 Key risks and failure modes

Phase 2 should actively look for the risks that cause T2D systems to appear credible in prototype but fail in real use. The most dangerous risks are not always missing data. They are often unclear definitions, unsafe joins, weak access controls, hidden caveats and unresolved ownership.

| Risk / failure mode          | Why it matters                                                                                                                 | Likely response                                                         |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| False source trust           | A dataset or dashboard is treated as trusted because people use it, not because lineage, quality and ownership are understood. | Validate source role, owner, caveats and suitability before MVP use.    |
| Semantic ambiguity           | Terms such as revenue, churn, customer, margin or stock mean different things across teams.                                    | Agree MVP definitions or defer affected questions.                      |
| Unsafe grain or join path    | Valid SQL can still produce duplicated, omitted or misleading results.                                                         | Define approved joins, grain rules and aggregation limits.              |
| Informal filters and caveats | Analyst judgement is embedded in spreadsheets, dashboards or habit rather than reusable logic.                                 | Convert material filters and caveats into explicit rules.               |
| Hidden data quality issues   | Completeness, freshness, reconciliation or load issues may affect answers without being visible to users.                      | Document, monitor, caveat, remediate or exclude affected questions.     |
| Weak metadata and lineage    | The team cannot explain where an answer came from or how the supporting asset was produced.                                    | Improve minimum lineage, ownership and documentation for scoped assets. |
| Access and exposure risk     | Users may see or infer restricted information through drill-downs, aggregations or repeated questions.                         | Apply restrictions, thresholds, masking, refusal rules and monitoring.  |
| Unstable data assets         | A source may be migrated, deprecated, re-platformed or structurally changed during delivery.                                   | Confirm future viability and plan for migration or exclusion.           |
| Prototype overconfidence     | A narrow demo works, but only because questions, data and access have been manually controlled.                                | Separate POC learning from scalable MVP readiness.                      |
| Unowned gaps                 | Issues are captured but no one can approve, remediate or accept them.                                                          | Assign owners or block/narrow affected questions.                       |

### 8.1 Practitioner note

The biggest Phase 2 failure is false confidence. A question should not be treated as ready because a model can generate a plausible answer. It is ready only when the source, definition, grain, join, filter, quality caveat and access route are understood well enough to support a defensible answer.

[^1]: Lineage has two levels. The first is traceability: can the answer be linked to the table, model or semantic asset used by T2D? The second is production lineage: how was that asset created, transformed, reconciled and approved? Both matter, but the second is often harder and determines whether the source is genuinely trustable.

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
