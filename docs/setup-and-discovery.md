---
layout: default
title: Setup and discovery
permalink: /docs/setup-and-discovery/
description: Connect to the hosted Research Wiki safely and discover only capabilities available to the current identity.
---

# Setup and discovery

Use the public documentation without authentication. Sign in to the workspace or configure an MCP client only when you need governed research capabilities.

## Entry points

| Surface | URL | Authentication |
| --- | --- | --- |
| Workspace | `https://research.vnibb.xyz/` | Required |
| Documentation | `https://kitkitkittt.github.io/research-wiki/docs/` | Public |
| MCP | `https://research.vnibb.xyz/mcp/research-brain/` | Required |
| Raw setup skill | `https://kitkitkittt.github.io/research-wiki/downloads/skills/setup-and-discovery/SKILL.md` | Public |
| Setup schema | `https://kitkitkittt.github.io/research-wiki/skills/setup-and-discovery/schema.json` | Public |

## Safe connection sequence

1. Obtain a deployment-issued API key for your assigned identity; workspace sign-in alone does not configure an external MCP client.
2. Keep credentials in the client environment or approved secret store. Follow [manual Codex setup](../guides/mcp-setup.md#manual-codex-setup) when using Codex.
3. Initialize the MCP session at the absolute published endpoint, then send `notifications/initialized` and authenticated `tools/list`.
4. If listed, call `system.describe_capabilities`: its MCP output is `callable-capability-discovery-v1`. REST `GET /api/research-brain/runtime/capabilities` returns the separate `runtime-capabilities-v1` matrix.
5. Select only currently callable tools permitted to the identity. Public skill `readiness` and hashes are static descriptor metadata, not live readiness or authorization.
6. Complete one authorized evidence search and re-fetch its citation before claiming research works. Discovery-only is **connected, research blocked**.
7. Stop on typed authentication, permission, readiness, or scope errors. Retained archive tools, when callable, provide separately labeled document evidence, not canonical company mapping or Financial Truth.

## Agent setup

Give an agent the [raw setup skill]({{ '/downloads/skills/setup-and-discovery/SKILL.md' | relative_url }}) and its [machine schema]({{ '/skills/setup-and-discovery/schema.json' | relative_url }}). For broader context, use [`llms.txt`]({{ '/llms.txt' | relative_url }}) rather than copying unrelated documentation.

## Security boundary

Public skill and schema files describe behavior; they do not grant access. Never put a password, session cookie, bearer token, private source, or internal path into prompts, skill directories, repository files, or URLs.

Continue with [MCP setup]({{ '/guides/mcp-setup/' | relative_url }}) and [authority and access](authority-and-access.md).
