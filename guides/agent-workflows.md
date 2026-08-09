---
layout: default
title: Agent workflows
permalink: /guides/agent-workflows/
---

# Agent workflows

MCP is the analyst-facing tool contract. Multi-agent work stays bounded behind one server-side coordinator: the client submits a goal, while the server controls specialist roles, allowed tools, budgets, deadlines, evidence contracts, and result verification.

## Coordinator responsibilities

1. Classify the request without granting access.
2. Freeze entity, period, answer class, access lane, and evidence authority.
3. Build a bounded dependency graph.
4. Assign each task one specialist objective and allowlisted tool set.
5. Run independent retrieval tasks concurrently within the published ceiling.
6. Verify citations before synthesis.
7. Return one immutable result or typed abstention.

## Suggested specialist lanes

- verified structured facts;
- financial statements;
- financial notes;
- annual and governance documents;
- analyst research;
- structured market observations;
- general document fallback;
- claim and citation verification.

A lane is an authority constraint, not an agent personality. A model may interpret verified evidence but cannot upgrade its authority.

## Exact answers

Use a zero-model path when a requested fact is already represented by a verified structured observation. Preserve the source dimensions, unit, period, currency, scope, and citation.

## Narrative answers

Provide the model only authorized, bounded, citation-addressable evidence. Require claim-to-citation closure and preserve conflicting versions rather than silently choosing one.

## Completion criterion

The workflow is complete when every material claim maps to current authorized evidence, every displayed number preserves its source dimensions, and every unsupported part is recorded as a limitation.

Install the [evidence-first research skill](../skills/evidence-first-research/SKILL.md) as the default agent process.
