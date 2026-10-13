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

## Retained archive document evidence

This is a separate, conditional document workflow, not an alias for canonical company research. The public reference does not promise that these tools are deployed or ready.

| Tool | Required scope |
| --- | --- |
| `archive.list_documents`, `archive.search` | `research:read` |
| `archive.fetch` | `citations:read` |
| `archive.get_resources` | `resources:read` |

Scopes alone do not grant access: the current runtime must authorize the retained public document membership, caller, and release. Use finite limits and returned pagination cursors; do not widen the archive label or claim canonical mapping from these tools.

1. Initialize an authenticated session and inspect `tools/list`; call `system.describe_capabilities` only if listed. Continue only when current caller-specific discovery reports `archive.list_documents`, `archive.search`, `archive.fetch`, and `archive.get_resources` as callable. Otherwise report **connected, archive research blocked**, with the observed blocker.
2. Use the discovered input schemas: `archive.list_documents(ticker, query='', cursor=0, limit=20)` and `archive.search(question, ticker, limit=5)` require an explicit ticker archive label. A ticker is not a canonical company ID. Never invent a company mapping or omit the ticker to widen retrieval.
3. Preserve returned artifact-version and citation identities. Re-fetch a citation from the same caller's prior search in the current release with `archive.fetch(citation_id)` and compare its evidence before synthesizing a claim. A copied or guessed citation ID is not authority.
4. Request `archive.get_resources(artifact_version_id)` for the returned artifact-version ID only when authorized. Open only runtime-returned archive resource URLs, preserving the original file hash and page location; do not construct canonical navigator links or guess resource IDs.
5. Label the result **retained document evidence**, preserve provenance and limitations, and abstain when source evidence or permission is missing. Retained documents do not become verified structured Financial Truth; a numeric claim still needs exact source dimensions and evidence.

Completion requires an actual authorized search and citation re-fetch, not successful discovery alone. Missing tools, blocked scope, unavailable canonical company mapping, or a resource authorization failure remains a limitation, never a reason to bypass the gate.

## Completion criterion

The workflow is complete when every material claim maps to current authorized evidence, every displayed number preserves its source dimensions, and every unsupported part is recorded as a limitation.

Review the [evidence-first research skill](../skills/reference.md#evidence-first-research), then download its canonical payload from the reference page when configuring a client.
