---
layout: default
title: Skill reference
permalink: /skills/reference/
description: Human-readable reference for the nine portable Research Wiki agent skills.
---

# Skill reference

These pages explain the canonical machine-readable skills without changing their payloads. Download the linked `SKILL.md` file when configuring a client.

## Setup and discovery {#setup-and-discovery}

Use for a first connection or to diagnose authentication, permissions, and capability readiness.

1. Load the entry skill.
2. Authenticate through the client.
3. Read the capability matrix.
4. List tools visible to the current identity.
5. Select only ready capabilities and stop on typed errors.

Completion requires successful scoped discovery without widening permissions or bypassing a disabled capability.

- [Download canonical skill]({{ '/skills/setup-and-discovery/SKILL.md' | relative_url }})
- [Open machine schema]({{ '/skills/setup-and-discovery/schema.json' | relative_url }})

## Evidence-first research {#evidence-first-research}

Use for source-backed questions, exact values, discovery, comparisons, and explicit limitations.

1. Classify the requested answer.
2. Resolve entity, period, source, and access scope.
3. Retrieve only authorized candidates.
4. Open exact passages, cells, pages, or observations.
5. Verify every claim and state unsupported parts.

Completion requires current evidence for every material claim and number. Exact requests abstain rather than silently downgrade.

[Download canonical skill]({{ '/downloads/skills/evidence-first-research/SKILL.md' | relative_url }})

## Company research {#company-research}

Use for one entity across documents, structured observations, events, and analyst conclusions.

Resolve one stable identity, freeze the research scope, inspect coverage gaps, retrieve and open evidence, preserve source disagreements, then separate observations from interpretation.

Completion requires an unambiguous entity and current evidence or an explicit limitation for every conclusion.

[Download canonical skill]({{ '/downloads/skills/company-research/SKILL.md' | relative_url }})

## Financial analysis {#financial-analysis}

Use for statements, notes, metrics, ratios, breakdowns, and valuation inputs.

Define complete financial dimensions, select the correct authority, fetch every source cell, reject incompatible units or periods, and calculate only with approved formulas over verified observations.

Completion requires reproducible values, named formula inputs, and citations for every narrative claim.

[Download canonical skill]({{ '/downloads/skills/financial-analysis/SKILL.md' | relative_url }})

## Period comparison {#period-comparison}

Use for quarter, year, entity, version, or restatement comparisons.

Resolve both periods, match dimensions, preserve restatements, fetch both sources, compute only compatible deltas, and leave non-comparable pairs explicit.

Completion requires every comparison to reproduce from cited source values.

[Download canonical skill]({{ '/downloads/skills/period-comparison/SKILL.md' | relative_url }})

## Citation audit {#citation-audit}

Use to review claims, values, tables, and reports for direct source support.

Inventory claims, re-fetch citations, match exact source locations, check versions and numeric fidelity, then classify each claim as supported, partial, contradicted, unresolved, or unauthorized.

Completion requires one audit disposition for every material claim.

[Download canonical skill]({{ '/downloads/skills/citation-audit/SKILL.md' | relative_url }})

## Table reconstruction {#table-reconstruction}

Use when tables span pages or arrive as fragments.

Preserve physical fragments, propose continuations from structural evidence, validate geometry and dimensions, keep ambiguity separate, and project only values that retain source-cell citations.

Completion requires deterministic compatibility for every join. The fallback is separate cited fragments, never fabricated rectangular data.

[Download canonical skill]({{ '/downloads/skills/table-reconstruction/SKILL.md' | relative_url }})

## Source intake {#source-intake}

Use when authorized documents enter governed evidence.

Declare rights, resolve identity, submit immutable bytes once, monitor without exposing content, validate complete citation-addressable output, review ambiguity, and publish only after every gate passes.

Completion requires a terminal disposition for every processing unit and explicit publication or withholding.

[Download canonical skill]({{ '/downloads/skills/source-intake/SKILL.md' | relative_url }})

## Working project {#working-project}

Use for editable analyst notes and cited drafts that must remain separate from source authority.

Define scope, collect references, label claim types, revalidate citations, preserve history, and export with limitations and unresolved conflicts.

Completion requires current evidence or an unresolved label for every material claim. Editable notes never become source authority.

[Download canonical skill]({{ '/downloads/skills/working-project/SKILL.md' | relative_url }})
