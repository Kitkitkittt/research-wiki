---
name: setup-and-discovery
description: Connect a scoped client and discover only ready capabilities.
---

# Research Wiki Setup and Discovery

Skill ID: `skill.setup-and-discovery`
Version: `1.1.0`
Capability content SHA-256: `92235c3af356e49a1c02c9f16665840f1ec6b2931ef4eb0633928b0363c9f2aa`
Readiness: `ready`

Connect a scoped client and discover only ready capabilities.

## Use when

- First connection
- Capability or authentication diagnosis

## Do not use when

- To bypass a disabled capability

## Required permissions

- Scopes: `research:read`
- Lanes: `public, analyst`

## Safe sequence

1. Load the entry skill.
2. Read the capability matrix.
3. List MCP tools visible to the current key.
4. Stop on typed permission or readiness errors.

## Interfaces

- REST: `GET /api/research-brain/runtime/capabilities`
- REST: `GET /api/research-brain/mcp/catalog`
- MCP: `system.describe_capabilities`
- Input: `none`
- Output: `runtime-capabilities-v1`
- Machine schema: [`schema.json`](./schema.json)

## Errors and abstention

- `authentication_required`
- `permission_denied`
- `service_degraded`
- `scope_unavailable`
- Return a typed abstention when the requested authority or scope is unavailable.
- Never relax access, assurance, period, report-scope, QA, or version filters silently.

## Citation rules

- Every material claim must cite a governed citation identity.
- Every displayed numeric value must re-fetch an exact source row or cell.

## Examples

## Limitations

- A principal identifier is not an API key.
