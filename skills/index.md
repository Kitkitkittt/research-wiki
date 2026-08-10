---
layout: default
title: Skills
permalink: /skills/
---

# Skills

Skills are portable process contracts for AI clients. Read the [human reference](reference.md), download canonical `SKILL.md` payloads individually, or copy them from the [portable source template](../plugins/). This site does not configure a client or host an MCP service.

## Setup

| Skill | Trigger | Completion criterion |
| --- | --- | --- |
| [Setup and discovery](reference.md#setup-and-discovery) | A client connects or diagnoses available capabilities | Authentication succeeds and only ready, permitted capabilities are selected |

## Research

| Skill | Trigger | Completion criterion |
| --- | --- | --- |
| [Evidence-first research](reference.md#evidence-first-research) | A research question needs cited evidence | Every material claim has current authorized evidence or an explicit limitation |
| [Company research](reference.md#company-research) | One entity needs cross-source research | Entity and coverage are explicit; conclusions remain cited |
| [Financial analysis](reference.md#financial-analysis) | Statements, notes, metrics, ratios, or breakdowns | Every value retains complete dimensions and source evidence |
| [Period comparison](reference.md#period-comparison) | Values or claims need cross-period comparison | Every pair is dimension-compatible or explicitly non-comparable |

## Evidence integrity

| Skill | Trigger | Completion criterion |
| --- | --- | --- |
| [Citation audit](reference.md#citation-audit) | Existing claims need verification | Every citation resolves and supports its claim, or the claim is marked unsupported |
| [Table reconstruction](reference.md#table-reconstruction) | A table spans pages or fragments | Every join is deterministic and cited; ambiguous fragments remain separate |

## Source and analyst work

| Skill | Trigger | Completion criterion |
| --- | --- | --- |
| [Source intake](reference.md#source-intake) | A document enters governed evidence | Every unit is terminal and publication or withholding is explicit |
| [Working project](reference.md#working-project) | Cited evidence enters editable analyst work | Every project claim is cited or unresolved; notes never become authority |

## Installation

Copy a skill directory into the skill location supported by your AI client. Keep the directory name and front-matter `name` stable. Do not add endpoint or credential values to a skill.
