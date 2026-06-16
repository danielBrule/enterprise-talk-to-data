# Talk-to-Data Delivery Blueprint — Phase 1 Annexes: Framing

*Daniel Brule · Talk-to-Data Delivery Blueprint · v1.0 · June 2026*

---

**Table of contents**

- [1 How to use this annex pack](#1-how-to-use-this-annex-pack)
- [2 Activity question banks](#2-activity-question-banks)
  - [2.1 Business framing](#21-business-framing)
  - [2.2 User and workflow discovery](#22-user-and-workflow-discovery)
  - [2.3 Initial data landscape scan](#23-initial-data-landscape-scan)
  - [2.4 Initial semantic framing](#24-initial-semantic-framing)
  - [2.5 Security and governance framing](#25-security-and-governance-framing)
  - [2.6 Solution architecture framing](#26-solution-architecture-framing)
  - [2.7 Delivery planning and MVP boundary](#27-delivery-planning-and-mvp-boundary)
  - [2.8 Evaluation design framing](#28-evaluation-design-framing)
  - [2.9 Operating model framing](#29-operating-model-framing)
- [3 Activity output templates](#3-activity-output-templates)
  - [3.1 Business framing](#31-business-framing)
  - [3.2 User and workflow discovery](#32-user-and-workflow-discovery)
  - [3.3 Initial data landscape scan](#33-initial-data-landscape-scan)
  - [3.4 Initial semantic framing](#34-initial-semantic-framing)
  - [3.5 Security and governance framing](#35-security-and-governance-framing)
  - [3.6 Solution architecture framing](#36-solution-architecture-framing)
  - [3.7 Delivery planning and MVP boundary](#37-delivery-planning-and-mvp-boundary)
  - [3.8 Evaluation design framing](#38-evaluation-design-framing)
  - [3.9 Operating model framing](#39-operating-model-framing)
- [4 Activity scorecards](#4-activity-scorecards)
  - [4.1 Business framing scorecard](#41-business-framing-scorecard)
  - [4.2 User and workflow discovery scorecard](#42-user-and-workflow-discovery-scorecard)
  - [4.3 Initial data landscape scan scorecard](#43-initial-data-landscape-scan-scorecard)
  - [4.4 Initial semantic framing scorecard](#44-initial-semantic-framing-scorecard)
  - [4.5 Security and governance framing scorecard](#45-security-and-governance-framing-scorecard)
  - [4.6 Solution architecture framing scorecard](#46-solution-architecture-framing-scorecard)
  - [4.7 Delivery planning and MVP boundary](#47-delivery-planning-and-mvp-boundary)
  - [4.8 Evaluation design framing scorecard](#48-evaluation-design-framing-scorecard)
  - [4.9 Operating model framing scorecard](#49-operating-model-framing-scorecard)
- [5 Overall phase readiness scorecard](#5-overall-phase-readiness-scorecard)
- [6 Risk, decision, assumption and dependency logs](#6-risk-decision-assumption-and-dependency-logs)
  - [6.1 Risk log](#61-risk-log)
  - [6.2 Decision log](#62-decision-log)
  - [6.3 Assumption log](#63-assumption-log)
  - [6.4 Dependency log](#64-dependency-log)

---

## 1 How to use this annex pack

This annex pack contains detailed tools and templates supporting the Phase 1 Framing Guide. It is intended for facilitation, documentation and project delivery. The main guide explains the framing logic; this annex provides the reusable working material.

## 2 Activity question banks

### 2.1 Business framing

| Area                | Questions                                                                                                                                           |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Strategic objective | Why Talk-to-Data now? Is the driver productivity, self-service, faster reporting, executive insight, analyst augmentation or another business need? |
| Priority domain     | Which domain should be addressed first: finance, sales, operations, customer, risk, product or another area?                                        |
| Scope               | What should the assistant answer in v1? What is explicitly out of scope? What is the longer-term ambition?                                          |
| Users               | Who is the first user group: executives, managers, analysts, frontline teams or another group?                                                      |
| Timeline            | What is the expected timeline for discovery, POC, MVP, pilot and production?                                                                        |
| Risk appetite       | What level of risk is acceptable for answer accuracy, data exposure, user autonomy and business impact?                                             |
| Sponsorship         | Who funds delivery? Who owns the business outcome?                                                                                                  |
| Governance          | Who approves scope, metric definitions, access rules, risk posture, pilot and go-live? What is reported, to whom and when?                          |
| Budget              | What budget envelope is available for discovery, POC/MVP, production readiness and ongoing run costs?                                               |
| Success             | What decisions will be improved? What time, cost, quality or risk benefit is expected?                                                              |
| Failure impact      | What would a harmful or unacceptable answer look like?                                                                                              |

### 2.2 User and workflow discovery

| Area                     | Questions                                                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| User groups              | Who are the target users: executives, managers, analysts, frontline teams or external users?                                   |
| User volume and location | How many users are expected? Where are they located? Are they office-based, remote, mobile or global?                          |
| Skill level              | Are users data-literate? Can they interpret metrics, SQL, charts, confidence levels and caveats?                               |
| Access context           | Which devices and channels do they use: desktop, mobile, Teams, Slack, BI tool, intranet or another interface?                 |
| Current workflow         | How do users answer these questions today: dashboard, analyst request, SQL, Excel, BI tool or manual process?                  |
| Workflow frequency       | How often are questions asked: daily, weekly, monthly, ad hoc or board-cycle driven?                                           |
| Pain points              | Is the issue speed, trust, lack of data skills, fragmented tools, inconsistent metrics, analyst dependency or slow turnaround? |
| Decision context         | What decisions are made from the answers? Are they operational, tactical, strategic, regulatory or investment-related?         |
| Question types           | Are users asking KPI, trend, comparison, variance, root-cause, forecasting, explanation or data-quality questions?             |
| Question complexity      | Are questions simple lookups, aggregations, multi-step analysis, cross-domain joins or ambiguous business questions?           |
| Follow-ups               | Do users need conversational drill-downs, filters, comparisons, rephrasing or “why has this changed?” analysis?                |
| Output format            | Do users expect a number, chart, table, SQL, narrative, export, dashboard link or recommended action?                          |
| Trust requirements       | Do users need source tables, metric definitions, SQL, confidence level, caveats or lineage to trust the answer?                |
| Human review             | When should the assistant answer directly, ask clarification, escalate to an analyst or refuse?                                |
| Error tolerance          | What level of error is acceptable by question type? Which answers require validation before being shown?                       |

### 2.3 Initial data landscape scan

| Area                     | Questions                                                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Sources                  | Which systems contain the required data: warehouse, lakehouse, BI semantic model, operational systems, APIs or files?          |
| Data ownership           | Who owns each source, table, metric and business definition?                                                                   |
| Trusted assets           | Which tables, views, dashboards or marts are certified, trusted, deprecated or experimental?                                   |
| Current usage            | Which tables and dashboards are currently used to answer the priority questions?                                               |
| Data grain               | At what level are facts stored: customer, transaction, account, day, product, contract or event?                               |
| Freshness                | How frequently is the data updated: real-time, daily, weekly, monthly or manually refreshed?                                   |
| Coverage                 | Does the available data cover the required users, geographies, products, time periods and entities?                            |
| Lineage                  | Can key metrics be traced from report back to model, table and source system?                                                  |
| Data quality             | Are there known issues with completeness, duplicates, nulls, timeliness, reconciliation or reliability?                        |
| Existing semantic assets | Are there existing BI models, certified datasets, dbt models, cubes or semantic layers that can be reused rather than rebuilt? |
| Data change risk         | Are source systems, tables, metrics or ownership expected to change during the delivery timeline?                              |

### 2.4 Initial semantic framing

| Area                     | Questions                                                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Metrics                  | Are key metrics clearly defined: revenue, margin, churn, active customer, pipeline, conversion?                                |
| Consistency              | Are definitions consistent across teams, geographies and reporting packs?                                                      |
| Dimensions               | Which dimensions are approved for slicing: time, region, customer, product, channel, segment, business unit?                   |
| Joins                    | Which joins are likely to be approved and safe? Are there ambiguous or many-to-many joins to avoid?                            |
| Filters                  | What standard exclusions apply: test accounts, cancelled orders, internal users, inactive products, intercompany transactions? |
| Business glossary        | Are business terms, synonyms and abbreviations documented?                                                                     |
| Calculation logic        | Are formulas documented in SQL, BI, dbt, semantic layer or only in analysts’ heads?                                            |
| Query examples           | Are trusted SQL examples or BI calculations available for grounding and evaluation?                                            |
| Ambiguity                | Which terms require clarification before answering?                                                                            |
| Certified answer sources | Which dashboards, reports, SQL queries or finance packs are considered official?                                               |

### 2.5 Security and governance framing

| Area                  | Questions                                                                                                                       |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------|
| Identity              | How is the user authenticated: SSO, BI permissions, warehouse roles or app-level identity?                                      |
| Authorisation         | Should T2D inherit existing user permissions, use service-account permissions or apply a separate policy layer?                 |
| Row-level security    | Can users only see their region, business unit, portfolio, customer segment or assigned accounts?                               |
| Column-level security | Are salary, PII, margin, customer identifiers, contract terms or sensitive fields masked or blocked?                            |
| Aggregation risk      | Could users infer restricted data from aggregates, small cohorts, drill-downs or repeated queries?                              |
| Data classification   | Which datasets contain public, internal, confidential, restricted, PII, financial or regulated data?                            |
| Compliance            | What constraints apply: GDPR, financial controls, client confidentiality, regulatory requirements, data residency or retention? |
| Model / vendor policy | Can data or metadata be sent to an external LLM provider? Are private endpoints, zero-retention or on-prem models required?     |
| Logging               | What must be logged: user, question, context, SQL, result summary, answer, errors and feedback?                                 |
| Audit                 | Who can review past questions, SQL, answers and access events? At what cadence and for what purpose?                            |
| Retention             | How long should prompts, SQL, results and feedback be retained? What must be redacted or excluded?                              |

### 2.6 Solution architecture framing

| Area                         | Questions                                                                                                                                                                            |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Cloud and platform landscape | Which cloud providers, data platforms, BI tools, identity providers and integration platforms are currently in use?                                                                  |
| Technology standards         | Are there mandated tools, preferred vendors, approved LLM providers, architecture principles or prohibited technologies?                                                             |
| Architecture governance      | What is the architecture review process? Who approves solution design, security design and production deployment?                                                                    |
| Architecture approval        | What evidence is required for architecture approval: high-level design, data flow, security model, integration diagram, non-functional requirements, cost estimate or support model? |
| IT roadmap                   | Are there planned changes: cloud migration, data platform migration, BI migration, identity changes or governance tooling?                                                           |
| Interface                    | Should T2D live in a dedicated UI, BI tool, Teams/Slack, internal portal, notebook, CRM or workflow application?                                                                     |
| User experience              | Should the interface support chat history, follow-up questions, charts, SQL visibility, citations, exports, feedback or escalation?                                                  |
| Model choice                 | Which LLM provider or model is allowed? If none, is there a process to select one?                                                                                                   |
| Model routing                | Should different models be used for intent classification, metadata retrieval, SQL generation, validation and explanation?                                                           |
| Context strategy             | What instructions, examples, metadata, business rules and user context should be retrieved?                                                                                          |
| Data connectivity            | Which query engine, warehouse, semantic layer or API will be used?                                                                                                                   |
| SQL validation               | Should validation use SQL parser, dry-run, explain plan, policy engine, allow-listed tables, row limits or second model review?                                                      |
| Safety controls              | What should be blocked: SELECT \*, PII columns, raw exports, high-cost queries, small cohorts or destructive commands?                                                               |
| Deployment model             | Should deployment use cloud, VPC, private endpoint, containers, Kubernetes, serverless, managed AI platform or internal platform?                                                    |
| Observability                | Where are latency, cost, token usage, errors, SQL, feedback, quality and security events logged?                                                                                     |
| Non-functional requirements  | What latency, scalability, reliability, cost, auditability and maintainability requirements apply?                                                                                   |

### 2.7 Delivery planning and MVP boundary

| Area            | Questions                                                                                                                           |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------|
| MVP boundary    | Which users, domains, questions, datasets and answer types are included in MVP?                                                     |
| Exclusions      | What is explicitly excluded from MVP?                                                                                               |
| Backlog         | What are the initial epics and work packages?                                                                                       |
| Timeline        | What is the timeline for discovery, readiness, governed layer, architecture, prototype, security, evaluation, pilot and production? |
| Team capacity   | Which business, data, engineering, security, SME and product roles are available?                                                   |
| Budget          | What budget is available for delivery effort, data engineering, LLM usage, warehouse compute, tooling, security review and support? |
| Approval gates  | What decisions are required before discovery, prototype, pilot and production?                                                      |
| Delivery risks  | What could delay or block MVP delivery?                                                                                             |
| Dependencies    | Which data, access, architecture, evaluation or governance dependencies are critical?                                               |
| Delivery method | Will delivery follow agile, phased gates, discovery sprint, POC, pilot or another approach?                                         |

### 2.8 Evaluation design framing

| Area                   | Questions                                                                                                                              |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Evaluation scope       | Are we evaluating SQL correctness, business correctness, safety, answer quality, latency, cost, adoption or all of these?              |
| Success bar            | What level of accuracy, safety, latency and user satisfaction is acceptable before MVP, pilot and production?                          |
| Golden questions       | What are the 30–100 questions users actually expect the assistant to answer?                                                           |
| Ground truth ownership | Who can confirm expected SQL, metric logic, final answer and caveats?                                                                  |
| Evaluation dimensions  | What counts as correct: valid SQL, right metric, right grain, right filters, correct number, useful explanation?                       |
| Safety evaluation      | What data must never be exposed? What access-control, PII, aggregation and inference risks must be tested?                             |
| Operational metrics    | What latency, cost per question, error rate and timeout rate are acceptable?                                                           |
| User feedback          | Can users mark answers as correct, wrong, unclear, unsafe or not useful?                                                               |
| Regression approach    | Will the golden set be rerun after prompt, model, semantic layer, schema or code changes?                                              |
| Evaluation ownership   | Who owns evaluation after launch: product, analytics, QA, SMEs, data governance or platform team?                                      |
| Failure taxonomy       | Are failures due to intent, metadata retrieval, SQL generation, semantic mismatch, data quality, permissions, UX or model explanation? |

### 2.9 Operating model framing

| Area                   | Questions                                                                                  |
|------------------------|--------------------------------------------------------------------------------------------|
| Product ownership      | Who owns the T2D product roadmap after launch?                                             |
| Business ownership     | Who owns the business outcome and prioritises new use cases?                               |
| Semantic ownership     | Who approves changes to metrics, dimensions, joins, filters and business definitions?      |
| Data ownership         | Who owns source data quality, freshness and lineage?                                       |
| Technical ownership    | Who maintains the application, orchestration, prompts, connectors and deployment?          |
| Security ownership     | Who maintains access rules, masking, row-level security and audit controls?                |
| Evaluation ownership   | Who maintains golden questions, regression tests and quality thresholds?                   |
| Support ownership      | Who triages user issues: data team, BI team, platform team, product owner or support desk? |
| Funding                | Who funds discovery, build, production deployment and ongoing run costs?                   |
| Change management      | What communication, training and adoption support is needed?                               |
| Workforce impact       | How will T2D affect analysts, reporting teams and business users?                          |
| Continuous improvement | How will new questions, failed answers, semantic gaps and user feedback be prioritised?    |

## 3 Activity output templates

These columns are illustrative examples only. They are intended to show the expected structure and level of detail.

### 3.1 Business framing

| Item                 | Description                                         | Owner<sup>1</sup>       | Status<sup>1</sup> | Notes<sup>1</sup>                              |
|----------------------|-----------------------------------------------------|-------------------------|--------------------|------------------------------------------------|
| Problem statement    | Why Talk-to-Data is being considered                | Product owner / sponsor | Draft / agreed     | Should link to a specific business pain point  |
| Priority domain      | First business area in scope                        | Business lead           | Draft / agreed     | Should avoid multi-domain MVP unless justified |
| MVP scope            | First users, questions, datasets and excluded areas | Product owner           | Draft / agreed     | Include explicit exclusions                    |
| Strategic value case | Expected benefit and decision improvement           | Sponsor                 | Draft / agreed     | Should be measurable where possible            |
| Risk appetite        | Acceptable risk posture for MVP                     | Sponsor / risk owner    | Draft / agreed     | Must inform security and evaluation            |
| Governance route     | Decision forums and approval gates                  | Delivery lead           | Draft / agreed     | Include pilot and go-live approval             |
| Budget envelope      | Funding for discovery, MVP and run costs            | Sponsor / finance       | Draft / agreed     | Include data, AI, platform and support costs   |

### 3.2 User and workflow discovery

| User group          | Workflow / decision         | Current process                           | Priority questions                                            | Frequency        | Pain point               | Expected answer format    | Trust requirement                 | MVP relevance |
|---------------------|-----------------------------|-------------------------------------------|---------------------------------------------------------------|------------------|--------------------------|---------------------------|-----------------------------------|---------------|
| Executive team      | Performance review          | Board pack and follow-up analyst requests | Revenue, margin, target variance, regional performance        | Monthly / ad hoc | Slow follow-up questions | KPI, chart, narrative     | Source, metric definition, caveat | High          |
| Sales managers      | Pipeline and account review | CRM dashboard and analyst extracts        | At-risk opportunities, declining customers, conversion trends | Weekly           | Fragmented reporting     | Table, chart, explanation | Source, filters, freshness        | High          |
| Analysts            | Exploratory analysis        | SQL, BI, Excel                            | Root-cause, variance, drill-downs                             | Daily / weekly   | Manual query effort      | SQL, table, export        | SQL visibility, lineage           | Medium        |
| Operations managers | Service or backlog review   | Dashboard and spreadsheets                | Backlog, delays, location variance                            | Daily / weekly   | Limited self-service     | KPI, table, chart         | Freshness, definitions            | Medium        |

### 3.3 Initial data landscape scan

| Priority question area | Candidate source / report           | System         | Owner               | Trusted status    | Coverage                  | Freshness             | Known issue                   | Step 2 validation needed                 |
|------------------------|-------------------------------------|----------------|---------------------|-------------------|---------------------------|-----------------------|-------------------------------|------------------------------------------|
| Revenue performance    | Finance revenue mart / finance pack | Warehouse / BI | Finance Analytics   | Likely certified  | Region, product, month    | Daily / monthly close | Definition may vary by report | Confirm source of truth and metric logic |
| Sales pipeline         | Sales pipeline dashboard            | CRM / BI       | Sales Ops           | Trusted reference | Opportunity, owner, stage | Daily                 | Stage definitions may vary    | Confirm grain, filters and owner         |
| Customer spend         | Revenue mart + customer master      | Warehouse      | Data / Sales Ops    | Partially trusted | Customer, month           | Daily                 | Customer duplicates           | Validate joins and customer hierarchy    |
| Churn                  | CRM + billing                       | CRM / Billing  | Sales Ops / Finance | Unknown           | Customer, segment, month  | Unknown               | No agreed definition          | Confirm definition and source ownership  |

### 3.4 Initial semantic framing

| Metric / term | Possible meaning                                | Default framing assumption                           | Source of truth candidate   | Owner            | Ambiguity risk | Step 2 validation needed              |
|---------------|-------------------------------------------------|------------------------------------------------------|-----------------------------|------------------|----------------|---------------------------------------|
| Revenue       | Gross, net, recognised, booked                  | Net revenue for MVP unless sponsor decides otherwise | Finance mart / finance pack | Finance          | High           | Agree approved definition and filters |
| Customer      | CRM account, billing customer, legal entity     | Billing customer for financial questions             | Customer master             | Sales Ops / Data | High           | Confirm hierarchy and joins           |
| Churn         | No spend, cancelled contract, lost account      | Not agreed                                           | CRM + billing               | Sales Ops        | High           | Define churn and ownership            |
| Pipeline      | Open opportunities, weighted pipeline, forecast | Sales pipeline by approved CRM stage                 | Sales BI dashboard          | Sales Ops        | Medium         | Confirm stage logic and exclusions    |

### 3.5 Security and governance framing

| Area             | Initial assumption                                                               | Risk level | Owner                    | Validation needed               | Decision required |
|------------------|----------------------------------------------------------------------------------|------------|--------------------------|---------------------------------|-------------------|
| Authentication   | Use enterprise SSO                                                               | Medium     | Security architect       | Confirm integration route       | Yes               |
| Authorisation    | Inherit existing BI / warehouse permissions where possible                       | High       | Security / data platform | Confirm feasibility and gaps    | Yes               |
| Sensitive data   | PII excluded from MVP unless specifically approved                               | High       | DPO / governance         | Confirm data classification     | Yes               |
| Row-level access | Apply region / business-unit restrictions for business users                     | High       | Data owner / security    | Confirm available access model  | Yes               |
| SQL visibility   | Analysts only for MVP                                                            | Medium     | Product owner / security | Confirm user groups             | Yes               |
| Logging          | Log user, question, retrieved context, generated SQL, result status and feedback | Medium     | Platform owner           | Confirm retention and redaction | Yes               |

### 3.6 Solution architecture framing

| Area           | Initial architecture assumption                              | Constraint / dependency             | Owner                   | Validation needed                    | MVP implication             |
|----------------|--------------------------------------------------------------|-------------------------------------|-------------------------|--------------------------------------|-----------------------------|
| User interface | Start with controlled internal UI or Teams/Slack integration | Enterprise UX and security approval | Product / platform      | Confirm preferred channel            | Defines user access path    |
| Model provider | Use approved enterprise LLM provider                         | Vendor and data policy              | AI architect / security | Confirm permitted model and endpoint | May affect cost and latency |
| Data access    | Query governed marts or semantic layer only                  | Step 2 data readiness               | Data architect          | Confirm available query layer        | Limits MVP scope            |
| SQL validation | Use parser, allow-listed schemas, dry-run and row limits     | Platform tooling                    | AI architect            | Confirm validation approach          | Required before pilot       |
| Observability  | Log prompts, SQL, result status, errors, feedback and cost   | Logging tools and policy            | Platform owner          | Confirm retention and redaction      | Required for safe MVP       |
| Deployment     | Use approved enterprise deployment pattern                   | Architecture approval               | Platform architect      | Confirm environment path             | Defines timeline            |

### 3.7 Delivery planning and MVP boundary

| Workstream   | Key activity                            | Owner              | Dependency          | Indicative timing | MVP criticality | Notes                     |
|--------------|-----------------------------------------|--------------------|---------------------|-------------------|-----------------|---------------------------|
| Product      | Confirm MVP questions and users         | Product owner      | Sponsor decision    | Week 0–1          | High            | Required before Step 2    |
| Data         | Validate candidate data assets          | Data architect     | Access to sources   | Week 1            | High            | Feeds Step 2              |
| Semantic     | Draft metric and business definitions   | Analytics engineer | SME availability    | Week 1            | High            | Feeds governed layer      |
| Security     | Confirm access and exposure constraints | Security architect | Data classification | Week 1–2          | High            | Required before prototype |
| Architecture | Confirm target pattern                  | AI architect       | Platform standards  | Week 1–2          | High            | Required before build     |
| Evaluation   | Create golden question plan             | AI architect / QA  | Question backlog    | Week 1–2          | Medium          | Required before pilot     |
| Delivery     | Build MVP roadmap and backlog           | Delivery lead      | All workstreams     | Week 1            | High            | Phase-gate input          |

### 3.8 Evaluation design framing

| Evaluation item      | Definition                                           | Owner                            | MVP expectation                  | Evidence needed                                 |
|----------------------|------------------------------------------------------|----------------------------------|----------------------------------|-------------------------------------------------|
| Golden question set  | Representative business questions for MVP            | Product owner / business analyst | 30–50 initial questions          | User interviews and existing reporting requests |
| Ground truth         | Expected answer, SQL, metric logic and caveats       | SME / analytics engineer         | Available for priority questions | Existing reports, SQL and SME sign-off          |
| Correctness criteria | SQL, metric, grain, filter and answer accuracy       | QA / AI architect                | Defined before pilot             | Evaluation rubric                               |
| Safety criteria      | Access, PII, small cohort and restricted field tests | Security / governance            | Defined before prototype         | Security test cases                             |
| Operational metrics  | Latency, cost, error rate and timeout thresholds     | Platform owner                   | Indicative targets               | Monitoring plan                                 |
| Feedback model       | User feedback categories and triage route            | Product owner                    | Defined for pilot                | Feedback workflow                               |

### 3.9 Operating model framing

| Ownership area | Proposed owner                  | Responsibility                                         | MVP need           | Open question             |
|----------------|---------------------------------|--------------------------------------------------------|--------------------|---------------------------|
| Product        | Product owner                   | Roadmap, scope, prioritisation and user experience     | Required           | Confirm long-term owner   |
| Business       | Business sponsor                | Business value and decision outcomes                   | Required           | Confirm sponsor and forum |
| Semantic       | Metric owners / analytics       | Metrics, definitions, joins, filters and glossary      | Required           | Confirm decision rights   |
| Data           | Data owners / data engineering  | Quality, freshness, lineage and source changes         | Required           | Confirm operational SLA   |
| Technical      | Platform / AI owner             | App, prompts, orchestration, connectors and deployment | Required           | Confirm support model     |
| Security       | Security / governance           | Access, masking, audit and compliance controls         | Required           | Confirm approval path     |
| Evaluation     | QA / analytics / SMEs           | Golden questions, tests and thresholds                 | Required           | Confirm ongoing owner     |
| Support        | Product / BI / platform support | Issue triage and user support                          | Required for pilot | Confirm escalation route  |

## 4 Activity scorecards

### 4.1 Business framing scorecard

| Criterion         | Green                                 | Amber                               | Red                        |
|-------------------|---------------------------------------|-------------------------------------|----------------------------|
| Business problem  | Clear, specific and valuable          | Broad but directionally clear       | Generic or technology-led  |
| MVP domain        | Single priority domain agreed         | Domain likely but not confirmed     | Multiple competing domains |
| Scope boundary    | In-scope and out-of-scope clear       | Some boundary questions remain      | Scope open-ended           |
| Sponsor ownership | Sponsor and business owner confirmed  | Sponsor identified but role unclear | No accountable sponsor     |
| Success criteria  | Measurable outcomes defined           | Outcomes qualitative only           | No success criteria        |
| Budget envelope   | Budget range and approval route clear | Budget assumption only              | No funding view            |

### 4.2 User and workflow discovery scorecard

| Criterion           | Green                                   | Amber                            | Red                            |
|---------------------|-----------------------------------------|----------------------------------|--------------------------------|
| Target users        | First user group clearly defined        | Multiple candidate groups remain | User group unclear             |
| Workflow fit        | Clear workflow and decision context     | Workflow partly understood       | No clear workflow              |
| Question backlog    | 30–50 candidate questions captured      | Initial questions captured       | Few or vague questions         |
| Frequency and value | Frequent or high-value questions        | Value plausible but unquantified | Low frequency or unclear value |
| Output expectations | Answer format and trust needs clear     | Some uncertainty remains         | Expectations undefined         |
| Human review needs  | Escalation and refusal cases identified | Some review needs unclear        | No control model               |

### 4.3 Initial data landscape scan scorecard

| Criterion         | Green                                                 | Amber                                 | Red                           |
|-------------------|-------------------------------------------------------|---------------------------------------|-------------------------------|
| Candidate sources | Likely sources identified for most priority questions | Sources identified for some questions | Sources unclear               |
| Ownership         | Business and technical owners known                   | Some owners missing                   | Owners unclear                |
| Trusted assets    | Certified or trusted assets likely available          | Mixed trusted and informal assets     | No trusted assets identified  |
| Coverage          | Coverage appears sufficient for MVP                   | Some coverage questions remain        | Material coverage gaps likely |
| Freshness         | Freshness likely adequate                             | Freshness uncertain                   | Freshness likely unsuitable   |
| Known data risks  | Key risks captured for Step 2                         | Some risks captured                   | Risks unknown                 |

### 4.4 Initial semantic framing scorecard

| Criterion         | Green                                        | Amber                                    | Red                    |
|-------------------|----------------------------------------------|------------------------------------------|------------------------|
| Key metrics       | Priority metrics identified and likely owned | Metrics identified but ownership unclear | Metrics unclear        |
| Business terms    | Main ambiguous terms captured                | Some ambiguity remains                   | Ambiguity not assessed |
| Dimensions        | Key dimensions identified                    | Some dimensions uncertain                | Dimensions unclear     |
| Filters           | Likely standard exclusions known             | Filters partly known                     | No filter assumptions  |
| Certified sources | Candidate official sources identified        | Multiple sources compete                 | No source of truth     |
| Semantic risk     | Material risks visible for Step 2            | Some risks captured                      | Semantic risk unknown  |

### 4.5 Security and governance framing scorecard

| Criterion              | Green                                 | Amber                             | Red                    |
|------------------------|---------------------------------------|-----------------------------------|------------------------|
| User access model      | Existing access model likely reusable | Adaptation needed                 | No access model        |
| Sensitive data         | Sensitive data known and manageable   | Classification incomplete         | Sensitivity unknown    |
| Compliance constraints | Key constraints understood            | Some constraints pending          | Compliance not engaged |
| Audit needs            | Logging and audit needs clear         | Partial audit view                | Audit unclear          |
| Exposure controls      | High-level controls agreed            | Some controls unresolved          | No safe exposure model |
| Approval route         | Security and risk owners engaged      | Owners identified but not engaged | No approval path       |

### 4.6 Solution architecture framing scorecard

| Criterion           | Green                                               | Amber                   | Red                      |
|---------------------|-----------------------------------------------------|-------------------------|--------------------------|
| Platform fit        | Existing platforms can support MVP                  | Some platform gaps      | No viable platform route |
| Model policy        | Approved LLM route clear                            | Approval pending        | No approved model route  |
| Data connectivity   | Query route likely available                        | Connectivity uncertain  | No safe query path       |
| Validation controls | SQL and safety controls feasible                    | Controls need design    | Controls unclear         |
| Deployment route    | Environments and release route known                | Some governance pending | No deployment path       |
| Non-functional view | Latency, cost, reliability and audit needs captured | Partial view            | Not assessed             |

### 4.7 Delivery planning and MVP boundary

| Criterion        | Green                                    | Amber                            | Red                        |
|------------------|------------------------------------------|----------------------------------|----------------------------|
| MVP boundary     | Clear and realistic                      | Some scope uncertainty           | Scope too broad or unclear |
| Timeline         | Plausible timeline agreed                | Timeline tight or assumption-led | Timeline unrealistic       |
| Team capacity    | Required roles available                 | Some roles constrained           | Critical roles unavailable |
| Budget           | Budget envelope and approval route clear | Budget indicative only           | No budget route            |
| Backlog          | Initial backlog structured               | Backlog incomplete               | No delivery backlog        |
| Governance gates | Decision points clear                    | Some gates unclear               | No approval path           |

### 4.8 Evaluation design framing scorecard

| Criterion           | Green                             | Amber                  | Red                    |
|---------------------|-----------------------------------|------------------------|------------------------|
| Golden questions    | Representative set defined        | Initial set incomplete | No question set        |
| Ground truth        | Owners and validation route clear | Some ownership gaps    | No validation owner    |
| Quality dimensions  | Scoring criteria defined          | Criteria partial       | No evaluation approach |
| Safety tests        | Safety scenarios identified       | Some scenarios missing | Safety not assessed    |
| Regression approach | Rerun approach defined            | Manual approach only   | No regression plan     |
| Feedback loop       | Feedback capture and triage clear | Partial feedback route | No feedback process    |

### 4.9 Operating model framing scorecard

| Criterion           | Green                                       | Amber                         | Red                   |
|---------------------|---------------------------------------------|-------------------------------|-----------------------|
| Product ownership   | Clear owner and roadmap accountability      | Interim owner only            | No owner              |
| Business ownership  | Sponsor and outcome owner clear             | Sponsor unclear               | No business owner     |
| Semantic ownership  | Metric decision rights clear                | Some owners missing           | No semantic ownership |
| Technical ownership | Platform and application owner clear        | Split ownership unresolved    | No support owner      |
| Security ownership  | Security and audit responsibilities clear   | Some responsibilities unclear | No security owner     |
| Support model       | Triage and escalation model defined         | Informal support only         | No support route      |
| Adoption approach   | Training and communication approach defined | Adoption assumptions only     | No adoption plan      |

## 5 Overall phase readiness scorecard

| Readiness area                    | Rating              | Evidence                                                | Key risk                          | Action required                     | Owner                   |
|-----------------------------------|---------------------|---------------------------------------------------------|-----------------------------------|-------------------------------------|-------------------------|
| Business value readiness          | Green / Amber / Red | Problem statement, value case, success criteria         | Weak value case                   | Refine use case or pause            | Sponsor / product owner |
| MVP scope readiness               | Green / Amber / Red | Domain, users, included / excluded areas                | Scope too broad                   | Narrow MVP boundary                 | Product owner           |
| User and workflow readiness       | Green / Amber / Red | User groups, workflows, priority questions              | Low adoption or weak fit          | Validate with users                 | Product owner / BA      |
| Data landscape readiness          | Green / Amber / Red | Candidate sources and ownership                         | Data not available or not trusted | Move to Step 2 validation           | Data architect          |
| Semantic readiness                | Green / Amber / Red | Draft metrics, terms, filters, joins                    | Definitions inconsistent          | Create semantic decision log        | Analytics engineer      |
| Security and governance readiness | Green / Amber / Red | Initial access, classification and audit assumptions    | Exposure risk underestimated      | Security review before prototype    | Security architect      |
| Architecture feasibility          | Green / Amber / Red | Platform, model, integration and deployment assumptions | No approved technical route       | Architecture review                 | AI architect            |
| Evaluation readiness              | Green / Amber / Red | Golden question plan and quality dimensions             | No objective success measure      | Define evaluation approach          | AI architect / QA       |
| Delivery readiness                | Green / Amber / Red | Timeline, backlog, budget, capacity                     | MVP not deliverable               | Re-plan or reduce scope             | Delivery lead           |
| Operating model readiness         | Green / Amber / Red | Ownership, support and adoption assumptions             | No sustainable run model          | Define RACI and support route       | Product owner           |
| Overall framing readiness         | Green / Amber / Red | Phase-gate decision pack                                | Proceeding with weak foundations  | Proceed / pause / re-scope decision | Sponsor                 |

Suggested rating logic:

| Rating | Meaning                                                  |
|--------|----------------------------------------------------------|
| Green  | Ready for governed data layer with limited caveats       |
| Amber  | Usable for MVP if specific gaps are resolved or accepted |
| Red    | Not ready; material blocker exists                       |
| Grey   | Not assessed yet                                         |

## 6 Risk, decision, assumption and dependency logs

### 6.1 Risk log

| Risk                                                                       | Impact                                                 | Likelihood | Mitigation                                                                      | Owner                   | Status |
|----------------------------------------------------------------------------|--------------------------------------------------------|------------|---------------------------------------------------------------------------------|-------------------------|--------|
| T2D is pursued because of GenAI interest rather than a clear business need | Low adoption, weak value case, poor prioritisation     | Medium     | Anchor scope in priority decisions, workflows and measurable outcomes           | Sponsor / product owner | Open   |
| MVP scope is too broad                                                     | Delivery becomes unmanageable and answer quality drops | High       | Start with one domain, one user group and bounded question set                  | Product owner           | Open   |
| Priority questions are vague or not frequent enough                        | T2D may not be the right solution                      | Medium     | Validate questions with users and compare against dashboard/report alternatives | Business analyst        | Open   |
| No clear sponsor or decision owner                                         | Delayed decisions and weak accountability              | Medium     | Confirm sponsor, decision rights and governance forum during framing            | Delivery lead           | Open   |
| Data availability is assumed but not validated                             | Step 2 may reveal major blockers                       | Medium     | Capture candidate sources and known gaps; validate in Step 2                    | Data architect          | Open   |
| Metrics are inconsistent across teams                                      | Conflicting answers and low trust                      | High       | Create semantic decision log and identify metric owners                         | Analytics engineer      | Open   |
| Security constraints are underestimated                                    | Security approval may block MVP                        | Medium     | Engage security, DPO and governance early                                       | Security architect      | Open   |
| Budget excludes run and support costs                                      | MVP may be unsustainable                               | Medium     | Include platform, model, warehouse, support and semantic maintenance costs      | Sponsor / finance       | Open   |
| Evaluation approach is left too late                                       | Cannot prove correctness or safety                     | Medium     | Define golden question plan during framing                                      | AI architect / QA       | Open   |
| Operating model is unclear                                                 | Prototype cannot transition to live service            | Medium     | Define ownership and support assumptions before build                           | Product owner           | Open   |

### 6.2 Decision log

| Decision                                   | Options                                                                        | Recommended option                                                      | Decision owner           | Due date       | Status |
|--------------------------------------------|--------------------------------------------------------------------------------|-------------------------------------------------------------------------|--------------------------|----------------|--------|
| Which domain should be used for MVP?       | Finance / Sales / Operations / Customer / Product / Risk                       | Select one high-value, data-ready domain                                | Sponsor / product owner  | End of framing | Open   |
| Which user group should be included first? | Executives / managers / analysts / frontline users                             | Start with bounded group with clear workflow and support                | Product owner            | End of framing | Open   |
| What is included in MVP?                   | Broad assistant / bounded question set / report replacement / analyst co-pilot | Bounded question set linked to specific decisions                       | Product owner            | End of framing | Open   |
| What is explicitly out of scope?           | Cross-domain joins / PII / row-level exports / forecasting / agentic actions   | Exclude high-risk and poorly governed areas from MVP                    | Product owner / security | End of framing | Open   |
| What success measures apply?               | Adoption / accuracy / time saved / cost per answer / satisfaction / trust      | Use a balanced set of business, quality, safety and operational metrics | Sponsor / product owner  | End of framing | Open   |
| What is the approval path?                 | Sponsor only / steering group / architecture / security / data governance      | Use proportionate phase gates for scope, security, pilot and go-live    | Delivery lead            | End of framing | Open   |
| What budget is available?                  | Discovery only / MVP / pilot / production / run                                | Confirm budget across delivery and run                                  | Sponsor / finance        | End of framing | Open   |
| Should T2D proceed to Step 2?              | Proceed / pause / re-scope / stop                                              | Proceed only if value, scope, ownership and feasibility are sufficient  | Sponsor                  | End of framing | Open   |

### 6.3 Assumption log

| Assumption                                                            | Impact if wrong                      | Validation method                     | Owner              | Status      |
|-----------------------------------------------------------------------|--------------------------------------|---------------------------------------|--------------------|-------------|
| A high-value use case exists for T2D                                  | Project may not justify investment   | Confirm with sponsor and target users | Product owner      | To validate |
| Priority users have recurring questions not well served by current BI | T2D may not be the right solution    | User interviews and workflow review   | Business analyst   | To validate |
| Candidate data exists for priority questions                          | Step 2 may expose data blockers      | Initial data landscape scan           | Data architect     | To validate |
| Existing reports or dashboards can provide starting logic             | Metric assumptions may be wrong      | Compare with BI owners and SMEs       | Analytics engineer | To validate |
| Security constraints can be addressed within MVP                      | Prototype may be blocked             | Security and DPO review               | Security architect | To validate |
| Approved enterprise model and deployment route exists                 | Architecture may need rework         | CTO/platform review                   | AI architect       | To validate |
| SMEs are available to validate questions and answers                  | Evaluation may be weak               | Confirm SME capacity                  | Product owner      | To validate |
| Budget can cover delivery and run costs                               | MVP may not be sustainable           | Finance review                        | Sponsor            | To validate |
| Product and support ownership can be assigned                         | Capability may not scale after pilot | Operating model review                | Delivery lead      | To validate |

### 6.4 Dependency log

| Dependency                                   | Needed by                            | Owner                   | Due date       | Status | Impact if delayed                    |
|----------------------------------------------|--------------------------------------|-------------------------|----------------|--------|--------------------------------------|
| Sponsor and decision forum confirmed         | Scope and proceed decision           | Sponsor / delivery lead | End of framing | Open   | Decisions delayed                    |
| Priority domain selected                     | User discovery and data scan         | Product owner           | End of framing | Open   | Scope remains too broad              |
| Target users identified                      | Workflow discovery and access review | Product owner           | End of framing | Open   | User needs unclear                   |
| Initial question backlog captured            | Data and semantic readiness          | Business analyst        | End of framing | Open   | Step 2 lacks focus                   |
| Candidate reports and dashboards identified  | Data landscape scan                  | BI lead / data analyst  | End of framing | Open   | Source discovery delayed             |
| Candidate data owners identified             | Step 2 validation                    | Data architect          | End of framing | Open   | Ownership unclear                    |
| Security and governance stakeholders engaged | Access and exposure framing          | Security architect      | End of framing | Open   | Late security blocker                |
| Architecture standards confirmed             | Solution feasibility                 | AI architect / CTO      | End of framing | Open   | Technical route unclear              |
| Budget envelope confirmed                    | MVP planning                         | Sponsor / finance       | End of framing | Open   | Delivery cannot be committed         |
| SME availability confirmed                   | Evaluation and semantic validation   | Product owner           | End of framing | Open   | Ground truth and definitions delayed |

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
