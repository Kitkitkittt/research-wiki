---
layout: default
title: Skills
permalink: /skills/
---

# Skills

Skills are public process contracts for AI clients. Install them individually or use the bundled [Research Wiki agent plugin](../plugins/).

## Research

| Skill | Trigger | Completion criterion |
| --- | --- | --- |
| [Evidence-first research](evidence-first-research/SKILL.md) | A research question needs cited evidence | Every material claim has current authorized evidence or an explicit limitation |
| [Company research](company-research/SKILL.md) | One entity needs cross-source research | Entity and coverage are explicit; conclusions remain cited |
| [Financial analysis](financial-analysis/SKILL.md) | Statements, notes, metrics, ratios, or breakdowns | Every value retains complete dimensions and source evidence |
| [Period comparison](period-comparison/SKILL.md) | Values or claims need cross-period comparison | Every pair is dimension-compatible or explicitly non-comparable |

## Evidence integrity

| Skill | Trigger | Completion criterion |
| --- | --- | --- |
| [Citation audit](citation-audit/SKILL.md) | Existing claims need verification | Every citation resolves and supports its claim, or the claim is marked unsupported |
| [Table reconstruction](table-reconstruction/SKILL.md) | A table spans pages or fragments | Every join is deterministic and cited; ambiguous fragments remain separate |

## Source and analyst work

| Skill | Trigger | Completion criterion |
| --- | --- | --- |
| [Source intake](source-intake/SKILL.md) | A document enters governed evidence | Every unit is terminal and publication or withholding is explicit |
| [Working project](working-project/SKILL.md) | Cited evidence enters editable analyst work | Every project claim is cited or unresolved; notes never become authority |

## Installation

Copy a skill directory into the skill location supported by your AI client. Keep the directory name and front-matter `name` stable. Do not add endpoint or credential values to a skill.
