# Talk-to-Data — Reference Implementation

Reference implementation of the [Talk-to-Data Delivery Blueprint](../docs). It exists to
demonstrate, in working code, the controls the blueprint argues for — as evidence that the design
holds up when built, not as a product.

> **Status: in active development.** Being built with OpenAI, Python, SQL, Azure, Terraform and
> Docker. Sources are SQL tables and views in Azure SQL Database. This README will carry a
> claim-to-code map as components land, so the blueprint and the build can be checked against each
> other.

## What it sets out to demonstrate

| Blueprint claim | Implemented in |
|---|---|
| Access-aware querying — table / column / row filtered by user rights | _to be added_ |
| Deterministic query validation before execution | _to be added_ |
| Metadata grounding to approved metric definitions | _to be added_ |
| Safe failure — clarify / caveat / refuse / escalate | _to be added_ |
| Evaluation harness — ~70 golden questions, ~20 tables, ~30 views | _to be added_ |

## Stack

Python · OpenAI · Azure SQL Database · Terraform · Docker.

## Running it

Setup and run instructions will be added as the implementation lands. Python dependencies are in
the repository-root `requirements.txt`; create the environment from the repo root with `make env`.
