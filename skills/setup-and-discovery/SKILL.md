---
name: setup-and-discovery
description: Configure a scoped MCP client, diagnose authentication, and check caller-specific callable capabilities before research.
---

# Research Wiki Setup and Discovery

Skill ID: `skill.setup-and-discovery`
Version: `1.1.0`
Registry entry SHA-256: `92235c3af356e49a1c02c9f16665840f1ec6b2931ef4eb0633928b0363c9f2aa` (unchanged upstream spec binding, not this document's checksum)
Static descriptor readiness: `ready`; this public source metadata does not prove live research readiness or grant authority.

Connect a scoped client and discover current callable capabilities. These portable instructions are documentation, not a live capability response.

## Use when

- First connection
- Capability or authentication diagnosis

## Do not use when

- To bypass a disabled capability

## Required permissions

- Scopes: `research:read`
- Lanes: `public, analyst`

## Safe sequence

1. Configure the absolute `/mcp/research-brain/` endpoint and a deployment-issued API key in the client's secret environment; a principal identifier is not a key. See [manual client setup](https://kitkitkittt.github.io/research-wiki/guides/mcp-setup/).
2. Initialize the authenticated MCP session and send `notifications/initialized`.
3. Read authenticated `tools/list`, then call `system.describe_capabilities` only if exposed to this caller.
4. Select only tools currently reported callable. Static descriptors, hashes, and a successful discovery call do not establish research readiness.
5. Complete one authorized search and re-fetch a returned citation before reporting research success. Discovery-only is **connected, research blocked**.
6. Stop on typed permission or readiness errors; report missing tools and authority without silently widening access.

## Interfaces

- REST: `GET /api/research-brain/runtime/capabilities`
- REST: `GET /api/research-brain/mcp/catalog`
- MCP: `system.describe_capabilities`
- Input: `none`
- REST runtime matrix output: `runtime-capabilities-v1`
- MCP callable discovery output: `callable-capability-discovery-v1`
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
- Retained `archive.list_documents`, `archive.search`, `archive.fetch`, and `archive.get_resources` are usable only when authenticated runtime discovery exposes them as callable. Follow the [archive document workflow](https://kitkitkittt.github.io/research-wiki/guides/agent-workflows/); it provides retained document evidence, not canonical company identity or authoritative numeric Financial Truth.
