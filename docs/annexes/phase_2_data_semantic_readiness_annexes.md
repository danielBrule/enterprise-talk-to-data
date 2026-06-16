# Talk-to-Data Delivery Blueprint — Phase 2 Annexes: Data & Semantic Readiness Assessment

*Daniel Brule · Talk-to-Data Delivery Blueprint · v1.0 · June 2026*

---

**Table of contents**

- [1 How to use this annex pack](#1-how-to-use-this-annex-pack)
- [2 Activity question banks](#2-activity-question-banks)
  - [2.1 Validated source inventory](#21-validated-source-inventory)
  - [2.2 Question-to-data mapping](#22-question-to-data-mapping)
  - [2.3 Data model review](#23-data-model-review)
  - [2.4 Metric discovery](#24-metric-discovery)
  - [2.5 Data quality assessment](#25-data-quality-assessment)
  - [2.6 Metadata assessment](#26-metadata-assessment)
  - [2.7 Access review](#27-access-review)
  - [2.8 Gap analysis](#28-gap-analysis)
- [3 Output templates](#3-output-templates)
  - [3.1 Validated source inventory](#31-validated-source-inventory)
  - [3.2 Question-to-data mapping](#32-question-to-data-mapping)
  - [3.3 Data model review](#33-data-model-review)
  - [3.4 Metric discovery](#34-metric-discovery)
  - [3.5 Data quality assessment](#35-data-quality-assessment)
  - [3.6 Metadata assessment](#36-metadata-assessment)
  - [3.7 Access review](#37-access-review)
  - [3.8 Gap analysis](#38-gap-analysis)
    - [3.8.1 Output: confirmed answerability matrix](#381-output-confirmed-answerability-matrix)
    - [3.8.2 Output: remediation plan](#382-output-remediation-plan)
- [4 Activity scorecards](#4-activity-scorecards)
  - [4.1 Validated source inventory](#41-validated-source-inventory)
  - [4.2 Question-to-data mapping](#42-question-to-data-mapping)
  - [4.3 Data model review](#43-data-model-review)
  - [4.4 Metric discovery](#44-metric-discovery)
  - [4.5 Data quality assessment](#45-data-quality-assessment)
  - [4.6 Metadata assessment](#46-metadata-assessment)
  - [4.7 Access review](#47-access-review)
  - [4.8 Gap analysis](#48-gap-analysis)
- [5 Overall phase readiness scorecard](#5-overall-phase-readiness-scorecard)
- [6 Risk, decision, assumption and dependency logs](#6-risk-decision-assumption-and-dependency-logs)
  - [6.1 Risks](#61-risks)
  - [6.2 Decisions](#62-decisions)
  - [6.3 Assumptions](#63-assumptions)
  - [6.4 Dependencies](#64-dependencies)

---

## 1 How to use this annex pack

This annex pack contains detailed tools and templates supporting the Phase 1 Framing Guide. It is intended for facilitation, documentation and project delivery. The main guide explains the framing logic; this annex provides the reusable working material.

## 2 Activity question banks

### 2.1 Validated source inventory

| Area                  | Questions                                                                                                                                           |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Source identification | Which systems, tables, marts, dashboards, BI models, APIs or files are believed to be relevant to the priority use case?                            |
| Trusted status        | Based on current business and platform knowledge, which assets are considered certified, trusted, experimental, deprecated or no longer maintained? |
| Ownership             | Who is believed to own or maintain each relevant source, table, mart, dashboard or API?                                                             |
| Current usage         | Which assets are currently used, formally or informally, to answer the priority business questions?                                                 |
| Accessibility         | Are these assets expected to be accessible for discovery, POC and production, or are there known constraints?                                       |
| Refresh               | What is the understood refresh frequency and expected latency of each source?                                                                       |
| Suitability           | Which assets appear suitable for direct querying, semantic-layer access, reference only or exclusion from MVP?                                      |
| Known caveats         | What known caveats, limitations or concerns should be captured before deeper validation?                                                            |

 

### 2.2 Question-to-data mapping

| Area                  | Questions                                                             |
|-----------------------|-----------------------------------------------------------------------|
| Question coverage     | Which priority questions can be mapped to candidate data assets?      |
| Metric mapping        | Which metrics are needed for each question?                           |
| Dimension mapping     | Which dimensions are needed for slicing, filtering or comparison?     |
| Source mapping        | Which source-of-truth asset should be used for each question?         |
| Initial answerability | Does the question appear answerable, partially answerable or unknown? |
| Validation need       | What must be validated before confirming answerability?               |
| MVP decision          | Should the question be included, restricted, deferred or excluded?    |

### 2.3 Data model review

| Area        | Questions                                                                                    |
|-------------|----------------------------------------------------------------------------------------------|
| Entities    | What are the main entities: customer, account, transaction, product, order, contract, event? |
| Grain       | What is the grain of each fact table or mart?                                                |
| Keys        | What are the primary, foreign and business keys?                                             |
| Join paths  | Which joins are approved and safe?                                                           |
| Join risks  | Are there many-to-many joins, duplicate keys or ambiguous relationships?                     |
| Time logic  | Which dates should be used: order date, invoice date, payment date, snapshot date?           |
| Aggregation | At what level can data be safely aggregated?                                                 |
| Reusability | Can the model support multiple priority questions or only narrow cases?                      |

### 2.4 Metric discovery

| Area              | Questions                                                                   |
|-------------------|-----------------------------------------------------------------------------|
| Metric definition | What is the approved definition for each KPI?                               |
| Calculation logic | Is the formula documented in SQL, BI, dbt, semantic layer or analyst logic? |
| Standard filters  | What exclusions apply by default?                                           |
| Dimensions        | Which dimensions are approved for slicing the metric?                       |
| Inconsistencies   | Do teams define the metric differently?                                     |
| Ownership         | Who owns and approves the metric definition?                                |
| Source of truth   | Which dashboard, mart, finance pack or semantic model is certified?         |
| Ambiguity         | Which business terms require clarification before answering?                |

### 2.5 Data quality assessment

| Area           | Questions                                                      |
|----------------|----------------------------------------------------------------|
| Completeness   | Are required fields populated sufficiently?                    |
| Freshness      | Is data updated frequently enough for the use case?            |
| Duplicates     | Are there duplicate customers, transactions, orders or events? |
| Reconciliation | Does the data reconcile to trusted reports or finance packs?   |
| Nulls          | Are there critical null values in metrics, keys or dimensions? |
| Timeliness     | Are there delays, backfills or late-arriving data?             |
| Known issues   | What issues are already known by data owners or analysts?      |
| Impact         | Which priority questions are affected by quality issues?       |

### 2.6 Metadata assessment

| Area               | Questions                                                         |
|--------------------|-------------------------------------------------------------------|
| Catalogue          | Are relevant assets registered in a data catalogue?               |
| Ownership          | Are business and technical owners documented?                     |
| Lineage            | Can key metrics be traced from report to model, table and source? |
| Glossary           | Are business terms and synonyms documented?                       |
| Documentation      | Are table, column and metric descriptions usable?                 |
| Freshness metadata | Is refresh information visible?                                   |
| Certification      | Can users distinguish trusted from non-trusted assets?            |
| T2D usability      | Is metadata structured enough for retrieval by the T2D system?    |

### 2.7 Access review

| Area                  | Questions                                                                           |
|-----------------------|-------------------------------------------------------------------------------------|
| User groups           | Who are the target users for MVP?                                                   |
| Authentication        | How are users authenticated?                                                        |
| Authorisation         | Should T2D inherit existing permissions or apply a new policy layer?                |
| Row-level security    | Are users restricted by region, account, customer, business unit or portfolio?      |
| Column-level security | Which fields must be masked, hidden or restricted?                                  |
| Sensitive data        | Which datasets contain PII, financial, confidential or regulated data?              |
| Aggregation risk      | Could users infer restricted information through small cohorts or repeated queries? |
| Output controls       | Can users see SQL, export results or access row-level detail?                       |
| Logging               | What must be logged for audit and compliance?                                       |

### 2.8 Gap analysis

| Area          | Questions                                                                            |
|---------------|--------------------------------------------------------------------------------------|
| Answerability | Which priority questions are answerable, partially answerable or not yet answerable? |
| Data gaps     | What data is missing, inaccessible or not trusted?                                   |
| Semantic gaps | Which definitions, filters, joins or terms are unclear?                              |
| Quality gaps  | Which quality issues block or limit answers?                                         |
| Metadata gaps | What ownership, lineage or documentation is missing?                                 |
| Access gaps   | Which permissions or sensitivity decisions are unresolved?                           |
| Remediation   | What must be fixed, accepted, restricted or deferred?                                |
| MVP decision  | Which questions should be included, restricted or excluded from MVP?                 |

## 3 Output templates

These columns are illustrative examples only. They are intended to show the expected structure and level of detail.

### 3.1 Validated source inventory

| Asset                    | Type         | System             | Owner             | Source of truth status    | Trusted status | Refresh        | Access status | MVP relevance | Supported question                    | Known caveats / comments                          |
|--------------------------|--------------|--------------------|-------------------|---------------------------|----------------|----------------|---------------|---------------|---------------------------------------|---------------------------------------------------|
| finance_revenue_mart     | Mart         | Data warehouse     | Finance Analytics | Authoritative for revenue | Certified      | Daily          | Available     | High          | Revenue by region                     | Official source for revenue reporting             |
| Sales pipeline dashboard | BI dashboard | Power BI / Tableau | Sales Ops         | Reference only            | Trusted        | Daily          | Available     | Medium        | Pipeline conversion, sales validation | Useful for metric validation, not direct querying |
| crm_opportunity_raw      | Raw table    | CRM replica        | CRM Platform      | Not authoritative for MVP | Experimental   | Near real-time | Restricted    | Low           | Opportunity-level exploration         | Raw object; not suitable for MVP without curation |

 

### 3.2 Question-to-data mapping

| Priority question                      | Metric(s)        | Dimensions      | Candidate source               | Initial status       | What needs validation                           | MVP decision         |
|----------------------------------------|------------------|-----------------|--------------------------------|----------------------|-------------------------------------------------|----------------------|
| What was revenue last month by region? | Net revenue      | Month, region   | finance_revenue_mart           | Likely answerable    | Confirm region hierarchy and revenue definition | Include              |
| Which customers have declining spend?  | Customer revenue | Customer, month | Revenue mart + customer master | Partially answerable | Validate customer join and minimum time window  | Include if validated |
| What is churn by segment?              | Churn rate       | Segment, month  | CRM + billing data             | Unknown              | Confirm churn definition and segment ownership  | Pending              |

Suggested status values:

| Status               | Meaning                                              |
|----------------------|------------------------------------------------------|
| Answerable           | Likely answerable with existing trusted data         |
| Partially answerable | Possible, but with caveats or unresolved assumptions |
| Unknown              | Requires further validation                          |
| Not answerable       | Missing data, definition, access or quality          |
| Out of scope         | Not suitable for MVP                                 |

### 3.3 Data model review

| Entity / table       | Grain        | Primary key     | Approved joins            | Risky joins      | Date logic       | Known issues           | Decision        |
|----------------------|--------------|-----------------|---------------------------|------------------|------------------|------------------------|-----------------|
| finance_revenue_mart | Invoice line | invoice_line_id | Customer, product, region | Opportunity join | Invoice date     | Month-end adjustments  | Use for revenue |
| customer_master      | Customer     | customer_id     | Revenue, account owner    | CRM account ID   | Current snapshot | Duplicate legacy IDs   | Use with caveat |
| crm_opportunity      | Opportunity  | opportunity_id  | Account, owner            | Revenue mart     | Close date       | Stage definitions vary | Reference only  |

### 3.4 Metric discovery

| Metric          | Business definition                          | Calculation logic          | Grain          | Standard filters                          | Approved dimensions                      | Source of truth      | Owner     |
|-----------------|----------------------------------------------|----------------------------|----------------|-------------------------------------------|------------------------------------------|----------------------|-----------|
| Net revenue     | Revenue after discounts, credits and refunds | Sum of net invoice amount  | Invoice line   | Exclude test accounts, cancelled invoices | Month, region, product, customer segment | Finance revenue mart | Finance   |
| Gross margin    | Net revenue less cost of goods sold          | Net revenue - COGS         | Invoice line   | Exclude internal transactions             | Month, product, region                   | Finance pack         | Finance   |
| Active customer | Customer with revenue in last 90 days        | Count distinct customer ID | Customer-month | Exclude internal/test customers           | Segment, region, product                 | Customer mart        | Sales Ops |

**Ambiguity log**

| Term     | Possible meanings                           | Default interpretation   | Clarification needed?       | Owner            | Decision                   |
|----------|---------------------------------------------|--------------------------|-----------------------------|------------------|----------------------------|
| Revenue  | Gross, net, recognised, booked              | Net revenue              | Yes for executive reporting | Finance          | Use net revenue by default |
| Customer | CRM account, billing customer, legal entity | Billing customer         | Yes for sales analysis      | Sales Ops        | Align customer hierarchy   |
| Churn    | No spend, cancelled contract, lost account  | No spend in last 90 days | Yes                         | Customer Success | Not MVP until agreed       |

### 3.5 Data quality assessment

| Dataset / field             | Issue                          | Affected question(s)   | Severity | Business impact             | Remediation                   | Owner             | MVP decision        |
|-----------------------------|--------------------------------|------------------------|----------|-----------------------------|-------------------------------|-------------------|---------------------|
| customer_master.customer_id | Duplicate legacy customer IDs  | Customer trends, churn | High     | Over/under-count customers  | Apply master customer mapping | Data Engineering  | Include if fixed    |
| finance_revenue_mart.region | Region sometimes null          | Revenue by region      | Medium   | Unallocated revenue         | Add “unknown region” rule     | Finance Analytics | Include with caveat |
| crm_opportunity.stage       | Stage definitions inconsistent | Pipeline conversion    | High     | Misleading conversion rates | Standardise stage mapping     | Sales Ops         | Defer               |

Severity scale:

| Rating   | Meaning                                 |
|----------|-----------------------------------------|
| Low      | Minor caveat, does not block MVP        |
| Medium   | Needs caveat, restriction or monitoring |
| High     | Blocks answer or requires remediation   |
| Critical | Should exclude from MVP until resolved  |

### 3.6 Metadata assessment

| Asset / metric   | Catalogue entry | Owner     | Lineage             | Glossary terms | Documentation quality | Certification status | T2D usability | Gap                             |
|------------------|-----------------|-----------|---------------------|----------------|-----------------------|----------------------|---------------|---------------------------------|
| Net revenue      | Yes             | Finance   | Report → mart → ERP | Yes            | Good                  | Certified            | High          | None                            |
| Customer segment | Partial         | Sales Ops | Partial             | Partial        | Medium                | Trusted              | Medium        | Segment definitions need update |
| Churn rate       | No              | Unclear   | No                  | No             | Poor                  | Not certified        | Low           | Owner and definition required   |

### 3.7 Access review

| User group        | Dataset       | Allowed rows     | Restricted columns           | Sensitive fields      | Output restrictions     | Export allowed? | Approval needed  |
|-------------------|---------------|------------------|------------------------------|-----------------------|-------------------------|-----------------|------------------|
| Executives        | Finance mart  | All regions      | None                         | Margin                | Aggregated answers only | No              | Finance          |
| Regional managers | Revenue mart  | Own region       | Margin, customer identifiers | Customer name, margin | No row-level detail     | No              | Regional Finance |
| Analysts          | Curated marts | Approved domains | PII fields masked            | Email, phone, salary  | SQL visible             | Yes, limited    | Data Governance  |

Additional exposure control template:

| Exposure type    | Allowed | Restricted | Blocked | Notes                                  |
|------------------|---------|------------|---------|----------------------------------------|
| Aggregated KPI   | Yes     | —          | —       | Default output for most users          |
| Row-level detail | —       | Yes        | —       | Only for analysts with approved access |
| PII              | —       | —          | Yes     | Excluded from MVP                      |
| Raw SQL          | —       | Yes        | —       | Visible to analysts only               |
| Export           | —       | Yes        | —       | Restricted by role and dataset         |

### 3.8 Gap analysis

#### 3.8.1 Output: confirmed answerability matrix

| Priority question                      | Final status         | Evidence                                            | Blocking issue          | Required action               | Owner             | MVP decision        |
|----------------------------------------|----------------------|-----------------------------------------------------|-------------------------|-------------------------------|-------------------|---------------------|
| What was revenue last month by region? | Answerable           | Certified finance mart and agreed metric            | None                    | None                          | Finance Analytics | Include             |
| Which customers have declining spend?  | Partially answerable | Revenue data exists, customer master has duplicates | Customer identity issue | Apply master customer mapping | Data Engineering  | Include if resolved |
| What is churn by segment?              | Not yet answerable   | No agreed churn definition                          | Semantic disagreement   | Agree definition and owner    | Sales Ops         | Defer               |

#### 3.8.2 Output: remediation plan

| Gap                                | Category     | Impact                                          | Priority | Remediation action                  | Owner              | Dependency    | Decision required       |
|------------------------------------|--------------|-------------------------------------------------|----------|-------------------------------------|--------------------|---------------|-------------------------|
| Churn definition differs by region | Semantic     | Churn questions cannot be answered consistently | High     | Agree standard MVP churn definition | Sales Ops          | Finance input | Include or defer churn  |
| Margin access unclear              | Access       | Risk of exposing sensitive commercial data      | High     | Define role-based margin policy     | Finance / Security | CISO approval | Restrict margin answers |
| Customer duplicates                | Data quality | Customer-level trends may be wrong              | Medium   | Use master customer mapping table   | Data Engineering   | MDM rules     | Include with caveat     |

## 4 Activity scorecards

### 4.1 Validated source inventory

| Criterion                      | Green                                                                              | Amber                                                  | Red                                                         |
|--------------------------------|------------------------------------------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------------|
| Relevant assets identified     | Key systems, marts, BI assets, APIs and files identified for the priority use case | Main assets identified, but some areas still uncertain | Relevant assets unclear or incomplete                       |
| Ownership understood           | Business and technical owners identified for key assets                            | Some owners missing or informal                        | Ownership unclear for critical assets                       |
| Trust and authority understood | Trusted status and likely source-of-truth role are clear for key assets            | Some overlap, disagreement or uncertainty remains      | Trust status unclear and no authoritative source identified |
| Access and refresh understood  | Access route and refresh cadence known for key assets                              | Some access or refresh details uncertain               | Access or refresh constraints unknown                       |
| Suitability for MVP            | Assets classified as direct query, semantic-layer, reference-only or excluded      | Some suitability decisions pending                     | Cannot determine which assets are usable                    |

 

### 4.2 Question-to-data mapping

| Criterion                    | Green                            | Amber                     | Red                           |
|------------------------------|----------------------------------|---------------------------|-------------------------------|
| Priority questions mapped    | Most questions mapped            | Partial mapping           | Few questions mapped          |
| Candidate sources identified | Clear source per question        | Multiple possible sources | No clear source               |
| Validation needs clear       | Open questions documented        | Some gaps unclear         | Validation not defined        |
| MVP decision support         | Supports include/defer decisions | Some uncertainty          | Cannot support scope decision |

### 4.3 Data model review

| Criterion          | Green                        | Amber                 | Red                            |
|--------------------|------------------------------|-----------------------|--------------------------------|
| Grain understood   | Grain clearly documented     | Some uncertainty      | Grain unclear                  |
| Keys understood    | Keys validated               | Some unresolved keys  | Keys unreliable                |
| Join paths         | Approved joins known         | Some risky joins      | Joins ambiguous                |
| Date logic         | Standard date logic agreed   | Multiple date options | No agreed date logic           |
| Aggregation safety | Safe aggregation rules clear | Some caveats          | High risk of wrong aggregation |

### 4.4 Metric discovery

| Criterion          | Green                         | Amber                              | Red                     |
|--------------------|-------------------------------|------------------------------------|-------------------------|
| Metric definitions | Approved definitions exist    | Definitions exist but inconsistent | No agreed definitions   |
| Calculation logic  | Logic documented and reusable | Logic partly documented            | Logic in people’s heads |
| Filters            | Standard filters clear        | Some filters unclear               | No standard filters     |
| Dimensions         | Approved dimensions known     | Some dimension risk                | Dimensions uncontrolled |
| Ownership          | Metric owners confirmed       | Partial ownership                  | No owner                |

### 4.5 Data quality assessment

| Criterion          | Green                   | Amber              | Red                   |
|--------------------|-------------------------|--------------------|-----------------------|
| Completeness       | Sufficient for MVP      | Some gaps          | Major missing data    |
| Freshness          | Meets user need         | Some delays        | Not fresh enough      |
| Reconciliation     | Matches trusted reports | Minor differences  | Material mismatch     |
| Key reliability    | Keys reliable           | Some issues        | Joins unsafe          |
| Issue transparency | Known issues documented | Partial visibility | Unknown quality state |

### 4.6 Metadata assessment

| Criterion           | Green                   | Amber               | Red                |
|---------------------|-------------------------|---------------------|--------------------|
| Catalogue coverage  | Key assets catalogued   | Partial coverage    | Not catalogued     |
| Ownership           | Owners clear            | Some missing owners | Ownership unclear  |
| Lineage             | Lineage available       | Partial lineage     | No lineage         |
| Glossary            | Terms documented        | Some terms missing  | No glossary        |
| Retrieval readiness | Metadata machine-usable | Some manual work    | Not usable for T2D |

### 4.7 Access review

| Criterion           | Green                 | Amber                | Red                   |
|---------------------|-----------------------|----------------------|-----------------------|
| User groups         | Clearly defined       | Some uncertainty     | Undefined             |
| Permissions         | Existing model usable | Needs adaptation     | No clear access model |
| Sensitive data      | Classified            | Partially classified | Unknown sensitivity   |
| Row/column controls | Controls defined      | Some gaps            | Controls missing      |
| Auditability        | Logging needs clear   | Partial logging      | Audit unclear         |

### 4.8 Gap analysis

| Criterion           | Green                                   | Amber                | Red                       |
|---------------------|-----------------------------------------|----------------------|---------------------------|
| Answerability known | Clear status for all priority questions | Some unknowns remain | Many questions unresolved |
| Gaps categorised    | Gaps grouped and prioritised            | Some gaps unclear    | No clear gap view         |
| Owners assigned     | Owners confirmed                        | Partial ownership    | No owners                 |
| Remediation defined | Clear actions and dates                 | Some actions vague   | No plan                   |
| MVP scope decision  | Include/defer decisions clear           | Some open decisions  | MVP scope blocked         |

## 5 Overall phase readiness scorecard

Use this at the end of the phase.

| Readiness area         | Rating              | Evidence | Key risk | Action required | Owner |
|------------------------|---------------------|----------|----------|-----------------|-------|
| Source readiness       | Green / Amber / Red |          |          |                 |       |
| Question coverage      | Green / Amber / Red |          |          |                 |       |
| Data model readiness   | Green / Amber / Red |          |          |                 |       |
| Metric readiness       | Green / Amber / Red |          |          |                 |       |
| Data quality readiness | Green / Amber / Red |          |          |                 |       |
| Metadata readiness     | Green / Amber / Red |          |          |                 |       |
| Access readiness       | Green / Amber / Red |          |          |                 |       |
| Overall MVP readiness  | Green / Amber / Red |          |          |                 |       |

Suggested rating logic:

| Rating | Meaning                                                  |
|--------|----------------------------------------------------------|
| Green  | Ready for governed data layer with limited caveats       |
| Amber  | Usable for MVP if specific gaps are resolved or accepted |
| Red    | Not ready; material blocker exists                       |
| Grey   | Not assessed yet                                         |

## 6 Risk, decision, assumption and dependency logs

### 6.1 Risks

| Risk                                           | Impact                                                   | Likelihood | Mitigation                                                    | Owner                        | Status      |
|------------------------------------------------|----------------------------------------------------------|------------|---------------------------------------------------------------|------------------------------|-------------|
| No agreed source of truth for priority metrics | Conflicting answers and low user trust                   | Medium     | Confirm certified sources with business and data owners       | Analytics Engineer           | Open        |
| Access to required datasets is delayed         | Discovery and validation cannot be completed on time     | High       | Submit access request early and define fallback data assets   | Data Architect               | In progress |
| Metric definitions differ across teams         | Assistant may generate inconsistent or incorrect answers | High       | Create metric decision log and agree MVP definitions          | Business SME / Product Owner | Open        |
| Data quality issues are discovered late        | MVP scope may need to be reduced                         | Medium     | Run early profiling on high-priority datasets                 | Data Engineer                | Open        |
| Sensitive data exposure is underestimated      | Security or compliance approval may be blocked           | Medium     | Complete access and sensitivity review before prototype build | Security Architect           | Open        |

### 6.2 Decisions

| Decision                                    | Options                                                                | Recommended option                                             | Decision owner               | Due date | Status |
|---------------------------------------------|------------------------------------------------------------------------|----------------------------------------------------------------|------------------------------|----------|--------|
| Which data assets are approved for MVP use? | Certified marts only / BI semantic layer / raw tables with controls    | Certified marts and approved semantic assets first             | Data Owner / Product Owner   |          | Open   |
| What is the default definition of revenue?  | Gross revenue / net revenue / recognised revenue                       | Use finance-approved net revenue definition                    | Finance Owner                |          | Open   |
| Should raw SQL be visible to users?         | All users / analysts only / no users                                   | Analysts only for MVP                                          | Product Owner / Security     |          | Open   |
| Which questions are included in MVP?        | All priority questions / only answerable questions / restricted subset | Include answerable and low-risk partially answerable questions | Product Owner                |          | Open   |
| How are unresolved semantic gaps handled?   | Block / caveat / ask clarification / defer                             | Defer high-risk gaps; caveat low-risk gaps                     | Product Owner / Business SME |          | Open   |

### 6.3 Assumptions

| Assumption                                            | Impact if wrong                                         | Validation method                                         | Owner              | Status      |
|-------------------------------------------------------|---------------------------------------------------------|-----------------------------------------------------------|--------------------|-------------|
| Certified marts exist for the priority domain         | Source inventory may need to include lower-level tables | Confirm with data platform and BI teams                   | Data Architect     | To validate |
| Existing BI dashboards reflect trusted business logic | Metric contract may be based on incorrect logic         | Reconcile dashboard logic with SQL/dbt/semantic layer     | Analytics Engineer | To validate |
| Target users can be mapped to existing access roles   | Additional security design may be required              | Compare user groups with current BI / warehouse roles     | Security Architect | To validate |
| Priority questions are representative of MVP usage    | Evaluation set and governed layer may be incomplete     | Validate questions with business SMEs and user interviews | Business Analyst   | To validate |
| Data refresh is sufficient for user expectations      | Users may reject answers as outdated                    | Compare refresh cadence with workflow needs               | Data Engineer      | To validate |

### 6.4 Dependencies

| Dependency                              | Needed by                                               | Owner                            | Due date | Status | Impact if delayed                              |
|-----------------------------------------|---------------------------------------------------------|----------------------------------|----------|--------|------------------------------------------------|
| Access to warehouse / BI semantic model | Source inventory, data model review, quality assessment | Data Platform Team               |          | Open   | Delays validation and answerability assessment |
| Priority question list from framing     | Question-to-data mapping and metric discovery           | Product Owner / Business Analyst |          | Open   | Discovery scope remains unclear                |
| Business SME availability               | Metric discovery and ambiguity resolution               | Business Lead                    |          | Open   | Metric decisions may remain unresolved         |
| Data owner input                        | Source trust status, ownership and quality issues       | Data Owners                      |          | Open   | Source readiness cannot be confirmed           |
| Security / governance input             | Access review and exposure model                        | Security / Governance Lead       |          | Open   | Safe MVP scope cannot be agreed                |
| Existing documentation and SQL examples | Metric contract and semantic grounding                  | BI Team / Analytics Engineering  |          | Open   | More reverse engineering require               |

---

*Talk-to-Data Delivery Blueprint · v1.0 · June 2026*  
*Daniel Brule · [LinkedIn](https://www.linkedin.com/in/danielbrule/) · [Repository](https://github.com/danielBrule/enterprise-talk-to-data-blueprint)*
