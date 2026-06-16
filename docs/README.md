# Talk-to-Data Delivery Blueprint — Documents

The full blueprint. Start with the [master](master.md) for the strategic overview, then go deeper
by phase. Formatted PDF versions of every document are in [`pdf/`](pdf).

## Master

[master.md](master.md) — delivery logic, risks, principles, decision gates and operating model.

## Phases

| Phase | Guide | Annex pack |
|---|---|---|
| 1 | [Framing](phases/phase_1_framing.md) | [annex](annexes/phase_1_framing_annexes.md) |
| 2 | [Data & semantic readiness](phases/phase_2_data_semantic_readiness.md) | [annex](annexes/phase_2_data_semantic_readiness_annexes.md) |
| 3 | [Governed data foundation](phases/phase_3_governed_data_foundation.md) | [annex](annexes/phase_3_governed_data_foundation_annexes.md) |
| 4 | [Design architecture](phases/phase_4_design_architecture.md) | [annex](annexes/phase_4_design_architecture_annexes.md) |
| 5 | [Prototype / MVP build](phases/phase_5_prototype_mvp_build.md) | [annex](annexes/phase_5_prototype_mvp_build_annexes.md) |
| 6 | [Validation, assurance & remediation](phases/phase_6_validation_assurance_remediation.md) | [annex](annexes/phase_6_validation_assurance_remediation_annexes.md) |
| 7 | [Controlled pilot & user testing](phases/phase_7_controlled_pilot.md) | [annex](annexes/phase_7_controlled_pilot_annexes.md) |
| 8 | [Production readiness & release](phases/phase_8_production_readiness.md) | [annex](annexes/phase_8_production_readiness_annexes.md) |
| 9 | [Operate, adopt & improve](phases/phase_9_operate_adopt_improve.md) | [annex](annexes/phase_9_operate_adopt_improve_annexes.md) |

Each main guide covers delivery logic, decisions, risks, required outputs and handover. Each annex
pack holds templates, checklists, registers, scorecards and worked examples to adapt, not follow
mechanically.

## PDFs

[`pdf/`](pdf) holds a formatted version of every document above. They are generated from the
Markdown — regenerate them after any edit, from the repository root:

```bash
make pdf
```
